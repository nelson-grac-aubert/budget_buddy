import tkinter as tk
import customtkinter as ctk
from scripts.graphic.charts.pie_chart import PieChart
from scripts.graphic.modules.transaction_utils import (pie_color, parse_date, col)
from scripts.logic.app.dashboard_data import get_transactions_from_db


class TransactionWindow(ctk.CTkFrame):
    """Vue transactions avec camembert (top 5) + liste récente."""

    def __init__(self, master, user_id: int = 1):
        super().__init__(master, corner_radius=0, fg_color="transparent")
        self._all_transactions = get_transactions_from_db(user_id)
        self._show_transactions()

    def _clear(self):
        for w in self.winfo_children():
            w.destroy()

    def _top5_debits(self) -> list:
        agg = {}
        for t in self._all_transactions:
            if t["montant"] < 0:
                agg[t["categorie"]] = agg.get(t["categorie"], 0) + abs(t["montant"])
        top5 = sorted(agg.items(), key=lambda x: x[1], reverse=True)[:5]
        return [(cat, val, pie_color(cat)) for cat, val in top5]

    def _show_transactions(self):
        self._clear()

        scroll = ctk.CTkScrollableFrame(self, corner_radius=0, fg_color="transparent")
        scroll.pack(fill="both", expand=True)

        ctk.CTkLabel(scroll, text="Transactions",
                     font=ctk.CTkFont(size=26, weight="bold"),
                     anchor="w").pack(anchor="w", pady=(0, 14))

        debits = self._top5_debits()
        total  = sum(v for _, v, _ in debits)

        body = ctk.CTkFrame(scroll, fg_color="transparent")
        body.pack(fill="x", pady=(0, 16))

        # ── Camembert ──
        chart_frame = ctk.CTkFrame(body, corner_radius=14, fg_color="#1e1e2e")
        chart_frame.pack(side="left", fill="both", expand=True, padx=(0, 12))

        ctk.CTkLabel(chart_frame, text="Top 5 des dépenses",
                     font=ctk.CTkFont(size=14, weight="bold"), anchor="w"
                     ).pack(anchor="w", padx=16, pady=(14, 2))
        ctk.CTkLabel(chart_frame, text=f"Total : {total:,.2f} €",
                     font=ctk.CTkFont(size=12), text_color="gray", anchor="w"
                     ).pack(anchor="w", padx=16, pady=(0, 8))
        PieChart(chart_frame, data=debits, height=220).pack(fill="x", padx=12, pady=(0, 12))

        # ── Légende ──
        legend_frame = ctk.CTkFrame(body, corner_radius=14, fg_color="#1e1e2e", width=230)
        legend_frame.pack(side="left", fill="y")
        legend_frame.pack_propagate(False)

        ctk.CTkLabel(legend_frame, text="Catégories",
                     font=ctk.CTkFont(size=14, weight="bold"), anchor="w"
                     ).pack(anchor="w", padx=16, pady=(14, 10))

        for cat, val, _ in debits:
            pct = val / total * 100

            row = ctk.CTkFrame(legend_frame, fg_color="transparent")
            row.pack(fill="x", padx=16, pady=5)

            # Point couleur
            dot = tk.Canvas(row, width=10, height=10, bg="#1e1e2e", highlightthickness=0)
            dot.pack(side="left", padx=(0, 10))
            dot.create_oval(0, 0, 10, 10, fill=pie_color(cat), outline="")

            # Nom catégorie
            ctk.CTkLabel(row, text=cat,
                         font=ctk.CTkFont(size=12),
                         anchor="w").pack(side="left", expand=True, fill="x")

            # Bloc % + montant alignés à droite
            right = ctk.CTkFrame(row, fg_color="transparent")
            right.pack(side="right")

            ctk.CTkLabel(right, text=f"{pct:.1f} %",
                         font=ctk.CTkFont(size=12, weight="bold"),
                         text_color=pie_color(cat),
                         width=54, anchor="e").pack(side="left")

            ctk.CTkLabel(right, text=f"{val:,.0f} €",
                         font=ctk.CTkFont(size=11),
                         text_color="gray",
                         width=50, anchor="e").pack(side="left")

            # Séparateur léger
            ctk.CTkFrame(legend_frame, height=1, fg_color="#2a2a3e").pack(
                fill="x", padx=16)

        # ── Transactions récentes ──
        ctk.CTkLabel(scroll, text="Transactions récentes",
                     font=ctk.CTkFont(size=14, weight="bold"), anchor="w"
                     ).pack(anchor="w", pady=(4, 8))

        list_frame = ctk.CTkFrame(scroll, corner_radius=14, fg_color="#1e1e2e")
        list_frame.pack(fill="x")

        recent = sorted(self._all_transactions,
                        key=lambda t: parse_date(t["date"]), reverse=True)[:8]

        for i, t in enumerate(recent):
            row = ctk.CTkFrame(list_frame, fg_color="transparent")
            row.pack(fill="x", padx=14, pady=(10 if i == 0 else 4, 4))

            dot_c = tk.Canvas(row, width=10, height=10, bg="#1e1e2e", highlightthickness=0)
            dot_c.pack(side="left", padx=(0, 10))
            dot_c.create_oval(0, 0, 10, 10, fill=pie_color(t["categorie"]), outline="")

            ctk.CTkLabel(row, text=t["description"],
                         font=ctk.CTkFont(size=13), anchor="w"
                         ).pack(side="left", expand=True, fill="x")

            ctk.CTkLabel(row, text=t["date"],
                         font=ctk.CTkFont(size=11), text_color="gray",
                         width=80, anchor="e").pack(side="left", padx=(0, 12))

            sign    = "+" if t["montant"] >= 0 else ""
            amt_col = col("credit") if t["montant"] >= 0 else col("debit")
            ctk.CTkLabel(row, text=f"{sign}{t['montant']:,.2f} €",
                         font=ctk.CTkFont(size=13, weight="bold"),
                         text_color=amt_col, width=100, anchor="e"
                         ).pack(side="right")

            if i < len(recent) - 1:
                ctk.CTkFrame(list_frame, height=1, fg_color="#2a2a3e").pack(
                    fill="x", padx=14, pady=(4, 0))

        ctk.CTkFrame(list_frame, height=10, fg_color="transparent").pack()