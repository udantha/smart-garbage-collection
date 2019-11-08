import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BOARD)

# Pin numbers
PIN_MOTOR_DOOR = 7

# Start configure pins for Door motor
GPIO.setup(PIN_MOTOR_DOOR, GPIO.OUT)  # output to send our PWM signal on
motorGateDoor = GPIO.PWM(PIN_MOTOR_DOOR, 50)  # setup PWM on pin #3 at 50Hz
# start it with 0 duty cycle so it doesn't set any angles on startup
motorGateDoor.start(0)
# End Door motor

try:
    # open
    # turn towards 90 degree #Open
    motorGateDoor.ChangeDutyCycle((270 / 18 + 2))
    time.sleep(1)
    # close
    motorGateDoor.ChangeDutyCycle(2.5)  # turn towards 0 degree
    time.sleep(1)  # sleep 1 second
    motorGateDoor.stop()
    
except KeyboardInterrupt:
    GPIO.cleanup()

GPIO.cleanup()
