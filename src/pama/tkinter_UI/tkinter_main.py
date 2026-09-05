import asyncio
import threading
import tkinter as tk
from tkinter import ttk
from typing import Sequence

from pama.models.account import Account
from pama.tkinter_UI import validators
from pama.tkinter_UI.components.account import AccountFrame
from pama.tkinter_UI.components.ask_keymaster_dialog import AskKeymasterDialog
from pama.tkinter_UI.components.head_options import HeadOptions
from pama.tkinter_UI.components.scrollable_frame import ScrollableFrame
from pama.data.engine import create_db_and_tables
from pama.service import account as service


class TkinterAsyncApp(tk.Tk):
    """
    Top level widget for tkinter application.

    Create db tables if not exists.

    Additional features include:

    - ``async_tasks_queue`` property for enqueueing async tasks.

    - ``async_loop`` An event loop that belongs to a daemon thread. Use like ``future = run_coroutine_threadsafe(coro, tkinter_async_app.async_loop)``
    """

    def __init__(self):
        super().__init__()

        self.async_tasks_queue = asyncio.Queue()
        """Queue for async tasks"""

        # Daemon for io-bound and cpu-bound tasks.
        self.async_loop = asyncio.new_event_loop()
        """Event loop for async tasks"""
        self.daemon_for_async_tasks = threading.Thread(target=self.async_worker_target, daemon=True)
        """Daemon worker thread for async tasks"""
        self.daemon_for_async_tasks.start()

        asyncio.run_coroutine_threadsafe(create_db_and_tables(), self.async_loop)


        validators.create_validators(self)
        self.title("PaMa")

        head_options = HeadOptions(self)
        head_options.pack(side="top", fill="x", anchor=tk.CENTER)

        self.accounts_scrollable_frame = ScrollableFrame(self)
        self.accounts_scrollable_frame.pack()

        self.afs = list[AccountFrame]
        """Contains AccountFrame widgets with accounts."""

        #test_accounts = [Account(name=f"{i}test", comments=f"{i}test comments", url=f"{i}test url", passw=b"") for i in range(1, 20)]
        #self.afs = [AccountFrame(scrollable.scrollable_content, account) for account in test_accounts]
        #for af in self.afs:
        #    af.pack()

        # Get accounts.
        future = asyncio.run_coroutine_threadsafe(service.search_account(), self.async_loop)
        future.add_done_callback(fn=lambda f : self.fill_accounts(f.result()))

        # Callback when user writes search bar.
        head_options.search_content.trace_add(mode="write",
                                              callback=lambda a, b, c: self.filter_accounts(head_options.search_content.get()) )

        # Set event when self is shown.
        self.bind("<Visibility>", lambda event: self._on_visible(event) if event.widget == self else False)

    def fill_accounts(self, accounts: Sequence[Account]):
        self.afs = [AccountFrame(self.accounts_scrollable_frame.scrollable_content, account) for account in accounts]
        for af in self.afs:
           af.pack()

    def _on_visible(self, event):
        """
        Called when self is visible.
        :param event:
        :return:
        """
        AskKeymasterDialog(self)

    def async_worker_target(self):
        """
        Worker target for async tasks. Set self.loop as the own event loop for the daemon worker thread.
        :return:
        """
        asyncio.set_event_loop(self.async_loop)
        self.async_loop.run_forever()

    def on_close(self):
        # If a ProcessPool is set, it should be shutdown here.
        self.destroy()

    def filter_accounts(self, filter):
        for af in self.afs:
            af.filter_with(filter)


if __name__ == '__main__':
    #root = tk.Tk()
    #validators.create_validators(root)

    app = TkinterAsyncApp()
    app.mainloop()