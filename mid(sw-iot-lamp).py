import uasyncio as asyncio
from machine import Pin
import network
import time
from umqtt.robust import MQTTClient
from config import (
    WIFI_SSID, WIFI_PASS,
    MQTT_BROKER, MQTT_USER, MQTT_PASS
)
 
led_wifi = Pin(2, Pin.OUT)
led_wifi.value(1)  # turn the red led off
led_iot = Pin(12, Pin.OUT)
led_iot.value(1)   # turn the green led off
 
wlan = network.WLAN(network.STA_IF)
wlan.active(True)

wlan.connect(WIFI_SSID, WIFI_PASS)

while not wlan.isconnected():
    time.sleep(0.5)
led_wifi.value(0)  # turn the red led on
 
mqtt = MQTTClient(client_id="",
                  server=MQTT_BROKER,
                  user=MQTT_USER,
                  password=MQTT_PASS)
mqtt.connect()
led_iot.value(0)   # turn the green led on

sw1 = Pin(16, Pin.IN, Pin.PULL_UP)   # sw1 to toggle the light
lamp = Pin(25, Pin.OUT)
lamp.value(1)  # turn USB lamp off initially
 
def sub_callback(topic, payload):
    # use decode instead of direct byte-array comparison
    if topic.decode() == "b6310545400/lamp/2":
        try:
            # make payload to percentage of 1023
            lamp.value(1-int(payload))
            count = int(lamp.value())
            print(payload)
        except ValueError:
            pass

mqtt.set_callback(sub_callback)
mqtt.subscribe("b6310545400/lamp/2")

async def switch_toggle():
    while True:
        # wait until sw is pressed
        while sw1.value() == 1:
            await asyncio.sleep_ms(0)
        await asyncio.sleep_ms(50) # debounce
 
        # toggle lamp
        lamp.value(1-lamp.value())
        mqtt.publish("b6310545400/lamp/2", str(1-lamp.value()))
        # wait until sw1 is released
        while sw1.value() == 0:
            await asyncio.sleep_ms(0)
        await asyncio.sleep_ms(50) # debounce

async def check_mqtt():
    while True:
        mqtt.check_msg()
        await asyncio.sleep_ms(50)

asyncio.create_task(check_mqtt())
asyncio.create_task(switch_toggle())
asyncio.run_until_complete()