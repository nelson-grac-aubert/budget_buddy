import customtkinter as ctk
from scripts.graphic.balance_chart import BalanceChart
from scripts.graphic.transfer_window import VirementWindow
from scripts.graphic.withdrawal_window import RetraitWindow
from scripts.graphic.depot_window import DepotWindow
 
 
# ── Toast de notification 
 
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
 
        ctk.CTkButton(frame, text="X", width=24, height=24,
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
 
 
# ── Dashboard 
 
class Dashboard(ctk.CTkFrame):
    def __init__(self, current_user_id, master, balance,
                 monthly_balance: dict = None,
                 income: float         = 0.0,
                 expenses: float       = 0.0,
                 fullname: str         = "",
                 on_releve=None,
                 on_notify=None,
                 on_logout=None):
        super().__init__(master, corner_radius=0, fg_color="transparent")
 
        self._monthly_balance = monthly_balance or {}
        self._balance         = balance
        self._income          = income
        self._expenses        = expenses
        self._fullname        = fullname
        self._virement_window = None
        self._retrait_window  = None
        self._depot_window    = None
        self._on_releve       = on_releve
        self._on_notify       = on_notify
        self._on_logout       = on_logout
        self.current_user_id  = current_user_id
        self._build()
 
    # ── Layout principal 
 
    def _build(self):
        scroll = ctk.CTkScrollableFrame(self, corner_radius=0, fg_color="transparent")
        scroll.pack(fill="both", expand=True)
 
        # En-tête : salutation + bouton déconnexion
        header = ctk.CTkFrame(scroll, fg_color="transparent")
        header.pack(fill="x", pady=(0, 16))
 
        greeting = f"Welcome, {self._fullname}" if self._fullname else "Welcome"
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
 
    # ── Cartes résumé 
 
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
 
    # ── Boutons d'action 
 
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
 
    # ── Graph
 
    def _build_chart_section(self, parent):
        chart_outer = ctk.CTkFrame(parent, corner_radius=14, fg_color="#1e1e2e")
        chart_outer.pack(fill="x", pady=(8, 0))
 
        if len(self._monthly_balance) >= 2:
            BalanceChart(chart_outer,
                         months=list(self._monthly_balance.keys()),
                         values=list(self._monthly_balance.values()),
                         height=280).pack(fill="x", padx=0, pady=12)
        else:
            ctk.CTkLabel(chart_outer,
                         text="Aucune operation enregistree pour le moment.",
                         font=ctk.CTkFont(size=13),
                         text_color="gray").pack(pady=40)
 
    # ── Notifications 
 
    def _notify(self, title: str, message: str, kind: str = "success"):
        _Toast(self.winfo_toplevel(), title, message, kind)
        if self._on_notify:
            self._on_notify(title, message, kind)
 
    # ── Déconnexion 
 
    def _logout(self):
        if self._on_logout:
            self._on_logout()
 
    # ── Fenêtres secondaires 
 
    def _open_virement(self):
        if self._virement_window is None or not self._virement_window.winfo_exists():
            self._virement_window = VirementWindow(
                self.current_user_id,
                master=self,
                on_success=lambda t, m: self._notify(t, m, kind="success"),
            )
            self._virement_window.focus()
        else:
            self._virement_window.focus()
 
    def _open_retrait(self):
        if self._retrait_window is None or not self._retrait_window.winfo_exists():
            self._retrait_window = RetraitWindow(
                self.current_user_id,
                master=self,
                on_success=lambda t, m: self._notify(t, m, kind="warning"),
            )
            self._retrait_window.focus()
 
    def _open_depot(self):
        if self._depot_window is None or not self._depot_window.winfo_exists():
            self._depot_window = DepotWindow(
                self.current_user_id,
                master=self,
                on_success=lambda t, m: self._notify(t, m, kind="warning"),
            )
            self._depot_window.focus()