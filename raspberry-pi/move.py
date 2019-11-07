import paho.mqtt.publish as publish
import RPi.GPIO as GPIO
import time

# initialize variables
MQTT_SERVER = "192.168.8.100"
MQTT_CHANNEL_GARBAGE = "channel_garbage_amount"
GARBAGE_BIN_ID = "20"
GARBAGE_BIN_TYPE_METAL = "BIN_METAL"
GARBAGE_BIN_TYPE_ALL = "BIN_NON_METAL"

# Pin numbers
PIN_US_TRIGGER = 12
PIN_US_ECHO = 18
PIN_MOTOR_DOOR = 12
PIN_MOTOR_MAIN = 11
PIN_IR_TRIGGER = 16

GPIO.setmode(GPIO.BOARD)

# IR Sensor
GPIO.setup(PIN_IR_TRIGGER, GPIO.IN)
# End IR Sensor

# Start configure pins for Door motor
GPIO.setup(PIN_MOTOR_DOOR, GPIO.OUT)  # output to send our PWM signal on
motorGateDoor = GPIO.PWM(PIN_MOTOR_DOOR, 50)  # setup PWM on pin #3 at 50Hz
# start it with 0 duty cycle so it doesn't set any angles on startup
motorGateDoor.start(0)
# End Door motor

# Main motor
GPIO.setup(PIN_MOTOR_MAIN, GPIO.OUT)
motorMain = GPIO.PWM(PIN_MOTOR_MAIN, 50)
motorMain.start(0)
# End Main motor

# Start configure pins for distance
GPIO.setup(PIN_US_TRIGGER, GPIO.OUT)
GPIO.output(PIN_US_TRIGGER, False)
GPIO.setup(PIN_US_ECHO, GPIO.IN)
# End for distance

# Listen for IR break to catch Initiation
try:
    while True:
        if GPIO.input(PIN_IR_TRIGGER):
            # 1. Initiate Metal detector
            # Set the target bin
            targetBinType = GARBAGE_BIN_TYPE_ALL  # or GARBAGE_BIN_TYPE_METAL based on

            # 2. decide which way to turn and Turn
            if targetBinType == GARBAGE_BIN_TYPE_METAL:
                # turn the opening towards metal
                motorMain.ChangeDutyCycle(7.5)  # turn towards 90 degree
                time.sleep(0.5)

            # 3. Open gate and drop garbage
            # open
            motorGateDoor.ChangeDutyCycle(7.5)  # turn towards 90 degree #Open
            time.sleep(1)
            # close
            motorGateDoor.ChangeDutyCycle(2.5)  # turn towards 0 degree
            time.sleep(1)  # sleep 1 second
            motorGateDoor.stop()

            # 4. Get garbage size
            # fire up calculating measurement
            distance = getGarbageMeasurement()

            # broadcast measurement via MQTT
            publish.single(MQTT_CHANNEL_GARBAGE, GARBAGE_BIN_ID + ':' + str(distance) + ':' + targetBinType, hostname=MQTT_SERVER)

            # 5. back to original position
            # turn the opening towards default all position
            motorMain.ChangeDutyCycle(2.5)  # turn towards 0 degree
            time.sleep(0.5)
            motorMain.stop()

            while GPIO.input(PIN_IR_TRIGGER):
                time.sleep(0.2)

except KeyboardInterrupt:
    GPIO.cleanup()

GPIO.cleanup()

# === method registrations ===


# def SetAngle(angle):
#     duty = angle / 18 + 2
#     GPIO.output(PIN_DOOR_MOTOR, True)
#     pwm.ChangeDutyCycle(duty)
#     sleep(1)
#     GPIO.output(PIN_DOOR_MOTOR, False)
#     pwm.ChangeDutyCycle(0)


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
