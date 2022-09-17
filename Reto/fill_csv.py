from random import randint, uniform, choice
from datetime import datetime
import csv

'''
VARIABLES IMPORTANTES:
    -temperatura de la transmision 90 a 150 Cel
    -voltaje de la batería   12.5 a 12.9 (V)
'''

data = []
valid_lst = ["A", "V"]
long_lst = ["W","E"]
lat_lst = ["N","S"]
fuel_lst =list(range(30,100))
km_lst =list(range(13,100))
dt = datetime.now()

headers = ['GPS_H', 'GPS_VALID', 'GPS_LONG', 'GPS_COOR_LONG', 'GPS_LAT', 'GPS_COOR_LAT', 'GPS_VEL', 'GPS_ORI', 'GPS_DATE',
                  'IMU_AX', 'IMU_AY', 'IMU_AZ', 'IMU_GX', 'IMU_GY', 'IMU_GZ', 'WL', 'WR',
                  'CS_FILL', 'CS_KGP', 'CS_VEL_TH',
                  'CH_FUEL', 'CH_KM', 'CH_OIL', 'CH_LWP', 'CH_RWP', 'TEMP', 'HUM', 'DIST', 'ALERT']

hour = dt.time()
validation = ""
longitude = [0.0, ""] # [longitude, coordinate]
latitude = [0.0, ""] # [latitude, coordinate]
gps_vel = 0.0
gps_ori = 0.0
gps_date = dt.date()

#IMU VARIABLES
a = [0.0, 0.0, 0.0] # [ax, ay, az]
g = [0.0, 0.0, 0.0] # [gx, gy, gz]
wl = 0.0
wr = 0.0

#COLLECTION SYSTEM
fill = 0.0
kg = 0.0
th_vel = 0.0

#CHECKING
fuel = 0.0
km = 0.0
oil = 0.0
wheel_pressure = [0.0, 0.0] # [L, R]

#ENVIRONMENT
temp = 0.0
hum = 0.0
distance = 0.0
alert = 0.0


def data_generator():

    global hour, validation, longitude, latitude, gps_vel, gps_ori, gps_date, a, g, wl, wr, fill, kg, th_vel, fuel, km, oil, wheel_pressure, temp, hum, distance, alert
    global dt, fuel_lst, data

    dt = datetime.now()


    #GPS VARIABLES
    hour = str(dt.time())
    validation = choice(valid_lst)
    longitude = [round(uniform(0, 180),2), choice(long_lst)]
    latitude = [round(uniform(0, 90),2), choice(lat_lst)]
    gps_vel = round(uniform(-0.50, 0.50),2)
    gps_ori = round(uniform(-0.50, 0.50),2)
    gps_date = str(dt.date())

    #IMU VARIABLES
    a = [round(uniform(-0.50, 0.50),2),round(uniform(-0.50, 0.50),2), round(uniform(-0.50, 0.50),2)]
    g = [round(uniform(-0.50, 0.50),2),round(uniform(-0.50, 0.50),2), round(uniform(-0.50, 0.50),2)]

    wl = round(uniform(45, 50),2)# rad/s
    wr = wl #wr = round(uniform(0, 50),2) # rad/s

    #COLLECTION SYSTEM
    fill = round(uniform(0, 40),2)
    kg = round(uniform(0, 30),2)
    th_vel = round(uniform(50, 60),2) # rad/s

    #CHECKING
    fuel = fuel_lst.pop()
    km = km_lst.pop(0)
    oil =  5 #round(uniform((3.5, 5.5),2)
    wheel_pressure = [randint(30, 32), randint(30, 32)] # [L, R]

    #ENVIRONMENT
    temp = round(uniform(21, 23),2)
    hum = round(uniform(40, 50),2)
    distance = round(uniform(2, 10),2)
    alert = 0.0

    #print("datos cargados")

    data = [hour, validation, longitude[0], longitude[1], latitude[0], latitude[1], gps_vel, gps_ori, gps_date,
    a[0], a[1], a[2], g[0], g[1], g[2], wl, wr,
    fill, kg, th_vel,
    fuel, km,oil,wheel_pressure[0], wheel_pressure[1], temp, hum, distance, alert]

    #print("Preparación del bus de data")


with open("movil_information.csv", 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(headers)

    for i in range (60):
            data_generator()
            print(data)
            writer.writerow(data)
    print("datos cargados exitosamente al csv")
