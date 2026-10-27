import RPi.GPIO as GPIO
import time


class R2R_ADC:
    def __init__(self, dynamic_range, compare_time=0.01, verbose=False):
        self.dynamic_range = dynamic_range
        self.verbose = verbose
        self.compare_time = compare_time

        # Пины входов R2R-ЦАП: старший бит первым, младший последним
        self.bits_gpio = [26, 20, 19, 16, 13, 12, 25, 11]
        # Пин, подключённый к выходу компаратора
        self.comp_gpio = 21

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.bits_gpio, GPIO.OUT, initial=0)
        GPIO.setup(self.comp_gpio, GPIO.IN)

    def deinit(self):
        GPIO.output(self.bits_gpio, 0)
        GPIO.cleanup()

    def dec2bin(self, value):
        # Число -> список из 8 нулей и единиц, например 5 -> [0,0,0,0,0,1,0,1]
        return [int(element) for element in bin(value)[2:].zfill(8)]

    def number_to_dac(self, number):
        GPIO.output(self.bits_gpio, self.dec2bin(number))

    # ---------- Задание 1: АЦП последовательного счёта ----------
    def sequential_counting_adc(self):
        for number in range(256):
            self.number_to_dac(number)
            time.sleep(self.compare_time)

            comp_value = GPIO.input(self.comp_gpio)

            if self.verbose:
                print(f"Число: {number}, компаратор: {comp_value}")

            # 1 на компараторе = напряжение ЦАП стало больше входного
            if comp_value == 1:
                return number

        # Напряжение ЦАП так и не превысило входное
        return 255

    def get_sc_voltage(self):
        number = self.sequential_counting_adc()
        voltage = number * self.dynamic_range / 255
        return voltage

    # ---------- Задание 4: АЦП последовательного приближения ----------
    def successive_approximation_adc(self):
        number = 0

        # Перебираем биты от старшего (128) к младшему (1)
        for i in range(7, -1, -1):
            bit_value = 2 ** i

            # Пробуем поставить этот бит в 1
            number = number + bit_value
            self.number_to_dac(number)
            time.sleep(self.compare_time)

            comp_value = GPIO.input(self.comp_gpio)

            if self.verbose:
                print(f"Бит: {bit_value}, число: {number}, компаратор: {comp_value}")

            # ЦАП больше входного напряжения -> перебор, убираем бит
            if comp_value == 1:
                number = number - bit_value

        return number

    def get_sar_voltage(self):
        number = self.successive_approximation_adc()
        voltage = number * self.dynamic_range / 255
        return voltage


if __name__ == "__main__":
    adc = None

    try:
        # Замени 3.3 на динамический диапазон ЦАП, измеренный мультиметром
        adc = R2R_ADC(3.3)

        while True:
            # Задание 1 (последовательный счёт):
            # voltage = adc.get_sc_voltage()

            # Задание 4 (последовательное приближение):
            voltage = adc.get_sar_voltage()

            print(f"Напряжение: {voltage:.3f} В")

    except KeyboardInterrupt:
        print("\nИзмерения остановлены")

    finally:
        if adc is not None:
            adc.deinit()
