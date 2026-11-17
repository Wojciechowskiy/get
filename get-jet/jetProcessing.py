# jetProcessing.py — обработка данных лабораторной работы 1 (струя)
# 1) калибровки: отсчёты АЦП -> паскали, шаги -> метры
# 2) профили скорости во всех сечениях
# 3) расход в каждом сечении и график расхода от расстояния

import numpy as np
import matplotlib.pyplot as plt

dataPath = "Пример данных/"   # папка с файлами; для своих данных: dataPath = "data/"

# ---------- данные калибровки (поменяйте на свои) ----------
p0 = 0          # давление в первом файле калибровки, Па
p1 = 45         # давление во втором файле (по манометру), Па
calibSteps = 500  # на сколько шагов сдвигали трубку
calibMm = 18      # на сколько миллиметров она сдвинулась
rho = 1.2       # плотность воздуха, кг/м^3
distances = [0, 10, 20, 30, 40, 50, 60, 70]   # сечения, мм
# ------------------------------------------------------------


def readAdc(filename):
    # читает файл "шаг отсчёт" и выбрасывает сбойные отсчёты АЦП
    data = np.loadtxt(filename)
    steps = data[:, 0]
    adc = data[:, 1]
    good = adc < 500000          # сбойные числа на порядок больше
    return steps[good], adc[good]


# ===== 1. Калибровка давления =====
s, adc0 = readAdc(dataPath + "calibration/%02d Pa.txt" % p0)
s, adc1 = readAdc(dataPath + "calibration/%02d Pa.txt" % p1)
adcPoints = [np.mean(adc0), np.mean(adc1)]
pPoints = [p0, p1]
k, b = np.polyfit(adcPoints, pPoints, 1)     # P = k*N + b
print("k = %.4f Па/отсчёт" % k)

plt.figure()
x = np.linspace(min(adcPoints), max(adcPoints), 10)
plt.plot(adcPoints, pPoints, "o", label="Измерения")
plt.plot(x, k * x + b, label="P = %.4f·N %+.0f [Па]" % (k, b))
plt.xlabel("Отсчёты АЦП")
plt.ylabel("Давление [Па]")
plt.title("Калибровка датчика давления")
plt.grid()
plt.legend()
plt.savefig("pressure-calibration.png")

# ===== 2. Калибровка перемещения =====
mPerStep = calibMm / 1000 / calibSteps        # метров на один шаг
print("1 шаг = %.2e м" % mPerStep)

plt.figure()
plt.plot([0, calibSteps], [0, calibMm], "o", label="Измерения")
plt.plot([0, calibSteps], [0, calibMm],
         label="x = %.4f·n [мм]" % (calibMm / calibSteps))
plt.xlabel("Шаги двигателя")
plt.ylabel("Перемещение [мм]")
plt.title("Калибровка перемещения")
plt.grid()
plt.legend()
plt.savefig("distance-calibration.png")


# ===== 3. Скорость в одном сечении =====
def calculateVelocity(filename):
    steps, adc = readAdc(filename)

    # ноль давления — прямая между левым и правым краем профиля
    n = 5
    left = np.median(adc[:n])
    right = np.median(adc[-n:])
    zero = np.interp(np.arange(len(adc)), [n / 2, len(adc) - n / 2], [left, right])

    # давление в паскалях
    p = k * (adc - zero)

    # маленькие и отрицательные давления — это шум, обнуляем
    edges = np.concatenate([adc[:n] - left, adc[-n:] - right])
    threshold = max(3 * k * np.std(edges), 3)
    p[p < threshold] = 0

    # скорость по Бернулли
    u = np.sqrt(2 * p / rho)

    # координата в метрах
    x = steps * mPerStep

    # центр струи — «центр масс» профиля
    xCenter = np.sum(x * u) / np.sum(u)
    x = x - xCenter
    return x, u


# ===== 4. Расход в одном сечении =====
def calculateOutgo(x, u):
    r = np.abs(x)                       # радиус — расстояние до оси
    f = rho * 2 * np.pi * r * u         # подынтегральная функция
    # сумма трапеций по всему профилю
    total = 0
    for i in range(len(x) - 1):
        total += (f[i] + f[i + 1]) / 2 * (x[i + 1] - x[i])
    return total / 2                    # две половины -> среднее


# ===== 5. Общий график скоростей с расходом в легенде =====
outgo = []
plt.figure(figsize=(10, 6))
for d in distances:
    x, u = calculateVelocity(dataPath + "%02d mm.txt" % d)
    q = calculateOutgo(x, u)
    outgo.append(q * 1000)              # в г/с
    print("%2d мм: Vmax = %.1f м/с, Q = %.2f г/с" % (d, max(u), q * 1000))
    plt.plot(x * 1000, u, label="Q (%02d мм) = %.2f [г/с]" % (d, q * 1000))
plt.xlabel("Расстояние от оси струи [мм]")
plt.ylabel("Скорость воздуха [м/с]")
plt.title("Профили скорости в сечениях струи")
plt.grid()
plt.legend()
plt.savefig("velocity-outgo.png")

# ===== 6. Расход от расстояния =====
a, c = np.polyfit(distances, outgo, 1)
plt.figure()
plt.plot(distances, outgo, "o", label="Измерения")
plt.plot(distances, a * np.array(distances) + c,
         label="Q = %.3f·z + %.2f [г/с]" % (a, c))
plt.xlabel("Расстояние от сопла [мм]")
plt.ylabel("Расход [г/с]")
plt.title("Расход струи от расстояния до сопла")
plt.grid()
plt.legend()
plt.savefig("outgo-distance.png")

plt.show()
