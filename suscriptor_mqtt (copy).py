# -*- coding: utf-8 -*-
"""
Suscriptor_MQTT.ipynb
"""

import paho.mqtt.client as mqttClient
import time

def on_connect(client, userdata, flags, rc):
    """Función que establece la conexión

    """
    if rc==0:
        print("Conectado al broker")
        global Connected
        Connected = True
    else:
        print("Falla en la conexión")
    return

def on_message(client,userdata,message):
    """
    Función que recibe los mensajes del broker
    """
    print("Mensaje - {}:{}".format(message.topic, message.payload))
    return

Connected = False  #variable para verificar el estado de la conexión
broker_address="192.168.1.67" #dirección del Broker
port= 1883 #puerto por defecto de MQTT
tag = "/CADI/I40/#"  #tag, etiqueta o tópico

client1=mqttClient.Client("cliente")
client1.on_connect=on_connect
client1.on_message=on_message
client1.connect(broker_address,port)
client1.loop_start()

while Connected != True:
    time.sleep(0.1)
    client1.subscribe(tag)
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Recepción de mensajes detenida por el usuario")
        client1.disconnect()
        client1.loop_stop()
