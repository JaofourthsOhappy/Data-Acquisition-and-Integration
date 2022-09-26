from machine import Pin, ADC, I2C
from time import sleep

ldr = ADC(Pin(36))
i2c = I2C(1, sda=Pin(4), scl=Pin(5))

while True:

    i2c.scan()
    i2c.writeto(77, bytearray(0))
    data = i2c.readfrom(77, 2)
    
    # x = data[0]
    # y = data[1]
    # w = x*256 + y
    temp_cel = ((data[0]*256)+data[1])/128
    
    print("Light detect as "+str(ldr.read())+" Lux")
    print("Temperature detect as "+str(temp_cel)+" °C")
    sleep(2)