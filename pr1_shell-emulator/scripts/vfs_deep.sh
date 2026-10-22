#!/bin/sh
# Запуск эмулятора: VFS с 3+ уровнями папок.
cd "$(dirname "$0")/.." || exit 1
python3 scripts/make_vfs.py
python3 src/main.py --vfs build/vfs/deep.zip --script scripts/emu/stage3.txt