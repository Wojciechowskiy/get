# jetMeasure.py — снимает один профиль струи (или калибровку)
#
# Запуск:
#   python3 jetMeasure.py "00 mm.txt" 40          -> профиль: 40 точек через 1 мм
#   python3 jetMeasure.py "00 Pa.txt" 50 0        -> калибровка: 50 точек на месте
#
# 1-й параметр — имя файла, 2-й — число точек, 3-й — шагов между точками (по умолчанию 28 = 1 мм)

import sys
import time
import numpy as np
import jetFunctions as j

# ---------- параметры ----------
filename = "test.txt"    # имя файла
count = 40               # сколько точек
stepsBetween = 28        # шагов между точками (28 шагов = 1 мм)
samples = 10             # сколько отсчётов АЦП читать в одной точке

# если параметры написаны в команде запуска — берём их
if len(sys.argv) > 1:
    filename = sys.argv[1]
if len(sys.argv) > 2:
    count = int(sys.argv[2])
if len(sys.argv) > 3:
    stepsBetween = int(sys.argv[3])

print("Файл:", filename, "| точек:", count, "| шагов между точками:", stepsBetween)
# --------------------------------

rows = []                # сюда пишем пары (номер шага, отсчёт АЦП)
start = time.time()

try:
    j.initSpiAdc()
    j.initStepMotorGpio()

    for i in range(count):
        # 1) читаем несколько отсчётов в этой точке
        values = []
        for k in range(samples):
            values.append(j.getAdc())
            time.sleep(0.05)       # АЦП выдаёт новое число 10 раз в секунду

        # 2) берём медиану (она не боится сбойных чисел) и запоминаем
        m = np.median(values)
        rows.append((i * stepsBetween, m))
        print(i + 1, "из", count, ":", m)

        # 3) сдвигаем трубку и ждём, пока датчик успокоится
        if stepsBetween > 0:
            j.stepForward(stepsBetween)
            time.sleep(0.2)

    # 4) возвращаем трубку в начальную точку
    if stepsBetween > 0:
        j.stepBackward(count * stepsBetween)

    # 5) сохраняем файл: два столбца — шаг и отсчёт АЦП
    header = "%s, points %d, steps between %d, samples %d, %.0f s\nstep adc" % (
        filename, count, stepsBetween, samples, time.time() - start)
    np.savetxt(filename, np.array(rows), fmt=["%d", "%.1f"], header=header)
    print("Сохранено в", filename)

finally:
    # выполнится всегда, даже при ошибке или Ctrl+C
    j.deinitSpiAdc()
    j.deinitStepMotorGpio()
