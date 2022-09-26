from machine import Pin, PWM
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
 
lamp = PWM(Pin(25, Pin.OUT))
lamp.duty(1023)  # turn USB lamp off initially
 
def sub_callback(topic, payload):
    # use decode instead of direct byte-array comparison
    if topic.decode() == "b6310545400/lamp":
        try:
            # make payload to percentage of 1023
            lamp.duty(1023-int(int(payload)*1023/100))
            print(payload)
        except ValueError:
            pass
    
mqtt.set_callback(sub_callback)
mqtt.subscribe("b6310545400/lamp")
 
while True:
    mqtt.check_msg()
