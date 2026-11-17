########################################
# Проверка датчика давления HX710B
#
#   python3 jetCheck.py            - проверка SPI: устройство, режим выводов, сырые байты
#   python3 jetCheck.py bitbang    - чтение датчика без SPI, «ногодрыгом» через GPIO
#
# Подключение: OUT датчика -> GPIO9 (ножка 21), SCK датчика -> GPIO11 (ножка 23),
# GND датчика -> GND Raspberry Pi, VCC датчика -> 3.3 В (ножка 1)
########################################

import os
import subprocess
import sys
import time

OUT_PIN = 9
SCK_PIN = 11


def run(cmd):
    try:
        result = subprocess.run(cmd, capture_output=True, text=True)
        return (result.stdout + result.stderr).strip()
    except FileNotFoundError:
        return None


def pin_function(pin):
    # в новых системах утилита pinctrl, в старых raspi-gpio
    for cmd in (["pinctrl", "get", str(pin)], ["raspi-gpio", "get", str(pin)]):
        text = run(cmd)
        if text is not None:
            return text
    return "нет ни pinctrl, ни raspi-gpio"


def set_spi_function(pin):
    for cmd in (["pinctrl", "set", str(pin), "a0"], ["raspi-gpio", "set", str(pin), "a0"]):
        if run(cmd) is not None:
            return


def check_spi():
    import spidev

    print("1. Устройство SPI")
    if os.path.exists("/dev/spidev0.0"):
        print("   /dev/spidev0.0 есть")
    else:
        print("   /dev/spidev0.0 НЕТ: включите SPI в sudo raspi-config -> Interface Options -> SPI")
        return

    print("2. Режим выводов")
    for pin in (OUT_PIN, SCK_PIN):
        text = pin_function(pin)
        mark = "в режиме SPI" if "SPI" in text else "НЕ в режиме SPI: raspi-gpio set %d a0" % pin
        print("   GPIO%d: %s -> %s" % (pin, text, mark))

    print("3. Сырые байты от датчика")
    spi = spidev.SpiDev()
    spi.open(0, 0)
    spi.max_speed_hz = 1600000
    values = []
    try:
        for i in range(10):
            raw = spi.xfer2([0, 0, 0, 0])
            value = raw[0] << 16 | raw[1] << 8 | raw[2]
            values.append(value)
            print("   %s -> %d" % (raw, value))
            time.sleep(0.15)    # датчик выдаёт новое значение 10 раз в секунду
    finally:
        spi.close()

    print("4. Вывод")
    if all(v == 0 for v in values):
        print("   Одни нули: до датчика не доходят такты или Raspberry Pi не видит линию OUT.")
        print("   Проверьте режим выводов (пункт 2), провода на ножках 21 и 23 и общую землю.")
        print("   Затем запустите: python3 jetCheck.py bitbang")
    elif all(v == 0xFFFFFF for v in values):
        print("   Одни единицы: OUT всё время в 1. Проверьте питание датчика и провод SCK.")
    elif len(set(values)) == 1:
        print("   Одно и то же число: подуйте в трубку Пито. Если не меняется, проверьте трубки.")
    else:
        print("   Датчик читается. Подуйте в трубку Пито: числа должны вырасти на тысячи.")


def check_bitbang():
    import RPi.GPIO as GPIO

    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup(OUT_PIN, GPIO.IN)
    GPIO.setup(SCK_PIN, GPIO.OUT, initial=0)
    try:
        for i in range(10):
            # ждём готовности: датчик опускает OUT в 0
            start = time.time()
            while GPIO.input(OUT_PIN) == 1:
                if time.time() - start > 0.5:
                    print("   OUT не опускается в 0 за 0,5 с: датчик не готов, проверьте питание и провод OUT")
                    return
            value = 0
            for bit in range(24):
                # без пауз: если SCK дольше 60 мкс в единице, датчик засыпает
                GPIO.output(SCK_PIN, 1)
                value = value << 1 | GPIO.input(OUT_PIN)
                GPIO.output(SCK_PIN, 0)
            GPIO.output(SCK_PIN, 1)    # 25-й такт: следующее измерение, дифференциальный вход, 10 Гц
            GPIO.output(SCK_PIN, 0)
            print("   %d" % value)
            time.sleep(0.15)
        print("   Числа около 200 000 и растут, если подуть: датчик и провода исправны,")
        print("   значит, нули по SPI дают настройки SPI или провод на ножке 21.")
    finally:
        GPIO.cleanup()
        # возвращаем выводы под SPI, иначе jetFunctions.py будет читать нули
        set_spi_function(OUT_PIN)
        set_spi_function(SCK_PIN)
        print("   Выводы возвращены в режим SPI. Проверьте: raspi-gpio get 9 и 11")


if len(sys.argv) > 1 and sys.argv[1] == "bitbang":
    check_bitbang()
else:
    check_spi()
