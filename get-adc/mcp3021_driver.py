import smbus
import time


class MCP3021:
    def __init__(self, dynamic_range, verbose=False):
        self.bus = smbus.SMBus(1)
        self.dynamic_range = dynamic_range
        self.address = 0x4D
        self.verbose = verbose

    def deinit(self):
        self.bus.close()

    def get_number(self):
        data = self.bus.read_word_data(self.address, 0)

        lower_data_byte = data >> 8
        upper_data_byte = data & 0xFF

        number = (upper_data_byte << 6) | (lower_data_byte >> 2)

        if self.verbose:
            print(
                f"Принятые данные: {data}, "
                f"Старший байт: {upper_data_byte:x}, "
                f"Младший байт: {lower_data_byte:x}, "
                f"Число: {number}"
            )

        return number

    def get_voltage(self):
        number = self.get_number()
        voltage = number * self.dynamic_range / 1023
        return voltage


if __name__ == "__main__":
    adc = None

    try:
        # Замени 5.0 на динамический диапазон, измеренный на контакте PWR блока AUX
        adc = MCP3021(5.0, verbose=False)

        while True:
            voltage = adc.get_voltage()
            print(f"Напряжение: {voltage:.3f} В")
            time.sleep(1)

    except KeyboardInterrupt:
        print("\nИзмерения остановлены")

    finally:
        if adc is not None:
            adc.deinit()
