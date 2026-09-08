import asyncio
import time
from tkinter import ttk, messagebox
import tkinter as tk

from pama import tkinter_UI
from pama.exceptions.service import ServiceError
from pama.models.account import Account
from pama.tkinter_UI.components.account import AccountFrame
from pama.tkinter_UI.components.ask_keymaster_dialog import AskKeymasterDialog
from pama.tkinter_UI.components.new_account_dialog import NewAccountDialog
from pama.service import account as service


class HeadOptions(ttk.Frame):
    """
    Window header containing some create button, set key button and search bar.
    """
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        buttons_frame = ttk.Frame(self)
        # 1. Place buttons in grid columns side-by-side
        ttk.Button(buttons_frame, text="New account",
                   command=self.show_new_account_dialog).grid(row=0, column=1, padx=tkinter_UI.PAD, pady=tkinter_UI.PAD)

        ttk.Button(buttons_frame, text="Set master key", command=lambda : AskKeymasterDialog(self)
                   ).grid(row=0, column=2, padx=tkinter_UI.PAD, pady=tkinter_UI.PAD)

        # 2. Add expandable empty columns on both sides to push buttons to the center
        buttons_frame.columnconfigure(0, weight=1)  # Left spacing
        buttons_frame.columnconfigure(3, weight=1)  # Right spacing
        buttons_frame.pack(side="top", fill="x", expand=True)

        # Search field.
        self.search_content: tk.StringVar = tk.StringVar()
        """Search content"""
        ttk.Entry(self, textvariable=self.search_content).pack(side="bottom", fill="x", expand=True, padx=tkinter_UI.PAD, pady=tkinter_UI.PAD)
        self.search_content.trace_add("write", self.filter_by_text)

    def filter_by_text(self, a, b, c):
        self.winfo_toplevel().filter_accounts(self.search_content.get())

    def show_new_account_dialog(self):
        new_account_dialog = NewAccountDialog(self)

        def insert_new_account_frame(account: Account):
            self.winfo_toplevel().create_and_insert_ordered_account_frame(account=account)

        def create_new_account():
            if new_account_dialog.result is not None:
                future = asyncio.run_coroutine_threadsafe(service.create_account(new_account_dialog.result), self.master.async_loop)
                future.add_done_callback(lambda f : insert_new_account_frame(f.result()) if f.result() else None)


            """
            if new_account_dialog.result is not None:
                try:
                    service.create_account(account=new_account_dialog.result)
                except ServiceError:
                    tk.messagebox.showerror(title="Error", message="Type some username.", parent=self)
            """
        new_account_dialog.bind("<Destroy>",
                                lambda event : create_new_account() if event.widget == new_account_dialog else None)

