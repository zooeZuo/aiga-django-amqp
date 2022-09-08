=====
aiga-django-amqp
=====

aiga-django-amqp merupakan package khusus django untuk keperluan berkomunikasi dengan rabbitmq

Quick start
-----------

1. Tambahkan "aiga_amqp" ke INSTALLED_APPS pada file settings.py::

    INSTALLED_APPS = [
        ...
        'aiga_amqp',
    ]

2. Pada folder app yang anda inginkan, tambahkan file ``consumer.py``
3. Pada file ``consumer.py`` buat function untuk menangani message seperti contoh dibawah ini::

    def consumer(channel, method, properties, body):
        print('saya telah baru saja melakukan sesuatu hal yang penting disini ...')

4. Pada file ``apps.py`` override method ``ready`` dan lakukan perintah seperti contoh berikut untuk mengeksekusi ``consumer.py``::

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


Settings Variable
-----------

Coming soon