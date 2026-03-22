import customtkinter as ctk

from scripts.graphic.charts.balance_chart import BalanceChart
from scripts.graphic.modules.toast import Toast
from scripts.graphic.windows.transfer_window import VirementWindow
from scripts.graphic.windows.withdrawal_window import RetraitWindow
from scripts.graphic.windows.deposit_window import DepotWindow


class Dashboard(ctk.CTkFrame):
    def __init__(self, current_user_id, master, balance,
                 monthly_balance: dict = None,
                 income: float         = 0.0,
                 expenses: float       = 0.0,
                 fullname: str         = "",
                 sidebar=None,
                 on_releve=None,
                 on_notify=None,
                 on_logout=None,
                 on_refresh=None):
        super().__init__(master, corner_radius=0, fg_color="transparent")

        self._monthly_balance = monthly_balance or {}
        self._balance         = balance
        self._income          = income
        self._expenses        = expenses
        self._fullname        = fullname
        self._sidebar         = sidebar
        self._chart_outer     = None
        self._virement_window = None
        self._retrait_window  = None
        self._depot_window    = None
        self._on_releve       = on_releve
        self._on_notify       = on_notify
        self._on_logout       = on_logout
        self._on_refresh      = on_refresh
        self.current_user_id  = current_user_id
        self._build()

    # ── Layout principal

    def _build(self):
        scroll = ctk.CTkScrollableFrame(self, corner_radius=0, fg_color="transparent")
        scroll.pack(fill="both", expand=True)

        header = ctk.CTkFrame(scroll, fg_color="transparent")
        header.pack(fill="x", pady=(0, 16))

        greeting = f"Bienvenue, {self._fullname}" if self._fullname else "Bienvenue"
        ctk.CTkLabel(header, text=greeting,
                     font=ctk.CTkFont(size=26, weight="bold"),
                     anchor="w").pack(side="left")

        ctk.CTkButton(
            header,
            text="⏻  Déconnexion",
            width=130, height=34,
            fg_color="transparent",
            border_width=2,
            border_color="#ef4444",
            text_color="#ef4444",
            hover_color="#3b1a1a",
            font=ctk.CTkFont(size=13),
            command=self._logout,
        ).pack(side="right")

        self._build_summary_cards(scroll)
        self._build_action_buttons(scroll)
        self._build_chart_section(scroll)

    # ── Summary cards

    def _build_summary_cards(self, parent):
        cards_frame = ctk.CTkFrame(parent, fg_color="transparent")
        cards_frame.pack(fill="x", pady=(0, 12))

        for title, value, color in [
            ("Solde total",      f"${self._balance:,.0f}",  "#7c3aed"),
            ("Revenus du mois",  f"${self._income:,.0f}",   "#2d7a3a"),
            ("Depenses du mois", f"${self._expenses:,.0f}", "#9b3a3a"),
        ]:
            card = ctk.CTkFrame(cards_frame, corner_radius=10)
            card.pack(side="left", expand=True, fill="both", padx=6)
            ctk.CTkLabel(card, text=title,
                         font=ctk.CTkFont(size=12), text_color="gray"
                         ).pack(anchor="w", padx=14, pady=(12, 2))
            ctk.CTkLabel(card, text=value,
                         font=ctk.CTkFont(size=20, weight="bold"), text_color=color
                         ).pack(anchor="w", padx=14, pady=(0, 12))

    # ── action buttons

    def _build_action_buttons(self, parent):
        actions_frame = ctk.CTkFrame(parent, fg_color="transparent")
        actions_frame.pack(fill="x", pady=(0, 12))

        for icon, label, cmd in [
            ("💸", "Virement", self._open_virement),
            ("💳", "Retrait",  self._open_retrait),
            ("💶", "Dépôt",    self._open_depot),
            ("📊", "Épargne",  lambda: print("Épargne clicked")),
            ("📄", "Relevé",   lambda: self._on_releve() if self._on_releve else None),
        ]:
            bf = ctk.CTkFrame(actions_frame, fg_color="transparent")
            bf.pack(side="left", expand=True)
            ctk.CTkButton(bf, text=icon, width=52, height=52, corner_radius=26,
                          font=ctk.CTkFont(size=23),
                          fg_color="#1e1e2e", hover_color="#4c1d95",
                          command=cmd).pack()
            ctk.CTkLabel(bf, text=label,
                         font=ctk.CTkFont(size=15),
                         text_color="gray").pack(pady=(6, 0))

    # ── Graphic

    def _build_chart_section(self, parent):
        self._chart_outer = ctk.CTkFrame(parent, corner_radius=14, fg_color="#1e1e2e")
        self._chart_outer.pack(fill="x", pady=(8, 0))

        if len(self._monthly_balance) >= 2:
            BalanceChart(self._chart_outer,
                         months=list(self._monthly_balance.keys()),
                         values=list(self._monthly_balance.values()),
                         height=280).pack(fill="x", padx=0, pady=12)
        else:
            ctk.CTkLabel(self._chart_outer,
                         text="Pas assez de donnée pour une courbe de tendance.",
                         font=ctk.CTkFont(size=13),
                         text_color="gray").pack(pady=40)

    # ── Calculate the anchor position for toasts

    def _toast_anchor(self):
        """Retourne (x, y) : bord droit de la sidebar, bas du graphique."""
        self.update_idletasks()

        x = (self._sidebar.winfo_rootx() + self._sidebar.winfo_width() + 10
             if self._sidebar is not None
             else self.winfo_screenwidth() - Toast._WIDTH - 20)

        y = (self._chart_outer.winfo_rooty() + self._chart_outer.winfo_height() + 10
             if self._chart_outer is not None
             else self.winfo_screenheight() - 200)

        return x, y

    # ── Notifications

    def _notify(self, title: str, message: str, kind: str = "success"):
        """Toast + ajout à la liste + refresh du dashboard."""
        x, y = self._toast_anchor()
        Toast(self.winfo_toplevel(), title, message, kind, anchor_x=x, anchor_y=y)
        if self._on_notify:
            self._on_notify(title, message, kind)
        if self._on_refresh:
            self._on_refresh()

    def _notify_no_refresh(self, title: str, message: str, kind: str = "warning"):
        """Toast + ajout à la liste, SANS refresh."""
        x, y = self._toast_anchor()
        Toast(self.winfo_toplevel(), title, message, kind, anchor_x=x, anchor_y=y)
        if self._on_notify:
            self._on_notify(title, message, kind)

    # ── Logout

    def _logout(self):
        if self._on_logout:
            self._on_logout()

    # ── second windows

    def _open_virement(self):
        if self._virement_window is None or not self._virement_window.winfo_exists():
            self._virement_window = VirementWindow(
                self.current_user_id,
                master=self,
                on_success=lambda t, m: self._notify(t, m, kind="success"),
                on_overdraft=lambda t, m: self._notify_no_refresh(t, m, kind="warning"),
            )
            self._virement_window.focus()
        else:
            self._virement_window.focus()

    def _open_retrait(self):
        if self._retrait_window is None or not self._retrait_window.winfo_exists():
            self._retrait_window = RetraitWindow(
                self.current_user_id,
                master=self,
                on_success=lambda t, m: self._notify(t, m, kind="success"),
                on_overdraft=lambda t, m: self._notify_no_refresh(t, m, kind="warning"),
            )
            self._retrait_window.focus()

    def _open_depot(self):
        if self._depot_window is None or not self._depot_window.winfo_exists():
            self._depot_window = DepotWindow(
                self.current_user_id,
                master=self,
                on_success=lambda t, m: self._notify(t, m, kind="success"),
            )
            self._depot_window.focus()