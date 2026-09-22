import tkinter as tk
from tkinter import ttk

from pama import tkinter_UI
from pama.utils.generator import password_generator


class PasswordGeneratorDialog(tk.Toplevel):
    def __init__(self, parent, title: str="Password generator", *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        self.result: None | str = None

        self.title(title)
        self.resizable(False, False)
        self.transient(parent)  # On top.
        self.grab_set()  # Modal.

        frame_form = ttk.Frame(self, padding=tkinter_UI.PAD)
        tk.Label(frame_form, text="Password length").pack()
        self._length = tk.IntVar(value=11)
        ttk.Scale(frame_form, from_=8, to=50, orient="horizontal", variable=self._length, length=200,
                  command=lambda val: self._length.set(round(float(val)))).pack()
        tk.Label(frame_form, textvariable=self._length).pack()

        frame_form.grid(row=2, column=2, sticky=(tk.E, tk.W), columnspan=2)

        self._include_numbers = tk.BooleanVar(value=True)
        ttk.Checkbutton(frame_form, text="Include numbers", variable=self._include_numbers).pack(anchor="w")

        self._include_letters = tk.BooleanVar(value=True)
        ttk.Checkbutton(frame_form, text="Include letters", variable=self._include_letters).pack(anchor="w")

        self._include_capital_letters = tk.BooleanVar(value=True)
        ttk.Checkbutton(frame_form, text="Include capital letters", variable=self._include_capital_letters).pack(anchor="w")

        self._include_special_chars = tk.BooleanVar(value=True)
        ttk.Checkbutton(frame_form, text="Include special chars", variable=self._include_special_chars).pack(anchor="w")

        frame_buttons = ttk.Frame(self, padding=tkinter_UI.PAD)
        frame_buttons.grid(row=3, column=2, sticky=(tk.E, tk.W), columnspan=2)

        ttk.Button(frame_buttons, text="OK", command=self._ok).grid(row=0, column=0, padx=tkinter_UI.PAD,
                                                                    pady=tkinter_UI.PAD, sticky=(tk.E, tk.W))
        ttk.Button(frame_buttons, text="Cancel", command=self._cancel).grid(row=0, column=1, padx=tkinter_UI.PAD,
                                                                            pady=tkinter_UI.PAD, sticky=(tk.E, tk.W))

        self.protocol("WM_DELETE_WINDOW", self._cancel)

    def _ok(self):
        self.result = password_generator(length=self._length.get(),
                                         numbers=self._include_numbers.get(),
                                         special_chars=self._include_special_chars.get(),
                                         lower_case=self._include_letters.get(),
                                         upper_case=self._include_letters.get())
        self.destroy()

    def _cancel(self):
        self.destroy()