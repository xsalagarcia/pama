from tkinter import ttk
import tkinter as tk

from pama import tkinter_UI


class HeadOptions(ttk.Frame):
    """
    Window header containing some create button, set key button and search bar.
    """
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        buttons_frame = ttk.Frame(self)
        # 1. Place buttons in grid columns side-by-side
        ttk.Button(buttons_frame, text="New account").grid(row=0, column=1, padx=tkinter_UI.PAD, pady=tkinter_UI.PAD)

        ttk.Button(buttons_frame, text="Set master key").grid(row=0, column=2, padx=tkinter_UI.PAD, pady=tkinter_UI.PAD)

        # 2. Add expandable empty columns on both sides to push buttons to the center
        buttons_frame.columnconfigure(0, weight=1)  # Left spacing
        buttons_frame.columnconfigure(3, weight=1)  # Right spacing
        buttons_frame.pack(side="top", fill="x", expand=True)

        # Search field.
        self.search_content: tk.StringVar = tk.StringVar()
        """Search content"""
        ttk.Entry(self, textvariable=self.search_content).pack(side="bottom", fill="x", expand=True, padx=tkinter_UI.PAD, pady=tkinter_UI.PAD)
