# quickPlot.py — быстро посмотреть, что получилось в файле
#
# Запуск:  python3 quickPlot.py "00 mm.txt"
# Для калибровки печатает среднее и разброс.

import sys
import numpy as np
import matplotlib.pyplot as plt

filename = sys.argv[1]
data = np.loadtxt(filename)
steps = data[:, 0]
adc = data[:, 1]

good = adc < 500000                 # выбрасываем сбойные числа АЦП
print("Точек:", len(adc), "| сбойных:", len(adc) - np.sum(good))
adc = adc[good]
steps = steps[good]

print("Среднее: %.0f   разброс (std): %.0f" % (np.mean(adc), np.std(adc)))
print("Левый край: %.0f   правый край: %.0f   максимум: %.0f" % (
    np.median(adc[:5]), np.median(adc[-5:]), np.max(adc)))

plt.plot(steps, adc, "o-")
plt.xlabel("Шаг двигателя")
plt.ylabel("Отсчёт АЦП")
plt.title(filename)
plt.grid()
plt.show()
