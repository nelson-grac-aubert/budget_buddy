
import tkinter as tk
 
 
MONTHLY_BALANCE = {
    "Jan": 45000,
    "Fév": 47500,
    "Mar": 51200,
    "Avr": 49800,
    "Mai": 62970,
}
 
 
class BalanceChart(tk.Canvas):
    """Graphique de solde en courbe lissée style area chart."""
 
    ACCENT = "#7c3aed"
    MONTHS = list(MONTHLY_BALANCE.keys())
    VALUES = list(MONTHLY_BALANCE.values())
 
    def __init__(self, master, **kwargs):
        super().__init__(master, bg="#1e1e2e", highlightthickness=0, **kwargs)
        self.bind("<Configure>", lambda e: self._draw())
 
    def _draw(self):
        self.delete("all")
        w = self.winfo_width()
        h = self.winfo_height()
        if w < 10 or h < 10:
            return
 
        pad_x, pad_top, pad_bot = 30, 20, 40
        values = self.VALUES
        n      = len(values)
        vmin   = min(values) * 0.92
        vmax   = max(values) * 1.05
 
        def to_x(i):
            return pad_x + i * (w - 2 * pad_x) / (n - 1)
 
        def to_y(v):
            return pad_top + (1 - (v - vmin) / (vmax - vmin)) * (h - pad_top - pad_bot)
 
        pts = [(to_x(i), to_y(v)) for i, v in enumerate(values)]
 
        # Aire dégradée
        fill_pts = pts + [(pts[-1][0], h - pad_bot), (pts[0][0], h - pad_bot)]
        self.create_polygon(fill_pts, fill="#3b1a6e", outline="")
 
        mid_pts  = [(x, y + (h - pad_bot - y) * 0.3) for x, y in pts]
        mid_fill = mid_pts + [(pts[-1][0], h - pad_bot), (pts[0][0], h - pad_bot)]
        self.create_polygon(mid_fill, fill="#4c1d95", outline="")
 
        # Courbe lissée
        smooth = []
        for x, y in pts:
            smooth.extend([x, y])
        self.create_line(smooth, fill=self.ACCENT, width=3, smooth=True, splinesteps=64)
 
        # Dernier point
        lx, ly = pts[-1]
        r = 6
        self.create_oval(lx - r, ly - r, lx + r, ly + r,
                         fill=self.ACCENT, outline="white", width=2)
 
        # Labels des mois
        for i, (month, (x, _)) in enumerate(zip(self.MONTHS, pts)):
            is_last = (i == n - 1)
            color   = "white" if is_last else "#6b7280"
            weight  = "bold"  if is_last else "normal"
            self.create_text(x, h - pad_bot + 14, text=month,
                             fill=color, font=("Helvetica", 10, weight))