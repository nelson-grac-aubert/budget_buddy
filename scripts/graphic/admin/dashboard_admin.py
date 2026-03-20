import customtkinter as ctk
from scripts.logic.app.dashboard_data import get_all_accounts


class AdminDashboard(ctk.CTkFrame):
    """Vue admin — liste de tous les comptes avec solde."""

    def __init__(self, master, on_logout=None):
        super().__init__(master, corner_radius=0, fg_color="transparent")
        self._on_logout = on_logout
        self._accounts  = []
        self._sort_asc  = False
        self._search    = ctk.StringVar()
        self._build()

    # ── Construction ──

    def _build(self):
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.pack(fill="x", pady=(0, 16))

        ctk.CTkLabel(
            header, text="👑  Admin — Comptes",
            font=ctk.CTkFont(size=24, weight="bold"), anchor="w",
        ).pack(side="left")

        ctk.CTkButton(
            header, text="⏻  Déconnexion",
            width=130, height=34,
            fg_color="transparent", border_width=2,
            border_color="#ef4444", text_color="#ef4444",
            hover_color="#3b1a1a", font=ctk.CTkFont(size=13),
            command=lambda: self._on_logout() if self._on_logout else None,
        ).pack(side="right")

        toolbar = ctk.CTkFrame(self, corner_radius=10)
        toolbar.pack(fill="x", pady=(0, 12), ipady=8)

        ctk.CTkLabel(toolbar, text="🔍", font=ctk.CTkFont(size=14)
                     ).pack(side="left", padx=(14, 4))
        ctk.CTkEntry(
            toolbar, textvariable=self._search,
            placeholder_text="Rechercher par nom ou email...",
            width=260, height=32, font=ctk.CTkFont(size=12),
        ).pack(side="left", padx=(0, 12))

        ctk.CTkButton(
            toolbar, text="Appliquer", width=100, height=32,
            font=ctk.CTkFont(size=12, weight="bold"),
            fg_color="#0d9488", hover_color="#0f766e",
            command=self._render,
        ).pack(side="left")

        ctk.CTkButton(
            toolbar, text="Réinitialiser", width=110, height=32,
            fg_color="transparent", border_width=2,
            text_color=("gray10", "gray90"), font=ctk.CTkFont(size=12),
            command=self._reset,
        ).pack(side="left", padx=(8, 0))

        self._sort_btn = ctk.CTkButton(
            toolbar, text="Solde ↓", width=100, height=32,
            fg_color="transparent", border_width=2,
            text_color=("gray10", "gray90"), font=ctk.CTkFont(size=12),
            command=self._toggle_sort,
        )
        self._sort_btn.pack(side="right", padx=14)

        self._count_label = ctk.CTkLabel(
            self, text="", font=ctk.CTkFont(size=12), text_color="gray")
        self._count_label.pack(anchor="w", padx=4, pady=(0, 6))

        self._table = ctk.CTkScrollableFrame(
            self, corner_radius=10, fg_color="#111a1a")
        self._table.pack(fill="both", expand=True)

        self._load()

    # ── Données ──

    def _load(self):
        self._accounts = get_all_accounts()
        self._render()

    def _filtered(self) -> list:
        search = self._search.get().strip().lower()
        data   = list(self._accounts)
        if search:
            data = [a for a in data
                    if search in a["fullname"].lower()
                    or search in a["email"].lower()]
        data.sort(key=lambda a: a["balance"], reverse=not self._sort_asc)
        return data

    # ── Rendu ──

    def _render(self):
        for w in self._table.winfo_children():
            w.destroy()

        data = self._filtered()
        self._count_label.configure(text=f"{len(data)} compte(s) trouvé(s)")

        if not data:
            ctk.CTkLabel(
                self._table,
                text="Aucun compte ne correspond.",
                font=ctk.CTkFont(size=13), text_color="gray",
            ).pack(pady=40)
            return

        self._render_header()
        for i, account in enumerate(data):
            self._render_row(account, i)
        self._render_summary(len(data), sum(a["balance"] for a in data))

    def _render_header(self):
        header = ctk.CTkFrame(self._table, fg_color="#1a7a7a", corner_radius=0)
        header.pack(fill="x", padx=2, pady=(2, 0))
        for col, w in [
            ("ID user",     60),
            ("ID compte",   70),
            ("Nom complet", 180),
            ("Email",       220),
            ("Solde",       110),
        ]:
            ctk.CTkLabel(
                header, text=col, width=w, anchor="center",
                font=ctk.CTkFont(size=12, weight="bold"), text_color="white",
            ).pack(side="left", padx=2, pady=8)

    def _render_row(self, account: dict, index: int):
        bg            = "#1e2a2a" if index % 2 == 0 else "#162020"
        balance_color = "#22c55e" if account["balance"] >= 0 else "#ef4444"
        sign          = "+" if account["balance"] >= 0 else ""

        row = ctk.CTkFrame(self._table, fg_color=bg, corner_radius=0)
        row.pack(fill="x", padx=2)

        for text, w, anchor, fg in [
            (f"#{account['user_id']}",             60,  "center", "#9ca3af"),
            (f"#{account['account_id']}",          70,  "center", "#6b7280"),
            (account["fullname"],                  180, "w",      "#d1d5db"),
            (account["email"],                     220, "w",      "#9ca3af"),
            (f"{sign}{account['balance']:,.2f} €", 110, "e",      balance_color),
        ]:
            ctk.CTkLabel(
                row, text=text, width=w, anchor=anchor,
                font=ctk.CTkFont(size=12), text_color=fg,
            ).pack(side="left", padx=(6 if anchor == "w" else 2), pady=7)

        ctk.CTkFrame(self._table, height=1, fg_color="#2d3a3a").pack(fill="x", padx=2)

    def _render_summary(self, count: int, total: float):
        color = "#22c55e" if total >= 0 else "#ef4444"
        sign  = "+" if total >= 0 else ""

        row = ctk.CTkFrame(self._table, fg_color="#0d3030", corner_radius=0)
        row.pack(fill="x", padx=2, pady=(4, 0))

        ctk.CTkLabel(
            row, text=f"Total — {count} compte(s)",
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color="white", anchor="w",
        ).pack(side="left", padx=14, pady=10, expand=True, fill="x")

        ctk.CTkLabel(
            row, text=f"{sign}{total:,.2f} €",
            font=ctk.CTkFont(size=13, weight="bold"),
            text_color=color, anchor="e",
        ).pack(side="right", padx=16, pady=10)

    # ── Actions ──

    def _reset(self):
        self._search.set("")
        self._render()

    def _toggle_sort(self):
        self._sort_asc = not self._sort_asc
        self._sort_btn.configure(text="Solde ↑" if self._sort_asc else "Solde ↓")
        self._render()