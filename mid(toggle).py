from machine import Pin
from time import sleep
from time import time
sw1 = Pin(16, Pin.IN, Pin.PULL_UP)
lamp = Pin(25, Pin.OUT)
count = 1
time = 0
while True:
    lamp.value(count)
    if sw1.value() < 1:
        count += 1
        if count%2 == 0:
            count = 0
        else:
            count = 1
    time += 1
    if time == 60:
        count = 1
    sleep(0.125)

    



