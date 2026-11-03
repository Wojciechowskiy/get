# Зарядка и разрядка RC-цепи на плате AUX.
# Цепь питается от GPIO14: 1 -> конденсатор заряжается, 0 -> разряжается.
# Напряжение на конденсаторе меряет АЦП MCP3021 по I2C.
# Запуск: python3 rc.py
import os
import time
import RPi.GPIO as GPIO
from mcp3021_driver import MCP3021

DYNAMIC_RANGE = 5.11      # В, динамический диапазон MCP3021
PIN = 14                  # GPIO, от которого питается RC-цепь
WAIT_TIME = 50          # с, разряжаем конденсатор перед началом
CHARGE_TIME = 50          # с, сколько держим GPIO14 = 1
DISCHARGE_TIME = 50       # с, сколько держим GPIO14 = 0
FILE_NAME = "rc_data.csv"

# Включаем I2C на ножках 2 и 3 (вместо ручного raspi-gpio)
os.system("raspi-gpio set 2 a0")
os.system("raspi-gpio set 3 a0")

GPIO.setmode(GPIO.BCM)
GPIO.setup(PIN, GPIO.OUT, initial=0)
adc = MCP3021(DYNAMIC_RANGE)

times = []
voltages = []


# Измеряем напряжение duration секунд подряд
def record(duration, start):
    t_end = time.time() + duration
    while time.time() < t_end:
        voltages.append(adc.get_voltage())
        times.append(time.time() - start)


try:
    print("Разряжаю конденсатор перед началом...")
    time.sleep(WAIT_TIME)

    start = time.time()

    print("Зарядка")
    GPIO.output(PIN, 1)
    record(CHARGE_TIME, start)

    print("Разрядка")
    GPIO.output(PIN, 0)
    record(DISCHARGE_TIME, start)

finally:
    GPIO.output(PIN, 0)
    GPIO.cleanup()
    adc.deinit()

# Сохраняем результат в файл
with open(FILE_NAME, "w") as f:
    f.write("time_s,voltage_V\n")
    for i in range(len(times)):
        f.write(f"{times[i]:.6f},{voltages[i]:.4f}\n")

print(f"Измерений: {len(times)}")
print(f"Частота: {len(times) / times[-1]:.0f} Гц")
print(f"Сохранено в {FILE_NAME}")
