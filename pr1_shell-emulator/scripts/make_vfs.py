"""Создаёт тестовые ZIP-архивы VFS в папке build/vfs.

Архивы не хранятся в репозитории, а создаются этим скриптом.
"""

import os
import zipfile

OUT_DIR = os.path.join("build", "vfs")

MINIMAL = {
    "readme.txt": b"Minimal VFS: one file.\n",
}

MULTI = {
    "readme.txt": b"VFS with several files.\n",
    "notes.txt": b"first line\nsecond line\nthird line\n",
    "todo.txt": b"1. learn git\n2. write emulator\n",
    "data/numbers.txt": b"1\n2\n3\n",
}

DEEP = {
    "readme.txt": b"VFS with 3+ levels.\n",
    "home/user/notes.txt": "".join(
        f"line {number}\n" for number in range(1, 16)).encode(),
    "home/user/docs/report.txt": b"Report\nPage 1\nPage 2\n",
    "home/user/docs/old/draft.txt": b"old draft\n",
    "home/guest/hello.txt": b"hello, guest\n",
    "etc/config.ini": b"[main]\nmode=test\n",
    "bin/tool.bin": bytes(range(256)),
    "tmp/": b"",
}


def build_zip(name, files):
    """Создаёт архив name.zip из словаря {путь: содержимое}."""
    path = os.path.join(OUT_DIR, name + ".zip")
    with zipfile.ZipFile(path, "w") as archive:
        for inner_path, data in files.items():
            archive.writestr(inner_path, data)
    print("создан", path)


def main():
    """Создаёт все тестовые архивы и один повреждённый файл."""
    os.makedirs(OUT_DIR, exist_ok=True)
    build_zip("minimal", MINIMAL)
    build_zip("multi", MULTI)
    build_zip("deep", DEEP)
    broken = os.path.join(OUT_DIR, "broken.zip")
    with open(broken, "w", encoding="utf-8") as file:
        file.write("это не ZIP-архив\n")
    print("создан", broken)


if __name__ == "__main__":
    main()