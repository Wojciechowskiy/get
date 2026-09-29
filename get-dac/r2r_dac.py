import RPi.GPIO as GPIO
class R2R_DAC:
    def __init__(self, gpio_bits, dynamic_range, verbose = False):
        self.gpio_bits = gpio_bits
        self.dynamic_range = dynamic_range
        self.verbose = verbose
        GPIO.setmode (GPIO.BCM)
        GPIO.setup(self.gpio_bits, GPIO.OUT, initial = 0)
    def deinit(self):
        GPIO.output(self.gpio_bits , 0)
        GPIO.cleanup()
    def deinit(self):
        GPIO.output(self.gpio_bits, 0)
        GPIO.cleanup()
    def voltage_to_number(self, voltage):
        if not (0.0 <= voltage <= self.dynamic_range):
            print(f"Напряжение выходит за динамический диапазон ЦАП (0.00 - {self.dynamic_range:.2f} B)")
            return 0
        return int( voltage / self.dynamic_range * 255)
    def number_to_dac(self, number):
        bits =  [int(element) for element in bin(number)[2:].zfill(8)]
        for i, bit in enumerate(bits):
            GPIO.output(self.gpio_bits[i], bit)
    def set_voltage(self, voltage):
        number = self.voltage_to_number(voltage)
        self.number_to_dac(number)
if __name__ == "__main__":
    try:
        dac = R2R_DAC([16,20,21,25,26,17,27,22], 3.183, True)
        while True:
            try:
                voltage = float(input("Введите напряжение в вольтах: "))
                
                dac.set_voltage(voltage)
            except ValueError:
                print ("Вы ввели не число. Попробуйте еще раз\n")
    finally:
        dac.deinit()
