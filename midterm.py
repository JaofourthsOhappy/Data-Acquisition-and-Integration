from machine import Pin, ADC, I2C
from umqtt.robust import MQTTClient
from config import (
    WIFI_SSID, WIFI_PASS,
    MQTT_BROKER, MQTT_USER, MQTT_PASS
)
import network
import uasyncio as asyncio
from time import sleep


led_wifi = Pin(2, Pin.OUT)
led_iot = Pin(12, Pin.OUT)
switch = Pin(16, Pin.IN, Pin.PULL_UP)
COUNT = 0


# Initially turn the on-board red and green LEDs off.
led_iot.value(1)   # turn the green led off
led_wifi.value(1)  # turn the red led off

# Connect to the Wi-Fi network KUWIN; once connected, turn the red LED on.
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(WIFI_SSID, WIFI_PASS)
while not wlan.isconnected():
    sleep(2)
led_wifi.value(0)  # turn the red led on

# Connect to the broker on iot.cpe.ku.ac.th with a unique client ID; once connected, turn the green LED on.
mqtt = MQTTClient(
    client_id="",
    server=MQTT_BROKER,
    user=MQTT_USER,
    password=MQTT_PASS
)
mqtt.connect()
led_iot.value(0)   # turn the green led on

# Subscribe to the topic daq2020/midterm/student-id/blink
# Blink the red LED for the number of times specified in the message's payload
# Each blinking consists of LED being on for 250ms and off for 750ms
MQTT_TOPIC1 = "b6310545400/test1"
def blink(times):
    for i in range(times):
        led_wifi.value(0)
        sleep(0.25)
        led_wifi.value(1)
        sleep(0.75)
    led_wifi.value(1)

def blink_listener(topic, payload):
    # use decode instead of direct byte-array comparison
    if topic.decode() == MQTT_TOPIC1:
        print(payload)
        try:
            blink(int(payload))
        except ValueError:
            print("There is an error")

async def check_mqtt():
    while True:
        mqtt.check_msg()
        await asyncio.sleep_ms(0)

# Count how many times button S1 has been pressed
MQTT_TOPIC2 = "b6310545400/test2"
async def count_button_handler():
    while True:
        before_value = switch.value()
        await asyncio.sleep_ms(20)
        after_value = switch.value()
        if before_value and before_value != after_value:
            await trigger_count()
        

async def trigger_count():
    global COUNT
    COUNT += 1
    print(COUNT)
    mqtt.publish(MQTT_TOPIC2, str(COUNT))

mqtt.set_callback(blink_listener)
mqtt.subscribe(MQTT_TOPIC1)
asyncio.create_task(check_mqtt())
asyncio.create_task(count_button_handler())
asyncio.run_until_complete()