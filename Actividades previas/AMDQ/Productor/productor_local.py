import pika

connect = pika.BlockingConnection(pika.ConnectionParameters(host='10.0.2.15')) #para establecer conexión
channel = connect.channel()
#ahora declaramos la cola o queue
cola="local"
channel.queue_declare(queue=cola)
#channel.exchange_declare(exchange='logs', exchange_type='fanout')

msg=input("Escribe tu mensaje: ")

try:
    while msg != "." :
        channel.basic_publish(exchange='',routing_key=cola,body=msg)
        print("Enviando :",msg)
        msg=input("Escribe tu mensaje: ")
except KeyboardInterrupt: #cuando presionas Ctrl + C
    print("Envío de datos detenido por el usuario")
    connect.close()
