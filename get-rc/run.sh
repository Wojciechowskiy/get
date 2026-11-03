#!/bin/bash
# Запуск всей работы одной командой: bash run.sh
cd "$(dirname "$0")"
python3 rc.py
python3 rc_plot.py
