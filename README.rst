merupakan package khusus django untuk keperluan berkomunikasi dengan rabbitmq

Quick start
-----------

1. Tambahkan "aiga_amqp" ke INSTALLED_APPS pada file settings.py::

    INSTALLED_APPS = [
        ...
        'aiga_amqp',
    ]

A.1 Message Sender
------------------

Berikut contoh kode untuk mengirim message::

    from aiga_amqp.core import send_queue

    send_queue('nama channel', message='ini pesan')


A.2 Compete Consumer
--------------------

Berikut merupakan langkah untuk consume antrian message secara "compete" atau bergantian.

1. Pada folder app yang anda inginkan, tambahkan file ``consumer.py``
2. Pada file ``consumer.py`` buat function untuk menangani message seperti contoh dibawah ini::

    def consumer(channel, method, properties, body):
        print('saya telah baru saja melakukan sesuatu hal yang penting disini ...')

3. Pada file ``apps.py`` override method ``ready`` dan lakukan perintah seperti contoh berikut untuk mengeksekusi ``consumer.py``::

    from django.apps import AppConfig

    class ExampleConfig(AppConfig):
        default_auto_field = 'django.db.models.BigAutoField'
        name = 'example'

        def ready(self) -> None:
            from aiga_amqp.core import AMQPListener
            from .consumer import consumer
            listener = AMQPListener()
            listener.consume(consumer, channel_name='your channel name')

5. Jalankan django

B.1 Publish Message
-------------------

segera


B.2 Subscribe Message
---------------------

segera

Settings Variable
-----------------

Terdapat beberapa variable yang bisa digunakan pada ``settings.py`` beserta default value nya::

    AIGA_AMQP = {
        'HOST' : 'localhost',   //alamat host dari rabbitmq
        'PORT' : 5672,          //port dari rabbitmq
        'CREDENTIAL' : False,   //set menjadi True jika menggunakan USERNAME dan PASSWORD
        'USERNAME' : None,      //username untuk mengakses rabbitmq
        'PASSWORD' : None,      //password untuk mengakses rabbitmq
        'HEARTBEAT' : 600,
        'TIMEOUT' : 300
    }
