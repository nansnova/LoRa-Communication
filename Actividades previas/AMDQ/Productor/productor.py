import pika #,os
import os

url = os.environ.get('CLOUDAMQP_URL', 'amqps://myqkmwsd:MYd_nwEcTvERSHHuW1oB6dud33f46cZ0@shark.rmq.cloudamqp.com/myqkmwsd')
params = pika.URLParameters(url)
connect = pika.BlockingConnection(params)
channel = connect.channel()
#ahora declaramos la cola o queue
cola="iot_public"
channel.queue_declare(queue=cola)

msg=input("Escribe tu mensaje: ")

try:
    while msg != "." :
        channel.basic_publish(exchange='',routing_key=cola,body=msg)
        print("Enviando :",msg)
        msg=input("Escribe tu mensaje: ")
except KeyboardInterrupt: #cuando presionas Ctrl + C
    print("Envío de datos detenido por el usuario")
    connect.close()
