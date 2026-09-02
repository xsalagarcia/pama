import asyncio
import threading
import tkinter as tk
from tkinter import ttk

from pama.models.account import Account
from pama.tkinter_UI import validators
from pama.tkinter_UI.components.account import AccountFrame
from pama.tkinter_UI.components.head_options import HeadOptions
from pama.tkinter_UI.components.scrollable_frame import ScrollableFrame


class TkinterApp:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("PaMa")

        head_options = HeadOptions(self.root)
        head_options.pack(side="top", fill="x", anchor=tk.CENTER)

        scrollable = ScrollableFrame(self.root)

        test_accounts = [Account(name=f"{i}test", comments=f"{i}test comments", url=f"{i}test url", passw=b"") for i in range(1, 20)]
        self.afs = [AccountFrame(scrollable.scrollable_content, account) for account in test_accounts]
        for af in self.afs:
            af.pack()
        scrollable.pack()

        head_options.search_content.trace_add(mode="write",
                                              callback=lambda a, b, c: self.filter_accounts(head_options.search_content.get()) )


        self.async_tasks_queue = asyncio.Queue()
        """Queue for async tasks"""

        # Daemon for io-bound and cpu-bound tasks.
        self.loop = asyncio.new_event_loop()
        """Event loop for async tasks"""
        self.daemon_for_async_tasks = threading.Thread(target=self.async_worker_target, daemon=True)
        """Daemon worker thread for async tasks"""
        self.daemon_for_async_tasks.start()

    def async_worker_target(self):
        """
        Worker target for async tasks. Set self.loop as the own event loop for the daemon worker thread.
        :return:
        """
        asyncio.set_event_loop(self.loop)
        self.loop.run_forever()

    def on_close(self):
        # If a ProcessPool is set, it should be shutdown here.
        self.root.destroy()

    def filter_accounts(self, filter):
        for af in self.afs:
            af.filter_with(filter)


if __name__ == '__main__':
    root = tk.Tk()
    validators.create_validators(root)
    app = TkinterApp(root)
    root.mainloop()