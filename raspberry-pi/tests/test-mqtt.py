import RPi.GPIO as GPIO
import time
import sys
import paho.mqtt.publish as publish

GPIO.setmode(GPIO.BOARD)

# initialize variables
MQTT_SERVER = "192.168.8.100"
MQTT_CHANNEL_GARBAGE = "channel_garbage_amount"
GARBAGE_BIN_ID = "1"
GARBAGE_BIN_TYPE_METAL = "BIN_METAL"
GARBAGE_BIN_TYPE_ALL = "BIN_NON_METAL"


try:
    print "Start MQTT broadcasting.."
    # broadcast measurement via MQTT
    publish.single(MQTT_CHANNEL_GARBAGE, GARBAGE_BIN_ID + ':' +
                   str(50) + ':BIN_NON_METAL', hostname=MQTT_SERVER)
    print "MQTT Broadcast completed."

GPIO.cleanup()
