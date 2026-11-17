# ЛР1. Расход затопленной струи

| Файл | Зачем | Запуск |
| --- | --- | --- |
| `jetFunctions.py` | функции АЦП и шагового двигателя (стартовый набор) | — |
| `jetMover.py` | двигать трубку Пито вручную | `python3 jetMover.py` |
| `jetCheck.py` | проверка датчика давления, если АЦП читает нули | `python3 jetCheck.py` |
| `jetMeasure.py` | снять профиль или калибровку | `python3 jetMeasure.py "00 mm.txt" 40` |
| `quickPlot.py` | быстро проверить записанный файл | `python3 quickPlot.py "00 mm.txt"` |
| `jetProcessing.py` | обработка: скорость, расход, графики | `python3 jetProcessing.py` |
| `Пример данных/` | данные для проверки обработки | — |

Перед работой (после каждого включения Raspberry Pi):

```bash
raspi-gpio set 9 a0
raspi-gpio set 10 a0
raspi-gpio set 11 a0
```

Калибровка: `python3 jetMeasure.py "00 Pa.txt" 50 0` (третий параметр 0 — трубка стоит на месте).

Сечения: 0–20 мм — 40 точек, 30–50 мм — 60 точек, 60–80 мм — 75 точек.
