import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BOARD)

# Pin numbers
PIN_SWITCH = 38

GPIO.setup(PIN_SWITCH, GPIO.IN, pull_up_down=GPIO.PUD_UP)

while True:
    input_state = GPIO.input(PIN_SWITCH)
    if input_state == False:
        print('Button Pressed')
        time.sleep(0.2)

GPIO.cleanup()
