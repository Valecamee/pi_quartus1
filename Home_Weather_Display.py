import grovepi
import csv
import numpy as np
from grovepi import *
from grove_rgb_lcd import *
from time import sleep
from math import isnan
import datetime


button = 2
potentiometer = 2
light_sensor = 1
dht_sensor_port = 3
dht_sensor_type = 0 

grovepi.pinMode(potentiometer,"INPUT")
#data = []

while True:
    try:
        
        p = int(grovepi.analogRead(potentiometer)/204.5)
        now = datetime.datetime.now()
        formatted_date = now.strftime("%d/%m/%y/%H:%M:%S")
        
        button_status = digitalRead(button)
        light_intensity = grovepi.analogRead(light_sensor)
        # check if we have nans
        # if so, then raise a type error exception
        [ temp,hum ] = dht(dht_sensor_port,dht_sensor_type)
        print("temp =", temp, "C\thumidity =", hum,"%")
        print(p)
        
        

        if isnan(temp) is True or isnan(hum) is True:
            raise TypeError('nan error')

        t = str(temp)
        h = str(hum)
        l = str(light_intensity)
        pt = str(p)

        if button_status:
            
            setText_norefresh("Temp:" + t + "C\n" + "Humidity:" + h + "%")
            sleep(0.5)
        else:
            setText_norefresh("light:" + l + "\n" + "Time:" + pt +"s")
            sleep(0.5)
            
            filename = "tabla.csv"
        
        with open(filename, mode = "a") as file:
            writer = csv.writer(file)
        
            writer.writerow([formatted_date,t,h,l])
            time.sleep(p)
        print("Datos guardados en ", filename)
        
    except (IOError, TypeError) as e:
        print(str(e))
        # and since we got a type error
        # then reset the LCD's text
        setText("")

    except KeyboardInterrupt as e:
        print(str(e))
        # since we're exiting the program
        # it's better to leave the LCD with a blank text
        setText("")
        break

    sleep(0.5)# wait some time before re-updating the LCD
