import pika

def receptor():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost')) #para establecer conexión
    channel = connection.channel()
    #ahora declaramos la cola o queue que vamos a 'consumir'
    cola="local"
    channel.queue_declare(queue=cola)

    def callback(ch, method, properties, body):
        print("Mensaje recibido %r" % body.decode())

    channel.basic_consume(queue=cola,on_message_callback=callback)
    channel.start_consuming()

try:
    receptor()
except KeyboardInterrupt: #cuando presionas Ctrl + C
    print("Recepción de datos detenida por el usuario")
