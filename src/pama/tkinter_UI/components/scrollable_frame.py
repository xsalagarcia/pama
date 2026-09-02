import tkinter as tk
from tkinter import ttk

class ScrollableFrame(tk.Canvas):
    """
    Components should be inserted into ScrollableFrame.scrollable_content
    """
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, highlightthickness=0, *args, **kwargs)

        # 1. Create vertical scrollbar
        self.scrollbar = ttk.Scrollbar(parent, orient="vertical", command=self.yview)
        self.configure(yscrollcommand=self.scrollbar.set)

        # 2. Create inner frame to hold the actual widgets
        self.scrollable_content = ttk.Frame(self)
        self.window_id = self.create_window((0, 0), window=self.scrollable_content, anchor="nw")

        # 3. Dynamic scroll region update when content changes
        self.scrollable_content.bind(
            "<Configure>",
            lambda e: self.configure(scrollregion=self.bbox("all"))
        )

        # 4. Auto-size inner frame width to match canvas width
        self.bind("<Configure>", self._on_canvas_configure)

        # 5. Enable mouse wheel scrolling
        self.bind_all("<MouseWheel>", self._on_mousewheel)

    def _on_canvas_configure(self, event):
        """Adjusts inner frame width to match the canvas window width."""
        self.itemconfig(self.window_id, width=event.width)

    def _on_mousewheel(self, event):
        """Handles cross-platform mousewheel scrolling."""
        self.yview_scroll(int(-1 * (event.delta / 120)), "units")

    def pack(self, **kwargs):
        """Helper to auto-pack both canvas and scrollbar together."""
        self.scrollbar.pack(side="right", fill="y")
        super().pack(side="left", fill="both", expand=True, **kwargs)

    def grid(self, **kwargs):
        """Helper to auto-grid both canvas and scrollbar together."""
        self.scrollbar.grid(row=kwargs.get("row", 0), column=kwargs.get("column", 0) + 1, sticky="ns")
        super().grid(side="left", fill="both", expand=True, **kwargs)