import paho.mqtt.publish as publish
import RPi.GPIO as GPIO
from time import sleep

# initialize variables
MQTT_SERVER = "192.168.1.5"
MQTT_CHANNEL_GARBAGE = "channel_garbage_amount"
GARBAGE_BIN_ID = "20"

# Pin numbers
PIN_US_TRIGGER = 12
PIN_US_ECHO = 18
PIN_DOOR_MOTOR = 03

# Start configure pins for Door motor
GPIO.setmode(GPIO.BOARD)
GPIO.setup(PIN_DOOR_MOTOR, GPIO.OUT) # output to send our PWM signal on
pwm=GPIO.PWM(PIN_DOOR_MOTOR, 50) # setup PWM on pin #3 at 50Hz
pwm.start(0) # start it with 0 duty cycle so it doesn't set any angles on startup
# End Door motor
# Start configure pins for distance
GPIO.setup(PIN_US_TRIGGER, GPIO.OUT)
GPIO.output(PIN_US_TRIGGER, False)
GPIO.setup(PIN_US_ECHO, GPIO.IN)
# End for distance

# move main motor to bin


# open door by rotating door motor
SetAngle(90)
sleep(3)
SetAngle(0)
pwm.stop()

# fire up calculating measurement
distance = getGarbageMeasurement()

# broadcast measurement via MQTT
publish.single(MQTT_CHANNEL_GARBAGE, GARBAGE_BIN_ID + ':' + str(distance), hostname=MQTT_SERVER)

# move back to starting position


GPIO.cleanup()

# === method registrations ===
def SetAngle(angle):
    duty = angle / 18 + 2
    GPIO.output(PIN_DOOR_MOTOR, True)
    pwm.ChangeDutyCycle(duty)
    sleep(1)
    GPIO.output(PIN_DOOR_MOTOR, False)
    pwm.ChangeDutyCycle(0)

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
    distanceInCM= round(distanceInCM, 2)
    time.sleep(10)
    return distanceInCM
