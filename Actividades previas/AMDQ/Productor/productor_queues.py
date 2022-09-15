import pika
import pandas as pd
import time
import os

dataframe = pd.read_csv("DatosPruebaMQTT.csv")
dataframe.head()
dataframe.describe(include="all")

temp = dataframe.Temperature.tolist()
hum = dataframe.Humidity.tolist()
co = dataframe.CO2.tolist()

url = os.environ.get('CLOUDAMQP_URL', 'amqps://myqkmwsd:MYd_nwEcTvERSHHuW1oB6dud33f46cZ0@shark.rmq.cloudamqp.com/myqkmwsd')
params = pika.URLParameters(url)
connect = pika.BlockingConnection(params)
channel = connect.channel()

colas=["temp","humid","CO2"]
for q in colas:
    channel.queue_declare(queue=q)

time.sleep(0.1)
try:
    for i,j,k in zip(temp,hum,co):
        val1,val2,val3='{"Temperatura":"'+str(i)+'"}','{"Humedad":"'+str(j)+'"}','{"CO2":"'+str(k)+'"}'
        print(colas[0],val1,'\n',colas[1],val2,'\n',colas[2],val3)

        channel.basic_publish(exchange='', routing_key='temp', body=val1)
        channel.basic_publish(exchange='', routing_key='humid', body=val2)
        channel.basic_publish(exchange='', routing_key='CO2', body=val3)
        time.sleep(1)
except KeyboardInterrupt:
    print("Envío de datos detenido por el usuario")
    connect.close()
