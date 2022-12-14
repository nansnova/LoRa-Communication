# -*- coding: utf-8 -*-
"""
Publicador_MQTT.ipynb
"""

#importación de librerías
import pandas as pd
import time
from datetime import datetime
import paho.mqtt.client as mqttClient
import json

dataframe=pd.read_csv("DatosPruebaMQTT.csv")
dataframe.head()

dataframe.describe(include="all")
df=dataframe.dropna() #aquí voy a limpiar todos los valores no numéricos
print(df)
temp=df.Temperature.tolist()
hum=df.Humidity.tolist()
co=df.CO2.tolist()

def on_connect(client, userdata, flags, rc):
    """
    Función que establece la conexión
    """
    if rc==0:
        print("Conectado al broker")
        global Connected
        Connected = True
    else:
        print("Falla en la conexión")
    return

Connected = False  #variable para verificar el estado de la conexión
broker_address="192.168.1.67" #dirección del Broker
port= 1883 #puerto por defecto de MQTT
tag1 = "/CADI/I40/Temperatura"  #tag, etiqueta o tópico
tag2 = "/CADI/I40/Humedad"  #tag, etiqueta o tópico
tag3 = "/CADI/I40/CO2"  #tag, etiqueta o tópico

client = mqttClient.Client("identificador") #instanciación
client.on_connect = on_connect #agregando la función
client.connect(broker_address, port)
client.loop_start() #inicia la instancia

while Connected != True:
    time.sleep(0.1)
    try:
        for i,j,k in zip(temp,hum,co):
            val1=str(i) #json.dumps("Temperatura: "+str(i))
            val2=str(j) #json.dumps("Humedad: "+str(j))
            val3=str(k) #json.dumps("CO2: "+str(k))
            print(tag1,val1,'\n',tag2,val2,'\n',tag3,val3)
            client.publish(tag1,val1,qos=2)
            client.publish(tag2,val2,qos=2)
            client.publish(tag3,val3,qos=2)
            time.sleep(2)
    except KeyboardInterrupt: #cuando presionas Ctrl +C
        print("Envío de datos detenido por el usuario")
        client.disconnect()
        client.loop_stop()

