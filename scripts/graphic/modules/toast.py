import tkinter as tk
import customtkinter as ctk


class Toast(ctk.CTkToplevel):
    """Notification flottante qui disparaît automatiquement après 4 s.

    Les toasts s'empilent verticalement à partir d'une position d'ancrage
    transmise à la construction (anchor_x, anchor_y). Chaque nouveau toast
    s'affiche sous le précédent, sans jamais se superposer.
    """

    _WIDTH = 340  # largeur fixe (px)
    _GAP   = 6    # espace entre deux toasts empilés (px)

    _stack: list = []

    def __init__(self, master, title: str, message: str, kind: str = "success",
                 anchor_x: int = None, anchor_y: int = None):
        super().__init__(master)
        self.overrideredirect(True)
        self.attributes("-topmost", True)
        self.resizable(False, False)

        self._anchor_x = anchor_x
        self._anchor_y = anchor_y

        palette = {
            "success": ("#14532d", "#22c55e"),
            "warning": ("#78350f", "#f59e0b"),
            "error":   ("#7f1d1d", "#ef4444"),
            "info":    ("#1e3a5f", "#3b82f6"),
        }
        bg, accent = palette.get(kind, palette["success"])

        self.geometry(f"{self._WIDTH}x1")
        self.configure(bg=bg)

        outer = tk.Frame(self, bg=accent)
        outer.pack(fill="both", expand=True, padx=1, pady=1)

        inner = tk.Frame(outer, bg=bg)
        inner.pack(fill="both", expand=True)

        tk.Frame(inner, bg=accent, width=4).pack(side="left", fill="y")

        tk.Button(
            inner, text="✕",
            bg=bg, fg="#9ca3af",
            activebackground=bg, activeforeground="#d1d5db",
            relief="flat", bd=0,
            font=("Helvetica", 10),
            cursor="hand2",
            command=self._close,
        ).pack(side="right", padx=(0, 8), anchor="center")

        text_area = tk.Frame(inner, bg=bg)
        text_area.pack(side="left", fill="both", expand=True, padx=(10, 0), pady=8)

        _wrap = self._WIDTH - 4 - 10 - 36

        tk.Label(
            text_area, text=title,
            bg=bg, fg=accent,
            font=("Helvetica", 11, "bold"),
            anchor="w", justify="left",
            wraplength=_wrap,
        ).pack(anchor="w", fill="x")

        tk.Label(
            text_area, text=message,
            bg=bg, fg="#d1d5db",
            font=("Helvetica", 10),
            anchor="w", justify="left",
            wraplength=_wrap,
        ).pack(anchor="w", fill="x", pady=(2, 0))

        self.update_idletasks()
        self._h = self.winfo_reqheight()
        Toast._stack.append(self)
        self._position()
        self._job = self.after(4000, self._close)

    def _position(self):
        x = self._anchor_x if self._anchor_x is not None else (
            self.winfo_screenwidth() - self._WIDTH - 20
        )
        y = self._anchor_y if self._anchor_y is not None else (
            self.winfo_screenheight() - 60
        )
        for toast in Toast._stack:
            if toast is self:
                break
            y += toast._h + self._GAP

        self.geometry(f"{self._WIDTH}x{self._h}+{x}+{y}")

    def _close(self):
        try:
            self.after_cancel(self._job)
        except Exception:
            pass
        if self in Toast._stack:
            idx = Toast._stack.index(self)
            Toast._stack.remove(self)
            for toast in Toast._stack[idx:]:
                toast._position()
        self.destroy()