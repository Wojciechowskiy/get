# Обработка rc_data.csv: постоянная времени tau разными способами.
# Запуск: python3 rc_analysis.py
import math
import numpy as np

FILE_NAME = "rc_data.csv"
CHARGE_TIME = 50          # с, как в rc.py

# Читаем файл
t = []
u = []
with open(FILE_NAME) as f:
    f.readline()
    for line in f:
        parts = line.strip().split(",")
        t.append(float(parts[0]))
        u.append(float(parts[1]))
t = np.array(t)
u = np.array(u)

# Делим на зарядку и разрядку, время разрядки отсчитываем от её начала
tc = t[t < CHARGE_TIME]
uc = u[t < CHARGE_TIME]
td = t[t >= CHARGE_TIME] - CHARGE_TIME
ud = u[t >= CHARGE_TIME]


# МНК для формулы U = A + B*exp(-t/tau):
# перебираем tau, для каждого A и B находятся обычной прямой линией,
# выбираем tau, при котором сумма квадратов отклонений самая маленькая
def fit(tt, uu):
    best_s = None
    best = None
    for tau in np.arange(7, 11, 0.001):
        x = np.exp(-tt / tau)
        B, A = np.polyfit(x, uu, 1)
        s = np.sum((uu - A - B * x) ** 2)
        if best_s is None or s < best_s:
            best_s = s
            best = (A, B, tau)
    return best


A, B, tau_fit_c = fit(tc, uc)
level63 = uc[0] + 0.632 * (A - uc[0])
tau63 = tc[np.argmax(uc >= level63)]

A2, B2, tau_fit_d = fit(td, ud)
level37 = 0.368 * ud[0]
tau37 = td[np.argmax(ud <= level37)]

# Наклон прямой ln U(t) при разрядке, только где U > 1 В
k, b = np.polyfit(td[ud > 1], np.log(ud[ud > 1]), 1)
tau_ln = -1 / k

print(f"Уровень 63 %, зарядка:  tau = {tau63:.2f} с")
print(f"Уровень 37 %, разрядка: tau = {tau37:.2f} с")
print(f"МНК, зарядка:           tau = {tau_fit_c:.2f} с (A = {A:.3f} В)")
print(f"МНК, разрядка:          tau = {tau_fit_d:.2f} с")
print(f"Наклон ln U, разрядка:  tau = {tau_ln:.2f} с")

taus = [tau63, tau37, tau_fit_c, tau_fit_d]
n = len(taus)
mean = sum(taus) / n
sigma = math.sqrt(sum((x - mean) ** 2 for x in taus) / (n * (n - 1)))
print(f"Среднее: tau = {mean:.2f} ± {sigma:.2f} с")
