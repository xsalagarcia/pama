from tkinter import ttk, messagebox
import tkinter as tk

from pama import tkinter_UI
from pama.exceptions.service import ServiceError
from pama.models.account import Account
from pama.service import account as service
from pama.tkinter_UI.validators import validators


class NewAccountDialog(tk.Toplevel):
    """
    Toplevel dialog for creating a new account.
    """
    def __init__(self, parent, title="New Account", account: None | Account = None, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.result: None | Account = None
        self.title(title)
        self.resizable(False, False)
        self.transient(parent)  # On top.
        self.grab_set()  # Modal.

        self._account_name = tk.StringVar()
        self._account_comments = tk.StringVar()
        self._account_url = tk.StringVar()
        self._account_pw = tk.StringVar()
        self._account_pw_c = tk.StringVar()
        self._is_pw_visible = tk.BooleanVar()

        if account is not None:
            try:
                pw = service.enc_dec.decrypt(account.passw).decode("utf-8")
            except ServiceError as e:
                tk.messagebox.showerror("Error", e.msg)
                self._cancel()
            self._account_name.set(account.name)
            self._account_comments.set(account.comments)
            self._account_url.set(account.url)
            self._account_pw.set(pw)
            self._account_pw_c.set(pw)

        frame_form = ttk.Frame(self, padding=tkinter_UI.PAD)
        frame_form.grid(row=2, column=2, sticky=(tk.E, tk.W), columnspan=2)

        ttk.Label(frame_form, text="Username").grid(row=0, column=0, padx=tkinter_UI.PAD, pady=tkinter_UI.PAD)
        ttk.Entry(frame_form, textvariable=self._account_name, validate="all",
                  validatecommand=validators["account name"]
                  ).grid(row=0, column=1, padx=tkinter_UI.PAD, pady=tkinter_UI.PAD)

        ttk.Label(frame_form, text="Comments").grid(row=1, column=0, padx=tkinter_UI.PAD, pady=tkinter_UI.PAD)
        ttk.Entry(frame_form, textvariable=self._account_comments, validate="all",
                  validatecommand=validators["account comments"]
                  ).grid(row=1, column=1, padx=tkinter_UI.PAD, pady=tkinter_UI.PAD)

        ttk.Label(frame_form, text="URL").grid(row=2, column=0, padx=tkinter_UI.PAD, pady=tkinter_UI.PAD)
        ttk.Entry(frame_form, textvariable=self._account_url, validate="all",
                  validatecommand=validators["account url"]
                  ).grid(row=2, column=1, padx=tkinter_UI.PAD, pady=tkinter_UI.PAD)

        ttk.Label(frame_form, text="Password").grid(row=3, column=0, padx=tkinter_UI.PAD, pady=tkinter_UI.PAD)
        self._pw_entry = ttk.Entry(frame_form, textvariable=self._account_pw, show="*")
        self._pw_entry.grid(row=3, column=1, padx=tkinter_UI.PAD, pady=tkinter_UI.PAD)

        ttk.Label(frame_form, text="Confirm PW").grid(row=4, column=0, padx=tkinter_UI.PAD, pady=tkinter_UI.PAD)
        self._pw_entry_2 = ttk.Entry(frame_form, textvariable=self._account_pw_c, show="*")
        self._pw_entry_2.grid(row=4, column=1, padx=tkinter_UI.PAD, pady=tkinter_UI.PAD)

        ttk.Button(frame_form, text="Random PW").grid(row=5, column=0, padx=tkinter_UI.PAD, pady=tkinter_UI.PAD)
        ttk.Checkbutton(frame_form, variable=self._is_pw_visible, offvalue=False, onvalue=True, text="Show PW",
                        command=self._show_pw
                        ).grid(row=5, column=1, padx=tkinter_UI.PAD, pady=tkinter_UI.PAD)

        frame_buttons = ttk.Frame(self, padding=tkinter_UI.PAD)
        frame_buttons.grid(row=3, column=2, sticky=(tk.E, tk.W), columnspan=2)

        ttk.Button(frame_buttons, text="OK", command=self._ok).grid(row=0, column=0, padx=tkinter_UI.PAD,
                                                                    pady=tkinter_UI.PAD, sticky=(tk.E, tk.W))
        ttk.Button(frame_buttons, text="Cancel").grid(row=0, column=1, padx=tkinter_UI.PAD, pady=tkinter_UI.PAD,
                                                      sticky=(tk.E, tk.W))

        self.protocol("WM_DELETE_WINDOW", self._cancel)

    def _cancel(self):
        self.result = None
        self.destroy()

    def _ok(self):
        if self._account_pw.get() != self._account_pw_c.get():
            tk.messagebox.showwarning(title="Error", message="Passwords don't match.", parent=self)
            return
        if self._account_name.get().strip() == "":
            tk.messagebox.showwarning(title="Error", message="Type some username.", parent=self)
            return

        self.result = Account(name=self._account_name.get(), comments=self._account_comments.get(),
                              url=self._account_url.get(), passw=self._account_pw.get().encode("utf-8"))

        self.destroy()

    def _show_pw(self):
        """
        Set pw fields visible or not.
        :return:
        """
        if self._is_pw_visible.get():
            self._pw_entry.config(show="")
            self._pw_entry_2.config(show="")
        else:
            self._pw_entry.config(show="*")
            self._pw_entry_2.config(show="*")
