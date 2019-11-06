import RPi.GPIO as GPIO
from time import sleep

GPIO.setmode(GPIO.BOARD)

PIN_IR_TRIGGER = 15
PIN_IR_RECEIVER = 16

# IR Sensor
GPIO.setup(PIN_IR_TRIGGER, GPIO.OUT)
GPIO.setup(PIN_IR_RECEIVER, GPIO.IN)
# End IR Sensor


# Listen for IR break to catch Initiation
try:
    while True:
        GPIO.output(PIN_US_TRIGGER, True)

        if GPIO.input(PIN_IR_RECEIVER):
            print "Object Detected"
            while GPIO.input(PIN_IR_RECEIVER):
                time.sleep(0.2)
        else:
            print "No Object"
            time.sleep(0.2)

except KeyboardInterrupt:
    GPIO.cleanup()

GPIO.cleanup()
