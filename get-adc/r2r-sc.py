import time
from r2r_adc import R2R_ADC
import adc_plot

# Замени 3.3 на динамический диапазон ЦАП, измеренный мультиметром
dynamic_range = 3.3

voltage_values = []
time_values = []
duration = 3.0

adc = None

try:
    adc = R2R_ADC(dynamic_range, compare_time=0.0001)

    start_time = time.time()

    while time.time() - start_time < duration:
        voltage = adc.get_sc_voltage()
        voltage_values.append(voltage)
        time_values.append(time.time() - start_time)

    # Задание 2: график
    adc_plot.plot_voltage_vs_time(time_values, voltage_values, dynamic_range)

    # Задание 3: гистограмма
    adc_plot.plot_sampling_period_hist(time_values)

finally:
    if adc is not None:
        adc.deinit()
