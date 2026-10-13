import pwm_dac
import signal_generator
import time

amplitude = 3.0
signal_frequency = 10
sampling_frequency = 1000
dac = pwm.dac.PWM_DAC(12,500,3.290, False)
try:
        
    start_time = time.time()
    while True:
        t = time.time() - start_time
        voltage = signal_generator.get_sin_wave_amplitude(signal_frequency, t)* amplitude
        dac.set_voltage(voltage)
        signal_generator.wait_for_sampling_period(sampling_frequency)
finally:
    dac.deinit()