import customtkinter as ctk
from scripts.graphic.balance_chart import BalanceChart
from scripts.graphic.virement_window import VirementWindow
from scripts.graphic.retrait_window import RetraitWindow


# TODO : remplacer par des données réelles issues de la base de données
_MONTHLY_BALANCE = {
    "Jan": 45000,
    "Fév": 47500,
    "Mar": 51200,
    "Avr": 49800,
    "Mai": 62970,
}
_INCOME   = 5_200
_EXPENSES = 3_180

_QUICK_ACTIONS = [
    ("💸", "Virement"),
    ("💶", "Retrait"),
    ("💳", "Paiement"),
    ("📊", "Épargne"),
    ("📄", "Relevé"),
]


class Dashboard(ctk.CTkFrame):
    def __init__(self, master,
                 monthly_balance: dict = _MONTHLY_BALANCE,
                 income: float         = _INCOME,
                 expenses: float       = _EXPENSES):
        super().__init__(master, corner_radius=0, fg_color="transparent")
        self._monthly_balance = monthly_balance
        self._income          = income
        self._expenses        = expenses
        self._balance         = list(monthly_balance.values())[-1]
        self._virement_window = None
        self._retrait_window  = None
        self._build()

    def _build(self):
        # Scroll container — évite que le contenu soit rogné
        scroll = ctk.CTkScrollableFrame(self, corner_radius=0, fg_color="transparent")
        scroll.pack(fill="both", expand=True)

        # ── Titre ──
        ctk.CTkLabel(
            scroll,
            text="Dashboard",
            font=ctk.CTkFont(size=26, weight="bold"),
            anchor="w",
        ).pack(anchor="w", pady=(0, 16))

        # ── Cartes résumé ──
        cards_frame = ctk.CTkFrame(scroll, fg_color="transparent")
        cards_frame.pack(fill="x", pady=(0, 12))

        cards = [
            ("Solde total",      f"${self._balance:,.0f}",  "#7c3aed"),
            ("Revenus du mois",  f"${self._income:,.0f}",   "#2d7a3a"),
            ("Dépenses du mois", f"${self._expenses:,.0f}", "#9b3a3a"),
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

        # ── Actions rapides ──
        actions_frame = ctk.CTkFrame(scroll, fg_color="transparent")
        actions_frame.pack(fill="x", pady=(0, 12))

        action_commands = {
            "Virement": self._open_virement,
            "Retrait":  self._open_retrait,
            "Paiement": lambda: print("Paiement clicked"),
            "Épargne":  lambda: print("Épargne clicked"),
            "Relevé":   lambda: print("Relevé clicked"),
        }

        for icon, label in _QUICK_ACTIONS:
            btn_frame = ctk.CTkFrame(actions_frame, fg_color="transparent")
            btn_frame.pack(side="left", expand=True)

            ctk.CTkButton(
                btn_frame,
                text=icon,
                width=52, height=52,
                corner_radius=26,
                font=ctk.CTkFont(size=22),
                fg_color="#1e1e2e",
                hover_color="#4c1d95",
                command=action_commands[label],
            ).pack()

            ctk.CTkLabel(
                btn_frame,
                text=label,
                font=ctk.CTkFont(size=11),
                text_color="gray",
            ).pack(pady=(6, 0))

        # ── Graphique de solde ──
        chart_outer = ctk.CTkFrame(scroll, corner_radius=14, fg_color="#1e1e2e")
        chart_outer.pack(fill="x", pady=(8, 0))

        self.chart = BalanceChart(
            chart_outer,
            months=list(self._monthly_balance.keys()),
            values=list(self._monthly_balance.values()),
            height=200,
        )
        self.chart.pack(fill="x", padx=0, pady=(8, 0))

        # ── Bande inférieure ──
        info_bar = ctk.CTkFrame(chart_outer, fg_color="#161625", corner_radius=10)
        info_bar.pack(fill="x", padx=12, pady=(4, 12))

        left = ctk.CTkFrame(info_bar, fg_color="transparent")
        left.pack(side="left", padx=14, pady=10)
        ctk.CTkLabel(left, text="Aujourd'hui",
                     font=ctk.CTkFont(size=11), text_color="gray").pack(anchor="w")
        ctk.CTkLabel(left, text=f"${self._balance:,.0f}",
                     font=ctk.CTkFont(size=22, weight="bold")).pack(anchor="w")

        right = ctk.CTkFrame(info_bar, fg_color="transparent")
        right.pack(side="right", padx=14)

        prev   = list(self._monthly_balance.values())[-2]
        change = (self._balance - prev) / prev * 100
        color  = "#22c55e" if change >= 0 else "#ef4444"
        arrow  = "▲" if change >= 0 else "▼"
        ctk.CTkLabel(right, text=f"{arrow} {abs(change):.1f}%",
                     font=ctk.CTkFont(size=14, weight="bold"),
                     text_color=color).pack(side="left", padx=(0, 10))

        ctk.CTkButton(right, text="+", width=32, height=32,
                      corner_radius=16, font=ctk.CTkFont(size=18, weight="bold"),
                      fg_color="#7c3aed", hover_color="#6d28d9",
                      command=lambda: None).pack(side="left")

    # ── Fenêtres secondaires 

    def _open_virement(self):
        if self._virement_window is None or not self._virement_window.winfo_exists():
            self._virement_window = VirementWindow(master=self)
            self._virement_window.focus()
        else:
            self._virement_window.focus()

    def _open_retrait(self):
        if self._retrait_window is None or not self._retrait_window.winfo_exists():
            self._retrait_window = RetraitWindow(master=self)
            self._retrait_window.focus()
        else:
            self._retrait_window.focus()