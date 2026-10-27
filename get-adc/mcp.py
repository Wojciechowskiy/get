import time

from mcp3021_driver import MCP3021
from adc_plot import plot_voltage_vs_time, plot_sampling_period_hist


voltage_values = []
time_values = []

duration = 10.0


# Замени 5.0 на напряжение, измеренное на контакте PWR блока AUX
adc = MCP3021(5.0, verbose=False)

try:
    start_time = time.time()

    while time.time() - start_time < duration:
        voltage = adc.get_voltage()
        voltage_values.append(voltage)

        current_time = time.time() - start_time
        time_values.append(current_time)

    plot_voltage_vs_time(time_values, voltage_values, adc.dynamic_range)
    plot_sampling_period_hist(time_values)

finally:
    adc.deinit()
