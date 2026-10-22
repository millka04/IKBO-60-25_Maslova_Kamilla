#!/bin/sh
# Запуск эмулятора: минимальная VFS (один файл).
cd "$(dirname "$0")/.." || exit 1
python3 scripts/make_vfs.py
python3 src/main.py --vfs build/vfs/minimal.zip --script scripts/emu/stage3.txt