#!/bin/sh
cd "$(dirname "$0")/.." || exit 1
echo "1) Запуск без параметров"
python3 src/main.py
echo "2) Только --vfs"
python3 src/main.py --vfs build/vfs/multi.zip
echo "3) Только --script"
python3 src/main.py --script scripts/emu/stage2.txt