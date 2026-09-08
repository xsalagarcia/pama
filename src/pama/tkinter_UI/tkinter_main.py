import asyncio
import threading
import tkinter as tk
from typing import Sequence

from pama.models.account import Account
from pama.tkinter_UI import validators
from pama.tkinter_UI.components.account import AccountFrame
from pama.tkinter_UI.components.ask_keymaster_dialog import AskKeymasterDialog
from pama.tkinter_UI.components.head_options import HeadOptions
from pama.tkinter_UI.components.scrollable_frame import ScrollableFrame
from pama.data.engine import create_db_and_tables
from pama.service import account as service
from pama.utils import sorted_list_ops


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

        # Register the window close handler
        self.protocol("WM_DELETE_WINDOW", self.on_close)

        head_options = HeadOptions(self)
        head_options.pack(side="top", fill="x", anchor=tk.CENTER)

        self.accounts_scrollable_frame = ScrollableFrame(self)
        self.accounts_scrollable_frame.pack()


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

    def create_and_insert_ordered_account_frame(self, account: Account):
        af = AccountFrame(self.accounts_scrollable_frame.scrollable_content, account=account)

    def _insert_account_frame_ordered(self, af: AccountFrame):
        afs_list = self.get_account_frames_list()
        predecessor = sorted_list_ops.find_predecessor(sorted_list=afs_list, element=af)
        if predecessor is not None:
            af.pack(after=predecessor)
        elif len(afs_list) > 0:
            af.pack(before=afs_list[0])
        else:
            af.pack()

    def fill_accounts(self, accounts: Sequence[Account]):
        [AccountFrame(self.accounts_scrollable_frame.scrollable_content, account).pack() for account in accounts]


    def get_account_frames_list(self) -> list[AccountFrame]:
        return [a_f for a_f in self.accounts_scrollable_frame.scrollable_content.winfo_children()]

    def remove_account(self, account_frame: AccountFrame):

        def remove_account_from_ui(f: asyncio.Future):
            if f.result() and sorted_list_ops.delete(self.get_account_frames_list(), account_frame) is not None:
                    account_frame.destroy()

        future = asyncio.run_coroutine_threadsafe(service.remove_account(account_id=account_frame.account.id), self.async_loop)
        future.add_done_callback(fn=lambda f : remove_account_from_ui(f))

    def reorder_account(self, af: AccountFrame):
        self._insert_account_frame_ordered(af)

    def _on_visible(self, event):
        """
        Called when self is visible the first time.
        :param event:
        :return:
        """
        self.unbind("<Visibility>")
        AskKeymasterDialog(self)

    def async_worker_target(self):
        """
        Worker target for async tasks. Set self.loop as the own event loop for the daemon worker thread.
        :return:
        """
        asyncio.set_event_loop(self.async_loop)
        self.async_loop.run_forever()

    def on_close(self):
        """
        Called when the app is closed.
        Gracefully wait for remaining async tasks to complete.
        :return:
        """

        # If a ProcessPool is set, it should be shutdown here.


        async def _shutdown():
            """
            Await all running tasks to complete.
            :return:
            """
            async_tasks = [t for t in asyncio.all_tasks(self.async_loop) if t is not asyncio.current_task(self.async_loop)]
            if async_tasks:
                await asyncio.gather(*async_tasks, return_exceptions=True)

        future = asyncio.run_coroutine_threadsafe(_shutdown(), self.async_loop)
        try:
            future.result(timeout=10)
        except Exception as e:
            print(f"Error during async shutdown: {e}")
        finally:
            self.async_loop.call_soon_threadsafe(self.async_loop.stop)

        self.daemon_for_async_tasks.join(timeout=5)
        self.destroy()

    def filter_accounts(self, filter):
        for af in self.get_account_frames_list():
            af.filter_with(filter)

def main():
    app = TkinterAsyncApp()
    app.mainloop()

if __name__ == '__main__':
    main()

