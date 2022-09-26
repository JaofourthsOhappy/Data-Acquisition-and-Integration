from time import sleep
from machine import Pin

while(True):
    led_wifi = Pin(12, Pin.OUT)
    print("Turning WIFI LED on for 0.1 seconds...")
    led_wifi.value(0)
    sleep(0.1)
    print("Turning WIFI LED off for 0.9 seconds...")
    led_wifi.value(1)
    sleep(0.9)