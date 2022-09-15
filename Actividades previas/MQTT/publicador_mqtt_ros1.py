#!/usr/bin/env python
"""
Publicador_MQTT
Autores: EQ 5
"""
#Librerias para manipulacion de csv
import pandas as pd
import time
from datetime import datetime
#Librerias para comunicacion mqtt
import paho.mqtt.client as mqttClient
import json
#Librerias ROS
import rospy
import numpy as np
#Mensajes de ROS necesarios
from std_msgs.msg import Float32

class pub_data():
    def __init__(self):
        #Iniciamos el nodo
        rospy.init_node("pub_temp_hum_co2")
        #Creamos los subscribers para leer los sensores
        rospy.Subscriber("/temp_sens",Float32,self.temp_sens_callback)
        rospy.Subscriber("/hum_sens",Float32,self.hum_sens_callback)
        rospy.Subscriber("/co2_sens",Float32,self.co2_sens_callback)
        #Creamos los Publishers que publicaran
        self.pub_temp = rospy.Publisher("/temp", Float32, queue_size = 3)
        self.pub_hum = rospy.Publisher("/hum", Float32, queue_size = 3)
        self.pub_co2 = rospy.Publisher("/co2", Float32, queue_size = 3)
        self.classDictionary = {1: "temperature", 2: "humidity", 3: "co2"}
        #Variables usadas para obtener los datos de los subscribers
        self.frame = np.array([[]],dtype = "uint8")
        self.temp_sens = 0
        self.hum_sens = 0
        self.co2_sens = 0
        #Mensajes por segundo
        self.rate = rospy.Rate(60)
        #Cuando se acabe el codigo o lo tiremos llamemos esa funcion
        rospy.on_shutdown(self.end_callback)

    #funciones callback para extraer los datos de los suscriptores
    def temp_sens_callback(self,data):
        self.temp_sens = data.data
    def hum_sens_callback(self,data):
        self.hum_sens = data.data
    def co2_sens_callback(self,data):
        self.co2_sens = data.data

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

    def main(self):
        while not rospy.is_shutdown():
            #Declaramos el df del que obtendremos la informacion
            dataframe=pd.read_csv("DatosPruebaMQTT.csv")
            dataframe.head()
            dataframe.describe(include="all")
            df=dataframe.dropna() #aquí voy a limpiar todos los valores no numéricos
            print(df)
            temp=df.Temperature.tolist()
            hum=df.Humidity.tolist()
            co=df.CO2.tolist()

            #Conexion MQTT
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

