#!/usr/bin/python
import RPi.GPIO as GPIO
import time

pin = 25 
data = []

GPIO.setmode(GPIO.BCM)

time.sleep(2)

GPIO.setup(pin, GPIO.OUT)
GPIO.output(pin, GPIO.HIGH)
GPIO.output(pin, GPIO.LOW)
time.sleep(0.04)
GPIO.output(pin, GPIO.HIGH)

GPIO.setup(pin, GPIO.IN)

while GPIO.input(pin) == GPIO.LOW:
    print ("收到了低电位")
    continue

while GPIO.input(pin) == GPIO.HIGH:
    print ("收到了高电位")
    continue

i = 0
while i < 40:
    print ("收到数据:", i)
    cnt = 0
    while GPIO.input(pin) == GPIO.LOW:
        print(i, ":收到了低电位")
        continue
    while GPIO.input(pin) == GPIO.HIGH:
        cnt += 1
        if cnt > 100:
            break    
    if cnt < 12:
        data.append(0)
    else:
        data.append(1)
    i += 1

humidity_bit = data[0:8]
humidity_point_bit = data[8:16]
temperature_bit = data[16:24]
temperature_point_bit = data[24:32]
check_bit = data[32:40]

humidity = 0
humidity_point = 0
temperature = 0
temperature_point = 0
check = 0

for i in range(8):
    humidity += humidity_bit[i] * 2 ** (7-i)
    humidity_point += humidity_point_bit[i] * 2 ** (7-i)
    temperature += temperature_bit[i] * 2 ** (7-i)
    temperature_point += temperature_point_bit[i] * 2 ** (7-i)
    check += check_bit[i] * 2 ** (7-i)

tmp = humidity + humidity_point + temperature +     temperature_point

if check == tmp:
    print ("temperature :", temperature, "*C, humidity:", humidity, "%")
else:
    print ("wrong")

GPIO.cleanup()
