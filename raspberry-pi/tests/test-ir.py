import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BOARD)

PIN_IR_TRIGGER = 16
PIN_IR_RECEIVER = 15

# IR Sensor
GPIO.setup(PIN_IR_TRIGGER, GPIO.OUT)
GPIO.output(PIN_IR_TRIGGER, True)
GPIO.setup(PIN_IR_RECEIVER, GPIO.IN)
# End IR Sensor


# Listen for IR break to catch Initiation
try:
    while True:
        #GPIO.output(PIN_IR_TRIGGER, True)
        print "Output - " + str(GPIO.input(PIN_IR_RECEIVER))
        time.sleep(0.2)
        #GPIO.output(PIN_IR_TRIGGER, False)

        # if GPIO.input(PIN_IR_RECEIVER):
        #     print "Object Detected"
        #     while GPIO.input(PIN_IR_RECEIVER):
        #         time.sleep(0.2)
        # else:
        #     print "No Object"
        #     time.sleep(0.2)

except KeyboardInterrupt:
    GPIO.cleanup()

GPIO.cleanup()
