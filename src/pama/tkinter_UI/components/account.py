import asyncio
from tkinter import ttk
import tkinter as tk

from pama import tkinter_UI
from pama.models.account import Account, AccountUpdate
from pama.tkinter_UI.components.new_account_dialog import NewAccountDialog
from pama.tkinter_UI.validators import validators
from pama.service import account as service


class AccountFrame(ttk.Frame):
    """
    Widget representing an account.
    """

    def __init__(self, parent, account: Account, auto_pack: bool = True, *args, **kwargs):
        """

        :param parent:
        :param account: Account data.
        :param auto_pack: If true, automatically pack the component. Defaults to True.
        :param args:
        :param kwargs:
        """
        super().__init__(parent, *args, **kwargs)

        self.account = account
        """Account data."""


        # Account fields
        fields_frame = ttk.Frame(self)

        fields_frame.pack(side="top")
        ttk.Label(fields_frame, text="name").grid(row=0, column=0, sticky=tk.E, padx=tkinter_UI.PAD, pady=tkinter_UI.PAD)
        self.name_variable = tk.StringVar(value=account.name)
        ttk.Entry(fields_frame, textvariable=self.name_variable, state="readonly",
                  validate="all",
                  validatecommand=validators["account name"]
                  ).grid(row=0, column=1, padx=tkinter_UI.PAD, pady=tkinter_UI.PAD)

        ttk.Label(fields_frame, text="Comments").grid(row=1, column=0, sticky=tk.E, padx=tkinter_UI.PAD, pady=tkinter_UI.PAD)
        self.comments_variable = tk.StringVar(value=account.comments)
        ttk.Entry(fields_frame, textvariable=self.comments_variable, state="readonly",
                  validate="all",
                  validatecommand=validators["account comments"]
                  ).grid(row=1, column=1, padx=tkinter_UI.PAD, pady=tkinter_UI.PAD)

        ttk.Label(fields_frame, text="URL").grid(row=3, column=0, sticky=tk.E, padx=tkinter_UI.PAD, pady=tkinter_UI.PAD)
        self.url_variable = tk.StringVar(value=account.url)
        ttk.Entry(fields_frame, textvariable=self.url_variable, state="readonly",
                  validate="all",
                  validatecommand=validators["account url"]
                  ).grid(row=3, column=1, padx=tkinter_UI.PAD, pady=tkinter_UI.PAD)

        self.last_updated_variable = tk.StringVar(value=account.last_updated.isoformat(sep=" "))
        ttk.Label(fields_frame, text="Last updated"
                  ).grid(row=4, column=0, sticky=tk.E, padx=tkinter_UI.PAD, pady=tkinter_UI.PAD)
        ttk.Label(fields_frame, textvariable=self.last_updated_variable
                  ).grid(row=4, column=1, sticky=tk.E, padx=tkinter_UI.PAD, pady=tkinter_UI.PAD)


        # Component buttons
        buttons_frame = ttk.Frame(self)
        buttons_frame.pack(side="top")
        ttk.Button(buttons_frame, text="Copy PW", command=self._copy_pw
                   ).grid(row=0, column=1, padx=tkinter_UI.PAD, pady=tkinter_UI.PAD)
        ttk.Button(buttons_frame, text="Show PW").grid(row=0, column=2, padx=tkinter_UI.PAD, pady=tkinter_UI.PAD)
        ttk.Button(buttons_frame, text="Edit", command=self._edit).grid(row=0, column=3, padx=tkinter_UI.PAD, pady=tkinter_UI.PAD)

        ttk.Button(self, text="Delete account").pack(side="top", padx=tkinter_UI.PAD, pady=tkinter_UI.PAD)

        ttk.Separator(self).pack(fill="x")

        if auto_pack:
            self.pack()

    def _edit(self):
        """
        Open modal dialog to edit account.
        :return:
        """
        nac = NewAccountDialog(self, title="Edit account", account=self.account)
        def update_account_at_database():
            if nac.result is not None and nac.result != self.account:
                future = asyncio.run_coroutine_threadsafe(
                    service.update_account(
                        account_update=AccountUpdate(id=self.account.id,
                                                     **nac.result.model_dump(exclude={"last_updated", "id"}))),
                    self.winfo_toplevel().async_loop)
                future.add_done_callback(lambda _: self.update_account(future.result()))

        nac.bind("<Destroy>", lambda event: update_account_at_database() if event.widget == nac else None)

    def update_account(self, updated_account: Account):
        if isinstance(updated_account, Account):
            self.account = updated_account
            self.name_variable.set(self.account.name)
            self.comments_variable.set(self.account.comments)
            self.url_variable.set(self.account.url)
            self.last_updated_variable.set(self.account.last_updated.isoformat(sep=" "))
        else:
            tk.messagebox.showerror(title="Error", message="Error updating account.")


    def _copy_pw(self):
        """
        Clear the clipboard. Copy pw to the clipboard.
        :return:
        """
        self.master.clipboard_clear()
        self.master.clipboard_append(service.enc_dec.decrypt(self.account.passw).decode("utf-8"))

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
