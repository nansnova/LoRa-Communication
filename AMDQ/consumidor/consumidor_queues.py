import pika,os

def receptor():
    url = os.environ.get('CLOUDAMQP_URL', )
    params = pika.URLParameters(url)
    connection = pika.BlockingConnection(params)
    channel = connection.channel()
    #ahora declaramos la cola o queue que vamos a 'consumir'
    colas=["temp","humid","CO2"]
    for i in colas:
        channel.queue_declare(queue=i)

    print("En espera de mensajes")
    def callback(ch, method, properties, body):
        print("Mensaje recibido %r" % body.decode())

    for j in colas:
        channel.basic_consume(queue=j,on_message_callback=callback)
        with open('DatosRecopilados.txt', 'w') as f:
            f.write('\n'.join(j))
    channel.start_consuming()

try:
    receptor()
except KeyboardInterrupt: #cuando presionas Ctrl + C
    print("Recepción de datos detenida por el usuario")
