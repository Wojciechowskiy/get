import r2r_dac as r2r
import signal_generator as sg
import time
amplitude = 3.0
signal_frequency = 10
sampling_frequency = 1000
dac  = r2r.R2R_DAC([16,20,21,25,26,17,27,22], 3.183, False)


try:
    

    current_time = 0
    while True:
        normalized = sg.get_sin_wave_amplitude(signal_frequency, current_time)
        voltage = normalized * amplitude
        dac.set_voltage(voltage)
        sg.wait_for_sampling_period(sampling_frequency)
        current_time += 1 / sampling_frequency
finally:
    dac.deinit()