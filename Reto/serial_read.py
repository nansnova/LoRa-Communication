import serial
import time
import csv
import pandas as pd
import json
ser = serial.Serial('COM11',115200)

ser.flushInput()
while True:
    elementos_dic = ""
    ser_bytes = ser.readline()
    #decoded_bytes = float(ser_bytes[0:len(ser_bytes)-2].decode("utf-8"))
    decoded_bytes = ser_bytes.decode("utf-8")
    #dict = dict(decoded_bytes)
    cont = 0
    vals = []
    todo = ""
    dic = [{'Distance': 0,
            'Humidity': 0,
            'Temperature': 0,
            'State': 0}]
    #{'Distance': 1, 'Humidity': 2, 'Temperature': 3, 'State': 4}
    for element in decoded_bytes.split(', '):
        for element2 in element.split(': '):
            cont += 1
            vals.append(element2)
            print(element2)
            #print("*",vals)
            if element2 == "Distance":
                val_dis = vals[cont-1]
                dic[0]["Distance"] = vals[1]
            if element2 == "Humidity":
                val_dis = vals[cont-1]
                dic[0]["Humidity"] = vals[1]
            if element2 == "Temperature":
                val_dis = vals[cont-1]
                dic[0]["Temperature"] = vals[1]
            if element2 == "State":
                val_dis = vals[cont-1]
                dic[0]["State"] = element2[1]
            #my_dict = json.loads(dic)
            #my_keys = my_dict.keys()
            col_name=["Distance","Humidity","Temperature","State"]
            with open("movil_information.csv", 'w', newline='') as csvfile:
                    wr = csv.DictWriter(csvFile, fieldnames=col_name)
                    wr.writeheader()
                    wr.writerows(dic)
    print(dic)
