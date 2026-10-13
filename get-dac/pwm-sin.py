import pwm_dac
import signal_generator
import time

amplitude = 3.0
signal_frequency = 10
sampling_frequency = 1000
dac = pwm_dac.PWM_DAC(12,500,3.290, False)
try:
        
    current_time = 0
    while True:
        
        voltage = signal_generator.get_sin_wave_amplitude(signal_frequency, current_time )* amplitude
        dac.set_voltage(voltage)
        signal_generator.wait_for_sampling_period(sampling_frequency)
        current_time  += 1/ sampling_frequency
finally:
    dac.deinit()
    