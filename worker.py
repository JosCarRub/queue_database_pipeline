import pika
import json
import os
import sys
import time
from decimal import Decimal

def setup_django():

    sys.path.append(os.path.dirname(os.path.abspath(__file__)))
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'queue_database_pipeline.settings')
    
    import django
    django.setup()
# función que se ejecuta cada vez que Pika recibe un mensaje
def callback(ch, method, properties, body):
    """
    procesa un mensaje recibido de la cola.
    ch: el canal
    method: información sobre la entrega del mensaje
    properties: propiedades del mensaje
    body: el contenido del mensaje (en bytes)
    """
    print(f" [x] Mensaje recibido: {body.decode()}")
    
    # de body a un diccionario de Python
    message_data = json.loads(body.decode())

    from apps.products.presentation.inyector import Inyector
    from apps.products.domain.exceptions import DuplicateProductError, InvalidProductError

    try:
        # caso de uso que sabe crear productos en la db
        create_uc = Inyector.create_product_uc()
        
        create_uc.execute(
            name=message_data['name'],
            description=message_data['description'],
            price=Decimal(message_data['price'])
        )
        
        # Si todo va bien, enviamos el "acknowledgement" (ack).
        # RabbitMQ borrará el mensaje de la cola.
        ch.basic_ack(delivery_tag=method.delivery_tag)
        print(" [x] Mensaje procesado y confirmado (ack).")

    except (DuplicateProductError, InvalidProductError) as e:

        print(f" [!] Error al procesar el mensaje: {e}")
        ch.basic_ack(delivery_tag=method.delivery_tag)
    
    except Exception as e:
        print(f" [!] Error inesperado: {e}")
        # NO se envia ack para que el mensaje permanezca en la cola, RabbitMQ intentará re-entregarlo
        ch.basic_nack(delivery_tag=method.delivery_tag, requeue=True)

def main():

    setup_django()    
    from decouple import config

    host = config('RABBITMQ_HOST', default='localhost')
    # Bucle de reconexión.
    while True:
        try:
            connection = pika.BlockingConnection(pika.ConnectionParameters(host=host))
            channel = connection.channel()

            channel.queue_declare(queue='product_creation_queue', durable=True)
            
            # El worker no recibirá un nuevo mensaje hasta que no haya terminado de procesar el actual
            # Esto evita que un worker se sature si los mensajes llegan muy rápido
            channel.basic_qos(prefetch_count=1)
            
            # 'basic_consume' suscribe la función 'callback' a la cola.
            channel.basic_consume(queue='product_creation_queue', on_message_callback=callback)

            print(' [*] Esperando mensajes. Para salir, presiona CTRL+C')
            # 'start_consuming' inicia el bucle de escucha. Es un proceso bloqueante.
            channel.start_consuming()

        except pika.exceptions.AMQPConnectionError as e:
            print(f"Error de conexión con RabbitMQ: {e}. Reintentando en 5 segundos...")
            time.sleep(5)
        except KeyboardInterrupt:
            print('Interrumpido por el usuario.')
            break
        except Exception as e:
            print(f"Un error inesperado ha ocurrido: {e}. Reiniciando...")
            time.sleep(5)


if __name__ == '__main__':
    main()