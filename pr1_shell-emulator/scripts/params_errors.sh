#!/bin/sh
cd "$(dirname "$0")/.." || exit 1
echo "1) Справка по параметрам (окно не откроется)"
python3 src/main.py --help
echo "2) Неизвестный параметр (окно не откроется, будет ошибка)"
python3 src/main.py --color red
echo "3) Несуществующий стартовый скрипт (в окне будет ошибка)"
python3 src/main.py --script scripts/emu/no_such_script.txt