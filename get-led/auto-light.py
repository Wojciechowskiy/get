import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM)
sensor = 6
led = 26
GPIO.setup(sensor, GPIO.IN)
GPIO.setup (led, GPIO.OUT)

while True:
    sensor_state = GPIO.input(sensor)
    inverted_state = 1 - sensor_state
    GPIO.output (led, inverted_state)