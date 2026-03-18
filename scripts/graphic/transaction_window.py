import tkinter as tk
import customtkinter as ctk
from scripts.graphic.pie_chart import PieChart
from scripts.graphic.releve_view import ReleveView
from scripts.graphic.transaction_utils import (
    get_transactions, pie_color, parse_date, col
)


class TransactionWindow(ctk.CTkFrame):
    """Vue transactions avec camembert + liste récente."""

    def __init__(self, master, user_id: int = 1):
        super().__init__(master, corner_radius=0, fg_color="transparent")
        self._all_transactions = get_transactions(user_id)
        self._show_transactions()

    def _clear(self):
        for w in self.winfo_children():
            w.destroy()

    def _show_transactions(self):
        self._clear()

        scroll = ctk.CTkScrollableFrame(self, corner_radius=0, fg_color="transparent")
        scroll.pack(fill="both", expand=True)

        ctk.CTkLabel(scroll, text="Transactions",
                     font=ctk.CTkFont(size=26, weight="bold"),
                     anchor="w").pack(anchor="w", pady=(0, 14))

        debits = [(t["categorie"], abs(t["montant"]), pie_color(t["categorie"]))
                  for t in self._all_transactions if t["montant"] < 0]
        total  = sum(v for _, v, _ in debits)

        body = ctk.CTkFrame(scroll, fg_color="transparent")
        body.pack(fill="x", pady=(0, 16))

        # Camembert
        chart_frame = ctk.CTkFrame(body, corner_radius=14, fg_color="#1e1e2e")
        chart_frame.pack(side="left", fill="both", expand=True, padx=(0, 12))

        ctk.CTkLabel(chart_frame, text="Répartition des dépenses",
                     font=ctk.CTkFont(size=14, weight="bold"), anchor="w"
                     ).pack(anchor="w", padx=16, pady=(14, 4))
        ctk.CTkLabel(chart_frame, text=f"Total dépenses : {total:,.2f} €",
                     font=ctk.CTkFont(size=12), text_color="gray", anchor="w"
                     ).pack(anchor="w", padx=16, pady=(0, 8))
        PieChart(chart_frame, data=debits, height=220).pack(fill="x", padx=12, pady=(0, 12))

        # Légende
        legend_frame = ctk.CTkFrame(body, corner_radius=14, fg_color="#1e1e2e", width=210)
        legend_frame.pack(side="left", fill="y")
        legend_frame.pack_propagate(False)
        ctk.CTkLabel(legend_frame, text="Catégories",
                     font=ctk.CTkFont(size=14, weight="bold"), anchor="w"
                     ).pack(anchor="w", padx=16, pady=(14, 8))

        seen = {}
        for cat, val, _ in debits:
            seen[cat] = seen.get(cat, 0) + val
        for cat, val in seen.items():
            pct = val / total * 100
            row = ctk.CTkFrame(legend_frame, fg_color="transparent")
            row.pack(fill="x", padx=16, pady=3)
            dot = tk.Canvas(row, width=12, height=12, bg="#1e1e2e", highlightthickness=0)
            dot.pack(side="left", padx=(0, 8))
            dot.create_rectangle(2, 2, 10, 10, fill=pie_color(cat), outline="")
            ctk.CTkLabel(row, text=cat, font=ctk.CTkFont(size=12),
                         anchor="w").pack(side="left", expand=True, fill="x")
            ctk.CTkLabel(row, text=f"{pct:.1f}%",
                         font=ctk.CTkFont(size=12, weight="bold"),
                         text_color=pie_color(cat),
                         anchor="e", width=44).pack(side="right")

        # Liste récente
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

            dot_c = tk.Canvas(row, width=12, height=12, bg="#1e1e2e", highlightthickness=0)
            dot_c.pack(side="left", padx=(0, 10))
            dot_c.create_oval(1, 1, 11, 11, fill=pie_color(t["categorie"]), outline="")

            ctk.CTkLabel(row, text=t["description"],
                         font=ctk.CTkFont(size=13), anchor="w"
                         ).pack(side="left", expand=True, fill="x")
            ctk.CTkLabel(row, text=t["date"],
                         font=ctk.CTkFont(size=11), text_color="gray",
                         anchor="e", width=80).pack(side="left")

            sign    = "+" if t["montant"] >= 0 else ""
            amt_col = col("credit") if t["montant"] >= 0 else col("debit")
            ctk.CTkLabel(row, text=f"{sign}{t['montant']:,.2f} €",
                         font=ctk.CTkFont(size=13, weight="bold"),
                         text_color=amt_col, anchor="e", width=100
                         ).pack(side="right")

            if i < len(recent) - 1:
                ctk.CTkFrame(list_frame, height=1, fg_color="#2a2a3e").pack(
                    fill="x", padx=14, pady=(4, 0))

        ctk.CTkFrame(list_frame, height=10, fg_color="transparent").pack()