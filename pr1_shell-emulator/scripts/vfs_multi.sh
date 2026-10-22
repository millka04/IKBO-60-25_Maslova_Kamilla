#!/bin/sh
# Запуск эмулятора: VFS с несколькими файлами.
cd "$(dirname "$0")/.." || exit 1
python3 scripts/make_vfs.py
python3 src/main.py --vfs build/vfs/multi.zip --script scripts/emu/stage3.txt