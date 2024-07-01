# Importing modules
import spidev # To communicate with SPI devices
from numpy import interp # To scale values
import time # To add delay
import RPi.GPIO as GPIO
import Adafruit_DHT
from sensor import MCP3004

# Set sensor type : Options are DHT11,DHT22 or AM2302
sensor = Adafruit_DHT.DHT11

# Set GPIO sensor is connected to
gpio = 18

# 自己接入的那个 pin 口
watering_channel = 19
GPIO.cleanup()
GPIO.setmode(GPIO.BCM)

mcp = MCP3004(bus=0,addr=0,vref=3.3)
mcp._spi.max_speed_hz = 2106000

while True:
    
    humidity, temperature = Adafruit_DHT.read_retry(sensor, gpio)
    print("start project!")
    
    if humidity is not None and temperature is not None:
        print('Temp={0:0.1f}*C Humidity={1:0.1f}%'.format(temperature, humidity))
    else:
        print('Failed to get reading. Try again!')


    
    output = mcp.read(0) # Reading from CH0
    print(output)
    # 数值越大越干燥 对于植物来说，一般大于400则可以进行浇水。
    if output > 400:
        # 进行控制开关水，每次浇水10秒钟
        GPIO.setup(watering_channel, GPIO.OUT)
        GPIO.output(watering_channel, GPIO.HIGH)
        time.sleep(10)
        GPIO.setup(watering_channel, GPIO.OUT)
        GPIO.output(watering_channel, GPIO.LOW)
    output = interp(output, [0, 1023], [100, 0])
    output = int(output)
    print("Moisture:", output)
    time.sleep(5)
