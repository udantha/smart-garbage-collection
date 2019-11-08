import paho.mqtt.publish as publish
import RPi.GPIO as GPIO
import time
import random

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

# Configure Switch
GPIO.setup(PIN_SWITCH, GPIO.IN, pull_up_down=GPIO.PUD_UP)
# End switch configuration

# Function definitions
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

# Listen for IR break to catch Initiation
try:
    while True:
        switchState = GPIO.input(PIN_SWITCH)
        if (GPIO.input(PIN_IR_TRIGGER)) or (switchState == False):
            print "====================== Garbage Detected.. ======================"
            # 1. Initiate Metal detector
            # Set the target bin
            garbageTypeRandomTmp = [GARBAGE_BIN_TYPE_ALL, GARBAGE_BIN_TYPE_METAL]
            # or GARBAGE_BIN_TYPE_METAL based on
            targetBinType = GARBAGE_BIN_TYPE_METAL #random.choice(garbageTypeRandomTmp)

            # 2. decide which way to turn and Turn
            if targetBinType == GARBAGE_BIN_TYPE_METAL:
                print "Garbage Type is METAL"
                # turn the opening towards metal
                # turn towards 180 degree
                motorMain.ChangeDutyCycle(180 / 18 + 2)
                time.sleep(0.5)
            else:
                print "Garbage Type is ALL"
            # 3. Open gate and drop garbage
            # open
            print "Open Gate"
            motorGateDoor.ChangeDutyCycle(7.5)  # turn towards 90 degree #Open
            time.sleep(1)
            # close
            print "Gate closed"
            motorGateDoor.ChangeDutyCycle(2.5)  # turn towards 0 degree
            time.sleep(1)  # sleep 1 second
            motorGateDoor.stop()

            # 4. Get garbage size
            # fire up calculating measurement
            distance = getGarbageMeasurement()
            print "Garbage height is " + str(distance) + " cm"

            # broadcast measurement via MQTT
            publish.single(MQTT_CHANNEL_GARBAGE, GARBAGE_BIN_ID + ':' + str(distance) + ':' + targetBinType, hostname=MQTT_SERVER)

            # 5. back to original position
            # turn the opening towards default all position
            print "Main motor back to start."
            motorMain.ChangeDutyCycle(2)  # turn towards 0 degree
            time.sleep(0.5)
            motorMain.stop()

            print "====================== Completed a Cycle ======================"
            while GPIO.input(PIN_IR_TRIGGER):
                time.sleep(0.2)

except KeyboardInterrupt:
    print "Garbage Ending."

except:
    # this catches ALL other exceptions including errors.
    print "exception occurred!"

finally:
    GPIO.cleanup()  # this ensures a clean exit

# === method registrations ===


# def SetAngle(angle):
#     duty = angle / 18 + 2
#     GPIO.output(PIN_DOOR_MOTOR, True)
#     pwm.ChangeDutyCycle(duty)
#     sleep(1)
#     GPIO.output(PIN_DOOR_MOTOR, False)
#     pwm.ChangeDutyCycle(0)


