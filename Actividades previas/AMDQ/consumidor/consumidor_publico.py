import pika,os

def receptor():
    url = os.environ.get('CLOUDAMQP_URL', )
    params = pika.URLParameters(url)
    connection = pika.BlockingConnection(params)
    channel = connection.channel()
    #ahora declaramos la cola o queue que vamos a 'consumir'
    cola="iot_public"
    channel.queue_declare(queue=cola)
    print("En espera de mensajes")
    def callback(ch, method, properties, body):
        print("Mensaje recibido %r" % body.decode())

    channel.basic_consume(queue=cola,on_message_callback=callback)
    channel.start_consuming()

try:
    receptor()
except KeyboardInterrupt: #cuando presionas Ctrl + C
    print("Recepción de datos detenida por el usuario")
