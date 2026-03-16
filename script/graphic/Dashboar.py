import customtkinter as ctk
from balance_chart import BalanceChart


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


class Dashboard(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, corner_radius=0, fg_color="transparent")
        self._build()

    def _build(self):
        # ── Titre ──
        ctk.CTkLabel(
            self,
            text="Dashboard",
            font=ctk.CTkFont(size=26, weight="bold"),
            anchor="w",
        ).pack(anchor="w", pady=(0, 16))

        # ── Cartes résumé ──
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

        # ── Graphique de solde ──
        chart_outer = ctk.CTkFrame(self, corner_radius=14, fg_color="#1e1e2e")
        chart_outer.pack(fill="x", pady=(8, 0))

        self.chart = BalanceChart(chart_outer, height=200)
        self.chart.pack(fill="x", padx=0, pady=(8, 0))

        # ── Bande inférieure : solde du jour + variation ──
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