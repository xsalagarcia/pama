from tkinter import ttk
import tkinter as tk

from pama import tkinter_UI
from pama.models.account import Account
from pama.tkinter_UI.validators import validators


class AccountFrame(ttk.Frame):
    def __init__(self, parent, account: Account, auto_pack: bool = True, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        self.account = account


        # Account fields
        fields_frame = ttk.Frame(self)

        fields_frame.pack(side="top")
        ttk.Label(fields_frame, text="name").grid(row=0, column=0, sticky=tk.E, padx=tkinter_UI.PAD, pady=tkinter_UI.PAD)
        self.name_variable = tk.StringVar(value=account.name)
        ttk.Entry(fields_frame, textvariable=self.name_variable,
                  validate="all",
                  validatecommand=validators["account name"]
                  ).grid(row=0, column=1, padx=tkinter_UI.PAD, pady=tkinter_UI.PAD)

        ttk.Label(fields_frame, text="Comments").grid(row=1, column=0, sticky=tk.E, padx=tkinter_UI.PAD, pady=tkinter_UI.PAD)
        self.comments_variable = tk.StringVar(value=account.comments)
        ttk.Entry(fields_frame, textvariable=self.comments_variable,
                  validate="all",
                  validatecommand=validators["account comments"]
                  ).grid(row=1, column=1, padx=tkinter_UI.PAD, pady=tkinter_UI.PAD)

        ttk.Label(fields_frame, text="URL").grid(row=3, column=0, sticky=tk.E, padx=tkinter_UI.PAD, pady=tkinter_UI.PAD)
        self.url_variable = tk.StringVar(value=account.url)
        ttk.Entry(fields_frame, textvariable=self.url_variable,
                  validate="all",
                  validatecommand=validators["account url"]
                  ).grid(row=3, column=1, padx=tkinter_UI.PAD, pady=tkinter_UI.PAD)


        # Component buttons
        buttons_frame = ttk.Frame(self)
        buttons_frame.pack(side="top")
        ttk.Button(buttons_frame, text="Copy PW").grid(row=0, column=1, padx=tkinter_UI.PAD, pady=tkinter_UI.PAD)
        ttk.Button(buttons_frame, text="Show PW").grid(row=0, column=2, padx=tkinter_UI.PAD, pady=tkinter_UI.PAD)

        ttk.Button(self, text="Delete account").pack(side="top", padx=tkinter_UI.PAD, pady=tkinter_UI.PAD)

        ttk.Separator(self).pack(fill="x")

        if auto_pack:
            self.pack()

    def filter_with(self, filter: str):
        """
        Show or not the component.
        :param filter:
        :return:
        """
        if filter not in self.account.name and filter not in self.account.comments and filter not in self.account.url:
            self.pack_forget()
        else:
            self.pack()
