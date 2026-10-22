#!/bin/sh
# Ошибки загрузки VFS: файла нет и файл не является ZIP-архивом.
cd "$(dirname "$0")/.." || exit 1
python3 scripts/make_vfs.py
echo "1) Несуществующий архив"
python3 src/main.py --vfs build/vfs/no_such.zip --script scripts/emu/stage3.txt
echo "2) Повреждённый архив"
python3 src/main.py --vfs build/vfs/broken.zip --script scripts/emu/stage3.txt