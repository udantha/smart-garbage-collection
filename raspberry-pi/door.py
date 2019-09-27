import RPi.GPIO as GPIO
import time
import sys

GPIO.setmode(GPIO.BCM)
GPIO.setup(18, GPIO.OUT)
pwm = GPIO.PWM(18, 50)
pwm.start(0)


try:
        #open
        pwm.ChangeDutyCycle(7.5)  # turn towards 90 degree #Open 
        time.sleep(1)
        #close
        pwm.ChangeDutyCycle(2.5)  # turn towards 0 degree
        time.sleep(1) # sleep 1 second

#except KeyboardInterrupt:
        pwm.stop()
        GPIO.cleanup()


except IOError as e:
    print "I/O error({0}): {1}".format(e.errno, e.strerror)
