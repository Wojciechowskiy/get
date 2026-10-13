import r2r_dac as r2r
import signal_generator
import time
amplitude = 3.0
signal_frequency = 10
sampling_frequency = 1000
dac  = r2r.R2R_DAC([16,20,21,25,26,17,27,22], 3.183, False)
try:
    
    start_time = time.time()
    while True:
        t = time.time() - start_time
        voltage = signal_generator.get_triangle_wave_amplitude(signal_frequency, t)*amplitude
        dac.set_voltage(voltage)
        signal_generator.wait_for_sampling_period(sampling_frequency)
finally:
    dac.deinit()
