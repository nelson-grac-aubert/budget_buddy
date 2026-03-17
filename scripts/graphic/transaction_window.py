import tkinter as tk
import customtkinter as ctk
from scripts.graphic.pie_chart import PieChart
from data import *


class TransactionWindow(ctk.CTkFrame):
    """Vue transactions avec camembert des dépenses par motif."""

    def __init__(self, master, user_id: int = 1):
        super().__init__(master, corner_radius=0, fg_color="transparent")
        self._transactions = get_transactions(user_id)
        self._build()

    def _build(self):
        # Titre
        ctk.CTkLabel(
            self,
            text="Transactions",
            font=ctk.CTkFont(size=26, weight="bold"),
            anchor="w",
        ).pack(anchor="w", pady=(0, 16))

        body = ctk.CTkFrame(self, fg_color="transparent")
        body.pack(fill="both", expand=True)

        # ── Camembert ──
        chart_frame = ctk.CTkFrame(body, corner_radius=14, fg_color="#1e1e2e")
        chart_frame.pack(side="left", fill="both", expand=True, padx=(0, 12))

        total = sum(v for _, v, _ in self._transactions)

        ctk.CTkLabel(
            chart_frame,
            text="Répartition des dépenses",
            font=ctk.CTkFont(size=14, weight="bold"),
            anchor="w",
        ).pack(anchor="w", padx=16, pady=(14, 4))

        ctk.CTkLabel(
            chart_frame,
            text=f"Total : {total:,.2f} €",
            font=ctk.CTkFont(size=12),
            text_color="gray",
            anchor="w",
        ).pack(anchor="w", padx=16, pady=(0, 8))

        self.pie = PieChart(chart_frame, data=self._transactions, height=240)
        self.pie.pack(fill="x", padx=12, pady=(0, 12))

        # ── Légende ──
        legend_frame = ctk.CTkFrame(body, corner_radius=14, fg_color="#1e1e2e", width=220)
        legend_frame.pack(side="left", fill="y")
        legend_frame.pack_propagate(False)

        ctk.CTkLabel(
            legend_frame,
            text="Motifs",
            font=ctk.CTkFont(size=14, weight="bold"),
            anchor="w",
        ).pack(anchor="w", padx=16, pady=(14, 8))

        for label, value, color in self._transactions:
            pct = value / total * 100
            row = ctk.CTkFrame(legend_frame, fg_color="transparent")
            row.pack(fill="x", padx=16, pady=4)

            dot = tk.Canvas(row, width=14, height=14,
                            bg="#1e1e2e", highlightthickness=0)
            dot.pack(side="left", padx=(0, 8))
            dot.create_rectangle(2, 2, 12, 12, fill=color, outline="")

            ctk.CTkLabel(
                row, text=label,
                font=ctk.CTkFont(size=12), anchor="w",
            ).pack(side="left", expand=True, fill="x")

            ctk.CTkLabel(
                row, text=f"{pct:.1f}%",
                font=ctk.CTkFont(size=12, weight="bold"),
                text_color=color, anchor="e", width=48,
            ).pack(side="right")

        # ── Liste des transactions ──
        ctk.CTkLabel(
            self,
            text="Détail",
            font=ctk.CTkFont(size=14, weight="bold"),
            anchor="w",
        ).pack(anchor="w", pady=(20, 8))

        list_frame = ctk.CTkFrame(self, corner_radius=14, fg_color="#1e1e2e")
        list_frame.pack(fill="x")

        for i, (label, value, color) in enumerate(self._transactions):
            row = ctk.CTkFrame(list_frame, fg_color="transparent")
            row.pack(fill="x", padx=14, pady=(12 if i == 0 else 4, 4))

            dot_c = tk.Canvas(row, width=12, height=12,
                              bg="#1e1e2e", highlightthickness=0)
            dot_c.pack(side="left", padx=(0, 10))
            dot_c.create_oval(1, 1, 11, 11, fill=color, outline="")

            ctk.CTkLabel(
                row, text=label,
                font=ctk.CTkFont(size=13), anchor="w",
            ).pack(side="left", expand=True, fill="x")

            ctk.CTkLabel(
                row, text=f"-{value:,.2f} €",
                font=ctk.CTkFont(size=13, weight="bold"),
                text_color="#ef4444", anchor="e",
            ).pack(side="right")

            if i < len(self._transactions) - 1:
                ctk.CTkFrame(list_frame, height=1, fg_color="#2a2a3e").pack(
                    fill="x", padx=14, pady=(4, 0))

        ctk.CTkFrame(list_frame, height=12, fg_color="transparent").pack()