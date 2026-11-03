# График U(t) по файлу rc_data.csv и оценка постоянной времени tau = R*C.
# Запуск: python3 rc_plot.py
import matplotlib.pyplot as plt

FILE_NAME = "rc_data.csv"
CHARGE_TIME = 50          # с, столько же, сколько в rc.py

# Читаем файл
t = []
u = []
with open(FILE_NAME) as f:
    f.readline()                      # пропускаем заголовок
    for line in f:
        parts = line.strip().split(",")
        t.append(float(parts[0]))
        u.append(float(parts[1]))

# tau: время, за которое при зарядке напряжение доходит до 63% от размаха
u_min = min(u)
u_max = max(u)
level = u_min + 0.63 * (u_max - u_min)

tau = 0
for i in range(len(t)):
    if t[i] < CHARGE_TIME and u[i] >= level:
        tau = t[i]
        break

print(f"tau = {tau:.2f} с")

plt.plot(t, u, ".-", markersize=2)
plt.axhline(level, color="red", linestyle="--", label="63% от максимума")
plt.axvline(tau, color="green", linestyle="--", label=f"tau = {tau:.2f} с")
plt.title("Зарядка и разрядка конденсатора")
plt.xlabel("Время, с")
plt.ylabel("Напряжение на конденсаторе, В")
plt.legend()
plt.grid(True)
plt.savefig("rc_plot.png", dpi=150)
plt.show()
