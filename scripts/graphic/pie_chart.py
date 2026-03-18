import tkinter as tk
import math


class PieChart(tk.Canvas):
    """Camembert des dépenses par motif."""

    def __init__(self, master, data: list, **kwargs):
        """data : liste de (label, valeur, couleur_hex)"""
        super().__init__(master, bg="#1e1e2e", highlightthickness=0, **kwargs)
        self._data = data
        self.bind("<Configure>", lambda e: self._draw())

    def _draw(self):
        self.delete("all")
        w = self.winfo_width()
        h = self.winfo_height()
        if w < 10 or h < 10:
            return

        total = sum(v for _, v, _ in self._data)
        if total == 0:
            return

        cx, cy = w // 2, h // 2
        r      = min(cx, cy) - 20
        start  = -90.0

        for _, value, color in self._data:
            extent = (value / total) * 360
            self.create_arc(
                cx - r, cy - r, cx + r, cy + r,
                start=start, extent=extent,
                fill=color, outline="#1e1e2e", width=2,
            )
            mid_angle = math.radians(start + extent / 2)
            lx = cx + (r * 0.65) * math.cos(mid_angle)
            ly = cy + (r * 0.65) * math.sin(mid_angle)
            pct = value / total * 100
            if pct >= 5:
                self.create_text(
                    lx, ly,
                    text=f"{pct:.0f}%",
                    fill="white",
                    font=("Helvetica", 9, "bold"),
                )
            start += extent