from django.utils.translation import gettext_lazy as _
from django.conf import settings
from pika.exchange_type import ExchangeType
from threading import Thread
from uuid import uuid4
import pika, os

SETTINGS = {
    'HOST' : 'localhost',
    'PORT' : 5672,
    'CREDENTIAL' : False,
    'USERNAME' : None,
    'PASSWORD' : None,
    'HEARTBEAT' : 600,
    'TIMEOUT' : 300
}

if hasattr(settings, 'AIGA_AMQP'):
    SETTINGS.update(settings.AIGA_AMQP)

class AMQPConnector(pika.BlockingConnection):
    BasicProperties = pika.BasicProperties

    def __init__(self):
        params = {
            'host' : SETTINGS['HOST'], 
            'port' : int(SETTINGS['PORT']),
            'heartbeat' : int(SETTINGS['HEARTBEAT']),
            'blocked_connection_timeout' : int(SETTINGS['TIMEOUT'])            
        }

        if SETTINGS['CREDENTIAL']:
            params['credentials'] = pika.PlainCredentials(
                settings.AIGA_AMQP['USERNAME'],
                settings.AIGA_AMQP['PASSWORD']
            )

        self.__connection_parameters = pika.ConnectionParameters(**params)

        super().__init__(self.__connection_parameters, None)

class AMQPListener:
    ExchangeType = ExchangeType

    def __init__(self):
        self.connection = self.__connect()

    def __connect(self):
        return AMQPConnector()

    def __disconnect(self):
        self.connection.close()

    def consume(self, consumer, channel_name = None):
        def runner():
            ch_name = channel_name
            channel = self.connection.channel()
            channel.queue_declare(queue=ch_name)
            channel.basic_qos(prefetch_count=1)

            def callback(channel, method, properties, body):
                consumer(channel, method, properties, body)
                channel.basic_ack(delivery_tag=method.delivery_tag)

            channel.basic_consume(queue=ch_name, on_message_callback=callback)
            channel.start_consuming()

        thread = Thread(name=uuid4(), target=runner)
        thread.daemon = True
        thread.start()
        return thread

    def subscribe(self, consumer, exchange_key = None, routing_key = '', exchange_type = ExchangeType.fanout):
        def runner():
            ch_name = exchange_key
            channel = self.connection.channel()

            exchange_declaration_params = {
                'exchange' : ch_name,
                'exchange_type' : exchange_type
            }

            channel.exchange_declare(**exchange_declaration_params)

            queue = channel.queue_declare(queue='', exclusive=True)

            queue_bind = {
                'exchange' : ch_name,
                'queue' : queue.method.queue
            }

            if routing_key is not None:
                queue_bind['routing_key'] = routing_key

            channel.queue_bind(**queue_bind)

            def callback(channel, method, properties, body):
                consumer(channel, method, properties, body)

            channel.basic_consume(queue=queue.method.queue, auto_ack=True, on_message_callback=callback)
            channel.start_consuming()

        thread = Thread(name=uuid4(), target=runner)
        thread.daemon = True
        thread.start()
        return thread

    def __enter__(self):
        print(self.connection)

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.__disconnect()

# function untuk mengirim queue ke rabbit mq
def send_queue(channel : str, message : str):
    connection = AMQPConnector()
    ch = connection.channel()
    ch.queue_declare(queue=channel)
    ch.basic_publish('', routing_key=channel, body=message)
    connection.close()

# function untuk mempublish queue ke rabbit mq
def publish_queue(exchange : str, message : str):
    pubsub_queue(
        message=message, 
        exchange=exchange, 
    )

def publish_direct_queue(exchange : str, routing_key : str, message : str):
    pubsub_queue(
        message=message, 
        exchange=exchange, 
        routing_key=routing_key, 
        exchange_type=ExchangeType.direct
    )

def publish_topic_queue(exchange : str, routing_key : str, message : str):
    pubsub_queue(
        message=message, 
        exchange=exchange, 
        routing_key=routing_key, 
        exchange_type=ExchangeType.topic
    )

def pubsub_queue(message : str, exchange : str, routing_key : str = '', exchange_type = ExchangeType.fanout):
    connection = AMQPConnector()
    ch = connection.channel()
    ch.exchange_declare(exchange=exchange, exchange_type=exchange_type)
    ch.basic_publish(exchange=exchange, routing_key=routing_key, body=message)
    connection.close()