import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM)
botton =13
led = 26
GPIO.setup(botton, GPIO.IN)
GPIO.setup (led, GPIO.OUT)
state = 0
while True:
    if GPIO.input(botton)==0:
        state = 1 - state
        GPIO.output(led, state)
        time.sleep(0.2)
        while GPIO.input(botton) == 0:
            time.sleep(0.05)
    time.sleep(0.05)
