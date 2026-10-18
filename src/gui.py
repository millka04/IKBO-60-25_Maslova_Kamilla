"""Графический интерфейс эмулятора на библиотеке tkinter."""

import tkinter as tk
from tkinter import scrolledtext

from errors import ShellError

FONT = ("Menlo", 13)


class App:
    """Окно эмулятора: область вывода и строка ввода команд."""

    def __init__(self, shell):
        """Создаёт окно и все его элементы."""
        self.shell = shell
        self.root = tk.Tk()
        self.root.title(shell.title())
        self.root.geometry("800x500")
        self.output = scrolledtext.ScrolledText(self.root, font=FONT, state="disabled", wrap="word")
        self.output.pack(fill="both", expand=True)
        bottom = tk.Frame(self.root)
        bottom.pack(fill="x")
        self.prompt_label = tk.Label(bottom, text=shell.prompt(), font=FONT)
        self.prompt_label.pack(side="left")
        self.entry = tk.Entry(bottom, font=FONT)
        self.entry.pack(side="left", fill="x", expand=True)
        self.entry.bind("<Return>", self.on_enter)
        self.entry.focus_set()

    def write(self, text):
        """Добавляет текст в область вывода."""
        if not text:
            return
        self.output.configure(state="normal")
        self.output.insert("end", text + "\n")
        self.output.see("end")
        self.output.configure(state="disabled")

    def run_line(self, line):
        """Показывает строку как ввод пользователя и выполняет её.

        Возвращает True, если команда выполнилась без ошибки.
        """
        self.write(self.shell.prompt() + line)
        success = True
        try:
            self.write(self.shell.execute(line))
        except ShellError as error:
            self.write(f"Ошибка: {error}")
            success = False
        if not self.shell.running:
            self.root.destroy()
            return success
        self.prompt_label.configure(text=self.shell.prompt())
        return success

    def on_enter(self, event):
        """Обрабатывает нажатие Enter в строке ввода."""
        line = self.entry.get()
        self.entry.delete(0, "end")
        self.run_line(line)

    def start(self):
        """Запускает главный цикл окна."""
        self.root.mainloop()