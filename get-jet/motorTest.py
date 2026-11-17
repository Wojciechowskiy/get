# motorTest.py — проверка шагового двигателя (без jetFunctions)
#
# Запуск:
#   python3 motorTest.py            -> 200 шагов вперёд и 200 назад
#   python3 motorTest.py 0          -> то же, но сигнал "разрешение" наоборот
#   python3 motorTest.py 1 0.01     -> медленнее (пауза 0.01 с)

import sys
import time
import RPi.GPIO as GPIO

directionPin = 24   # направление
enablePin = 25      # разрешение работы
stepPin = 26        # шаг

steps = 200         # сколько шагов
enableOn = 1        # каким сигналом включается драйвер (1 или 0)
delay = 0.005       # пауза между импульсами, с (больше — медленнее)

if len(sys.argv) > 1:
    enableOn = int(sys.argv[1])
if len(sys.argv) > 2:
    delay = float(sys.argv[2])

print("enableOn =", enableOn, "| delay =", delay)

GPIO.setmode(GPIO.BCM)
GPIO.setup([directionPin, enablePin, stepPin], GPIO.OUT)


def move(n, direction):
    GPIO.output(directionPin, direction)
    GPIO.output(enablePin, enableOn)        # включить драйвер
    for i in range(n):
        GPIO.output(stepPin, 0)
        time.sleep(delay)
        GPIO.output(stepPin, 1)             # один импульс = один шаг
        time.sleep(delay)
    GPIO.output(enablePin, 1 - enableOn)    # выключить драйвер


try:
    print("Вперёд", steps, "шагов")
    move(steps, 1)
    time.sleep(1)
    print("Назад", steps, "шагов")
    move(steps, 0)
    print("Готово. Трубка должна была съездить и вернуться (~7 мм).")
finally:
    GPIO.output([directionPin, enablePin, stepPin], 0)
    GPIO.cleanup()
