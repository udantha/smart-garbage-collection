import RPi.GPIO as GPIO
import time
import sys

GPIO.setmode(GPIO.BOARD)

# Pin numbers
PIN_MOTOR_DOOR = 12
PIN_MOTOR_MAIN = 11

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

try:

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
    # 5. back to original position
    # turn the opening towards default all position
    motorMain.ChangeDutyCycle(2.5)  # turn towards 0 degree
    time.sleep(0.5)
    motorMain.stop()

#except KeyboardInterrupt:
    GPIO.cleanup()


except IOError as e:
    print "I/O error({0}): {1}".format(e.errno, e.strerror)
