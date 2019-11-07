import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BOARD)

# Pin numbers
PIN_US_TRIGGER = 12
PIN_US_ECHO = 11

# Start configure pins for distance
GPIO.setup(PIN_US_TRIGGER, GPIO.OUT)
GPIO.output(PIN_US_TRIGGER, False)
GPIO.setup(PIN_US_ECHO, GPIO.IN)
# End for distance

def getGarbageMeasurement():
    # Waiting For Sensor1 To Settle
    time.sleep(.1)
    GPIO.output(PIN_US_TRIGGER, True)
    time.sleep(0.00001)
    GPIO.output(PIN_US_TRIGGER, False)

    while GPIO.input(PIN_US_ECHO) == 0:
        pass
        pulse_start1 = time.time()

    while GPIO.input(PIN_US_ECHO) == 1:
        pass
        pulse_end1 = time.time()

    pulse_duration1 = pulse_end1 - pulse_start1

    distanceInCM = pulse_duration1 * 17150
    distanceInCM = round(distanceInCM, 2)
    time.sleep(10)
    return distanceInCM

try:
    print "Height in CM - " + str(getGarbageMeasurement())
except KeyboardInterrupt:
    GPIO.cleanup()

GPIO.cleanup()

