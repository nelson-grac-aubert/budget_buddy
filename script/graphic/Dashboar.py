import tkinter as tk
import customtkinter as ctk


# Données simulées : solde par mois (attenyion a remplacer par des données réelles de la database)
MONTHLY_BALANCE = {
    "Jan": 45000,
    "Fév": 47500,
    "Mar": 51200,
    "Avr": 49800,
    "Mai": 62970,
}

INCOME   = 5_200
EXPENSES = 3_180
BALANCE  = list(MONTHLY_BALANCE.values())[-1]

# 
class BalanceChart(tk.Canvas):
    """Graphique de solde en courbe lissée style area chart."""

    ACCENT   = "#7c3aed"   
    MONTHS   = list(MONTHLY_BALANCE.keys())
    VALUES   = list(MONTHLY_BALANCE.values())

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

        # ── Aire dégradée   #
        fill_pts = pts + [(pts[-1][0], h - pad_bot), (pts[0][0], h - pad_bot)]
        self.create_polygon(fill_pts, fill="#3b1a6e", outline="")

        # Deuxième couche plus claire pour donner du relief
        mid_pts = [(x, y + (h - pad_bot - y) * 0.3) for x, y in pts]
        mid_fill = mid_pts + [(pts[-1][0], h - pad_bot), (pts[0][0], h - pad_bot)]
        self.create_polygon(mid_fill, fill="#4c1d95", outline="")

        # ── Courbe lissée #
        smooth = []
        for i, (x, y) in enumerate(pts):
            smooth.extend([x, y])
        self.create_line(smooth, fill=self.ACCENT, width=3, smooth=True, splinesteps=64)

        # dernier point  #
        lx, ly = pts[-1]
        r = 6
        self.create_oval(lx - r, ly - r, lx + r, ly + r,
                         fill=self.ACCENT, outline="white", width=2)

        # ── Labels des mois #
        for i, (month, (x, _)) in enumerate(zip(self.MONTHS, pts)):
            is_last = (i == n - 1)
            color   = "white" if is_last else "#6b7280"
            weight  = "bold"  if is_last else "normal"
            self.create_text(x, h - pad_bot + 14, text=month,
                             fill=color, font=("Helvetica", 10, weight))


class Dasboard(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, corner_radius=0, fg_color="transparent")
        self._build()

    def _build(self):
        #Titre  #
        ctk.CTkLabel(
            self,
            text="Dashboard",
            font=ctk.CTkFont(size=26, weight="bold"),
            anchor="w",
        ).pack(anchor="w", pady=(0, 16))

        # ── Cartes résumé  #
        cards_frame = ctk.CTkFrame(self, fg_color="transparent")
        cards_frame.pack(fill="x", pady=(0, 16))

        cards = [
            ("Solde total",      f"${BALANCE:,.0f}",  "#7c3aed"),
            ("Revenus du mois",  f"${INCOME:,.0f}",   "#2d7a3a"),
            ("Dépenses du mois", f"${EXPENSES:,.0f}", "#9b3a3a"),
        ]
        for title, value, color in cards:
            card = ctk.CTkFrame(cards_frame, corner_radius=10)
            card.pack(side="left", expand=True, fill="both", padx=6)
            ctk.CTkLabel(card, text=title,
                         font=ctk.CTkFont(size=12), text_color="gray"
                         ).pack(anchor="w", padx=14, pady=(12, 2))
            ctk.CTkLabel(card, text=value,
                         font=ctk.CTkFont(size=20, weight="bold"), text_color=color
                         ).pack(anchor="w", padx=14, pady=(0, 12))

        #Graphique de solde #
        chart_outer = ctk.CTkFrame(self, corner_radius=14, fg_color="#1e1e2e")
        chart_outer.pack(fill="x", pady=(8, 0))

        self.chart = BalanceChart(chart_outer, height=200)
        self.chart.pack(fill="x", padx=0, pady=(8, 0))

        # Bande inférieure : solde du jour + variation
        info_bar = ctk.CTkFrame(chart_outer, fg_color="#161625", corner_radius=10)
        info_bar.pack(fill="x", padx=12, pady=(4, 12))

        left = ctk.CTkFrame(info_bar, fg_color="transparent")
        left.pack(side="left", padx=14, pady=10)
        ctk.CTkLabel(left, text="Aujourd'hui",
                     font=ctk.CTkFont(size=11), text_color="gray").pack(anchor="w")
        ctk.CTkLabel(left, text=f"${BALANCE:,.0f}",
                     font=ctk.CTkFont(size=22, weight="bold")).pack(anchor="w")

        right = ctk.CTkFrame(info_bar, fg_color="transparent")
        right.pack(side="right", padx=14)

        # Variation par rapport au mois précédent
        prev   = list(MONTHLY_BALANCE.values())[-2]
        change = (BALANCE - prev) / prev * 100
        color  = "#22c55e" if change >= 0 else "#ef4444"
        arrow  = "▲" if change >= 0 else "▼"
        ctk.CTkLabel(right, text=f"{arrow} {abs(change):.1f}%",
                     font=ctk.CTkFont(size=14, weight="bold"),
                     text_color=color).pack(side="left", padx=(0, 10))

        ctk.CTkButton(right, text="+", width=32, height=32,
                      corner_radius=16, font=ctk.CTkFont(size=18, weight="bold"),
                      fg_color="#7c3aed", hover_color="#6d28d9",
                      command=lambda: None).pack(side="left")