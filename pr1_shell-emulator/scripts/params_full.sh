#!/bin/sh
cd "$(dirname "$0")/.." || exit 1
echo "1) --vfs и --script"
python3 src/main.py --vfs build/vfs/multi.zip --script scripts/emu/stage2.txt
echo "2) Параметры в обратном порядке"
python3 src/main.py --script scripts/emu/stage2.txt --vfs build/vfs/multi.zip
echo "3) Полный (абсолютный) путь к скрипту"
python3 src/main.py --script "$(pwd)/scripts/emu/stage2.txt"