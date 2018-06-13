#!/usr/bin/python

from gpiozero import CPUTemperature
from time import sleep, strftime, time
from sense_hat import SenseHat
import syslog
import json
from twython import Twython
from random import randint
import mysql.connector as mariadb

cpu = CPUTemperature()
sense = SenseHat()
sense.clear()
p = sense.get_pressure()
atm = (((p - 6.2) / 1013.25) * 29.9213)
t = sense.get_temperature()
treal = (t - 7.5)
h = sense.get_humidity()
hum = (h + 10)
o = sense.get_orientation()
pitch = o["pitch"]
roll = o["roll"]
yaw = o["yaw"]
acceleration = sense.get_accelerometer_raw()
x = acceleration['x']
y = acceleration['y']
z = acceleration['z']
x = abs(x)
y = abs(y)
z = abs(z)
temp = cpu.temperature

twitter = Twython(
	'',
        '',
        '',
        ''
)

twitM = "CPU Temp: " + str(temp) + " / " + "Temp: " + str(treal) + " / " + "Pressure: " + str(atm) + " / " + "Humidity: " + str(hum)
message = twitM
twitter.update_status(status=message)

data = json.dumps({
    'sensors': {
        'cputemp': temp,
        'pressure': atm,
	'temperature': treal,
	'humidity': hum,
	'pitch': pitch,
	'roll': roll,
	'yaw': yaw,
	'xaccl': x,
	'yaccl': y,
	'zaccl': z 
    }
})

print(strftime("%Y-%m-%d %H:%M:%S"),str(temp),str(atm),str(treal),str(hum),str(pitch),str(yaw),str(roll),str(x),str(y),str(z))
syslog.syslog(data)

mariadb_connection = mariadb.connect(user='root', password='', database='')
cursor = mariadb_connection.cursor()
cursor.execute("INSERT INTO [database] VALUES ('"+str(temp)+"', '"+str(atm)+"', '"+str(treal)+"', '"+str(hum)+"')")
mariadb_connection.commit()
mariadb_connection.close()

with open("/home/pi/weatherconditions.csv", "a") as log:
        log.write("{0},{1},{2},{3},{4}\n".format(strftime("%Y-%m-%d %H:%M:%S"),str(temp),str(atm),str(treal),str(hum)))
