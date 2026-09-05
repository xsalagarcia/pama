import hashlib
import tkinter as tk
from tkinter import ttk

from pama import tkinter_UI
from pama.service import account as service
from pama.settings.settings import config


class AskKeymasterDialog(tk.Toplevel):
    """
    TopLevel dialog for ask keymaster.
    """

    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.title("Type master key")
        self.resizable(False, False)
        self.transient(parent)  # On top.
        self.grab_set()  # Modal.

        self._key_master = tk.StringVar()

        frame_form = ttk.Frame(self, padding=tkinter_UI.PAD)
        frame_form.pack()
        ttk.Label(frame_form, text="Master key"
                  ).grid(row=0, column=0, padx=tkinter_UI.PAD, pady=tkinter_UI.PAD)
        km_entry = ttk.Entry(frame_form, textvariable=self._key_master, show="*")
        km_entry.grid(row=0, column=1, padx=tkinter_UI.PAD, pady=tkinter_UI.PAD)
        km_entry.bind("<Return>", self._ok)

        ttk.Button(self, text="OK", command=self._ok).pack(side="top", padx=tkinter_UI.PAD, pady=tkinter_UI.PAD)

    def _ok(self, event=None):
        service.set_encoder(key=hashlib.sha256(self._key_master.get().encode("utf-8")).digest(), salt=config.salt)
        self.destroy()






