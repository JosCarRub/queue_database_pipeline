import pika
import json
from typing import Dict, Any

from apps.products.domain.publishers import ProductPublisher
from decouple import config

class PikaProductPublisher(ProductPublisher):
    """
    implementación del publicador de mensajes (ProductPublisher)
    habla con RabbitMQ usando Pika
    """
    def __init__(self):

        host = config('RABBITMQ_HOST', default='localhost')
        port = config('RABBITMQ_PORT', default=5672, cast=int)
        user = config('RABBITMQ_USER', default='guest')
        password = config('RABBITMQ_PASS', default='guest')

        # objeto de credenciales para Pika
        credentials = pika.PlainCredentials(user, password)
        # objeto de parámetros de conexión
        parameters = pika.ConnectionParameters(host=host, port=port, credentials=credentials)
        #conexión síncrona con RabbitMQ
        self.connection = pika.BlockingConnection(parameters)


        #apertura del canal dentro del server de rabbit
        self.channel = self.connection.channel()
        #declaración de la cola
        self.channel.queue_declare(
            queue='product_creation_queue',  # dirección: comprueba si existe y si no existe la crea
            durable=True # si rabbit se reinicia la cola permanece
        )


    def publish_product_creation(self, product_data: Dict[str, Any]) -> None:
        """
        Publicador de mensajes en la cola de creación de productos.
        """
        # de Dic a string Json
        message = json.dumps(product_data)
        self.channel.basic_publish(
            exchange='', 
            routing_key='product_creation_queue', # dirección
            body=message, # contenido en string JSON
            properties=pika.BasicProperties(
                delivery_mode=2,  # Hace que el mensaje sea persistente
            )
        )
        print(f" [x] Mensaje enviado a la cola: '{message}'")
        self.connection.close()
