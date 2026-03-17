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


# ── Toast de notification ─────────────────────────────────────────────────── #

class _Toast(ctk.CTkToplevel):
    """Notification flottante qui disparaît automatiquement après 4 s."""

    def __init__(self, master, title: str, message: str, kind: str = "success"):
        super().__init__(master)
        self.overrideredirect(True)
        self.attributes("-topmost", True)
        self.resizable(False, False)

        colors = {
            "success": ("#14532d", "#22c55e"),
            "warning": ("#78350f", "#f59e0b"),
            "error":   ("#7f1d1d", "#ef4444"),
            "info":    ("#1e3a5f", "#3b82f6"),
        }
        bg, accent = colors.get(kind, colors["success"])

        frame = ctk.CTkFrame(self, fg_color=bg, corner_radius=12,
                             border_width=1, border_color=accent)
        frame.pack(padx=0, pady=0)

        # Barre colorée à gauche
        ctk.CTkFrame(frame, width=4, fg_color=accent,
                     corner_radius=0).pack(side="left", fill="y", padx=(0, 12))

        content = ctk.CTkFrame(frame, fg_color="transparent")
        content.pack(side="left", padx=(0, 16), pady=14)

        ctk.CTkLabel(content, text=title,
                     font=ctk.CTkFont(size=13, weight="bold"),
                     text_color=accent, anchor="w").pack(anchor="w")
        ctk.CTkLabel(content, text=message,
                     font=ctk.CTkFont(size=12),
                     text_color="#d1d5db", anchor="w",
                     wraplength=260).pack(anchor="w", pady=(2, 0))

        ctk.CTkButton(frame, text="✕", width=24, height=24,
                      fg_color="transparent", text_color="#9ca3af",
                      hover_color=bg, font=ctk.CTkFont(size=12),
                      command=self._close
                      ).pack(side="right", padx=(0, 8), pady=8, anchor="n")

        self.update_idletasks()
        self._position()
        self._job = self.after(4000, self._close)

    def _position(self):
        w  = self.winfo_width()
        h  = self.winfo_height()
        sw = self.winfo_screenwidth()
        sh = self.winfo_screenheight()
        self.geometry(f"{w}x{h}+{sw - w - 24}+{sh - h - 60}")

    def _close(self):
        try:
            self.after_cancel(self._job)
        except Exception:
            pass
        self.destroy()


# ── Dashboard ─────────────────────────────────────────────────────────────── #

class Dashboard(ctk.CTkFrame):
    def __init__(self, master,
                 monthly_balance: dict = _MONTHLY_BALANCE,
                 income: float         = _INCOME,
                 expenses: float       = _EXPENSES,
                 on_releve=None):
        super().__init__(master, corner_radius=0, fg_color="transparent")
        self._monthly_balance = monthly_balance
        self._income          = income
        self._expenses        = expenses
        self._balance         = list(monthly_balance.values())[-1]
        self._virement_window = None
        self._retrait_window  = None
        self._on_releve       = on_releve
        self._build()

    def _build(self):
        scroll = ctk.CTkScrollableFrame(self, corner_radius=0, fg_color="transparent")
        scroll.pack(fill="both", expand=True)

        # ── Titre ──
        ctk.CTkLabel(scroll, text="Dashboard",
                     font=ctk.CTkFont(size=26, weight="bold"),
                     anchor="w").pack(anchor="w", pady=(0, 16))

        # ── Cartes résumé ──
        cards_frame = ctk.CTkFrame(scroll, fg_color="transparent")
        cards_frame.pack(fill="x", pady=(0, 12))

        for title, value, color in [
            ("Solde total",      f"${self._balance:,.0f}",  "#7c3aed"),
            ("Revenus du mois",  f"${self._income:,.0f}",   "#2d7a3a"),
            ("Dépenses du mois", f"${self._expenses:,.0f}", "#9b3a3a"),
        ]:
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

        for icon, label, cmd in [
            ("💸", "Virement", self._open_virement),
            ("💶", "Retrait",  self._open_retrait),
            ("💳", "Paiement", lambda: print("Paiement clicked")),
            ("📊", "Épargne",  lambda: print("Épargne clicked")),
            ("📄", "Relevé",   lambda: self._on_releve() if self._on_releve else None),
        ]:
            bf = ctk.CTkFrame(actions_frame, fg_color="transparent")
            bf.pack(side="left", expand=True)
            ctk.CTkButton(bf, text=icon, width=52, height=52, corner_radius=26,
                          font=ctk.CTkFont(size=22),
                          fg_color="#1e1e2e", hover_color="#4c1d95",
                          command=cmd).pack()
            ctk.CTkLabel(bf, text=label,
                         font=ctk.CTkFont(size=11),
                         text_color="gray").pack(pady=(6, 0))

        # ── Graphique ──
        chart_outer = ctk.CTkFrame(scroll, corner_radius=14, fg_color="#1e1e2e")
        chart_outer.pack(fill="x", pady=(8, 0))

        BalanceChart(chart_outer,
                     months=list(self._monthly_balance.keys()),
                     values=list(self._monthly_balance.values()),
                     height=200).pack(fill="x", padx=0, pady=(8, 0))

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
        ctk.CTkLabel(right,
                     text=f"{'▲' if change >= 0 else '▼'} {abs(change):.1f}%",
                     font=ctk.CTkFont(size=14, weight="bold"),
                     text_color=color).pack(side="left", padx=(0, 10))

        ctk.CTkButton(right, text="+", width=32, height=32, corner_radius=16,
                      font=ctk.CTkFont(size=18, weight="bold"),
                      fg_color="#7c3aed", hover_color="#6d28d9",
                      command=lambda: None).pack(side="left")

    # ── Notifications ─────────────────────────────────────────────────────── #

    def _notify(self, title: str, message: str, kind: str = "success"):
        _Toast(self.winfo_toplevel(), title, message, kind)

    # ── Fenêtres secondaires ──────────────────────────────────────────────── #

    def _open_virement(self):
        if self._virement_window is None or not self._virement_window.winfo_exists():
            self._virement_window = VirementWindow(
                master=self,
                on_success=lambda t, m: self._notify(t, m, kind="success"),
            )
            self._virement_window.focus()
        else:
            self._virement_window.focus()

    def _open_retrait(self):
        if self._retrait_window is None or not self._retrait_window.winfo_exists():
            self._retrait_window = RetraitWindow(
                master=self,
                on_success=lambda t, m: self._notify(t, m, kind="warning"),
            )
            self._retrait_window.focus()