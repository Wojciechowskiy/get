import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM)
leds=[16,12,25,17,27,23,22,24]
for led in leds:
    GPIO.setup (led, GPIO.OUT)
for led in leds:
    GPIO.output(led,0)

num = 0

up = 9
down = 10
GPIO.setup(up,GPIO.IN)
GPIO.setup(down,GPIO.IN)
def dec2bin(value):
    return [int(element) for element in bin(value) [2:].zfill(8)]
sleep_time = 0.2
while True:
    if GPIO.input(up):
        num = num +1
        print (num, dec2bin(num))
        time.sleep(sleep_time)
    if GPIO.input(down):
        num = num -1
        print (num, dec2bin(num))
        time.sleep(sleep_time)
    if num > 255:
        num = 0
    if num < 0:
        num = 255
    [GPIO.output(leds[i], dec2bin(num)[i]) for i in range(len(leds))]



