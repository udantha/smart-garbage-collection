import paho.mqtt.publish as publish
import RPi.GPIO as GPIO
import time
import random
import os

# initialize variables
MQTT_SERVER = "192.168.8.103"
MQTT_CHANNEL_GARBAGE = "channel_garbage_amount"
GARBAGE_BIN_ID = "20"
GARBAGE_BIN_TYPE_METAL = "BIN_METAL"
GARBAGE_BIN_TYPE_ALL = "BIN_NON_METAL"

# Pin numbers
PIN_US_TRIGGER = 12
PIN_US_ECHO = 11
PIN_MOTOR_DOOR = 7
PIN_MOTOR_MAIN = 40
PIN_IR_TRIGGER = 15
PIN_IR_RECEIVER = 16
PIN_SWITCH = 38

GPIO.setmode(GPIO.BOARD)

# IR Sensor
GPIO.setup(PIN_IR_TRIGGER, GPIO.OUT)
#GPIO.output(PIN_IR_TRIGGER, True)
GPIO.setup(PIN_IR_RECEIVER, GPIO.IN)
# End IR Sensor

# Configure Switch
GPIO.setup(PIN_SWITCH, GPIO.IN, pull_up_down=GPIO.PUD_UP)
# End switch configuration


# Listen for IR break to catch Initiation
try:
    while True:
        switchState = GPIO.input(PIN_SWITCH)
        if (GPIO.input(PIN_IR_TRIGGER)) or (switchState == False):
            os.system('python run.py')
            while GPIO.input(PIN_IR_TRIGGER):
                time.sleep(0.2)

except KeyboardInterrupt:
    print "Garbage Ending."

except:
    # this catches ALL other exceptions including errors.
    print "exception occurred!"

finally:
    GPIO.cleanup()  # this ensures a clean exit
