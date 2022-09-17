#!/usr/bin/env python3

#############################  LIBRARIES  #############################

from datetime import datetime
from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS
import pandas as pd
import operator as op
import time


#############################  CSV FILE  ##############################
headers = ['GPS_H', 'GPS_VALID', 'GPS_LONG', 'GPS_COOR_LONG', 'GPS_LAT', 'GPS_COOR_LAT', 'GPS_VEL', 'GPS_ORI', 'GPS_DATE',
                  'IMU_AX', 'IMU_AY', 'IMU_AZ', 'IMU_GX', 'IMU_GY', 'IMU_GZ', 'WL', 'WR',
                  'CS_FILL', 'CS_KGP', 'CS_VEL_TH',
                  'CH_FUEL', 'CH_KM', 'CH_OIL', 'CH_LWP', 'CH_RWP', 'TEMP', 'HUM', 'DIST', 'ALERT']

csvfile = pd.read_csv('movil_information.csv', header=0)
c = csvfile.columns
print(len(c))
data = []

#############################  INFLUXDB2  #############################

# Database Specifications
bucket = "LoRa"
url = "http://192.168.1.70:8086"
token = "lB4hzN2Fh7lyajxjtvO9IXpwkvKNiljnLrvDCMGahHR0spHhr3Y128pzimD9o9dw2Bg7mkTsN2LW73bQWTx-BA=="
org = "EQ5"

# Client
client = InfluxDBClient(url, token, org)

# Write API
write_api = client.write_api(write_options=SYNCHRONOUS)

while True:
	for row in range (len(csvfile)):
		data = []
		for i in range (29):
			value = list(csvfile[c[i]])

			data.append(value[row])
		print(len(data))
		print(data)
		print()
		print()

		p = Point("Tractor 3312").field(headers[0], data[0]).field(headers[1], data[1]).field(headers[2], data[2]).field(headers[3], data[3]).field(headers[4], data[4]).field(headers[5], data[5]).field(headers[6], data[6]).field(headers[7], data[7]).field(headers[8], data[8]).field(headers[9], data[9]).field(headers[10], data[10]).field(headers[11], data[11]).field(headers[12], data[12]).field(headers[13], data[13]).field(headers[14], data[14]).field(headers[15], data[15]).field(headers[16], data[16]).field(headers[17], data[17]).field(headers[18], data[18]).field(headers[19], data[19]).field(headers[20], data[20]).field(headers[21], data[21]).field(headers[22], data[22]).field(headers[23], data[23]).field(headers[24], data[24]).field(headers[25], data[25]).field(headers[26], data[26]).field(headers[27], data[27]).field(headers[28], data[28])
		write_api.write(bucket=bucket, record=p, org=org)
		time.sleep(15) # 5 secon
