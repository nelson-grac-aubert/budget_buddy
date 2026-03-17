import tkinter as tk
import customtkinter as ctk
from datetime import date


# todo: remplacer les données statiques par des appels à la base de données
TRANSACTIONS = [
    ("16/04/2021", "15/04/2021", "Virement salaire avril",      None,   4.90),
    ("08/01/2021", "05/01/2021", "Remboursement frais",         None,   1.59),
    ("16/12/2020", "16/12/2020", "Paiement abonnement Netflix", 13.99,  None),
    ("14/12/2020", "11/12/2020", "Courses Carrefour",           52.30,  None),
    ("16/11/2020", "14/11/2020", "Virement ami",                None,   0.09),
    ("14/11/2020", "14/11/2020", "Restaurant Le Bistrot",       32.00,  None),
    ("11/11/2020", "11/11/2020", "Remboursement sécurité soc.", None,   6.94),
    ("01/10/2020", "01/10/2020", "Loyer octobre",              750.00,  None),
    ("03/08/2020", "02/08/2020", "Prime vacances",              None,   2.67),
    ("13/07/2020", "13/07/2020", "Pharmacie",                   18.50,  None),
    ("06/07/2020", "03/07/2020", "Freelance mission juillet",   None,   7.90),
    ("01/07/2020", "30/06/2020", "Virement salaire juillet",    None,   7.99),
]

SOLDE_DEBUT = 237.67
SOLDE_FIN   = 278.05


#  Couleurs 
COL_HEADER  = "#1a7a7a"
COL_ROW_ODD = "#1e2a2a"
COL_ROW_EVN = "#162020"
COL_BOLD    = "#0d3030"
TXT_DEBIT   = "#ef4444"
TXT_CREDIT  = "#22c55e"
TXT_HEAD    = "#ffffff"
TXT_NORMAL  = "#d1d5db"
TXT_GRAY    = "#9ca3af"


class ReleveView(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, corner_radius=0, fg_color="transparent")
        self._build()

    def _build(self):
        # ── Titre 
        ctk.CTkLabel(
            self,
            text="Relevé de compte",
            font=ctk.CTkFont(size=26, weight="bold"),
            anchor="w",
        ).pack(anchor="w", pady=(0, 14))

        # ── Filtres 
        filters = ctk.CTkFrame(self, corner_radius=10)
        filters.pack(fill="x", pady=(0, 12), ipady=10)

        # Période
        period_row = ctk.CTkFrame(filters, fg_color="transparent")
        period_row.pack(anchor="w", padx=16, pady=(10, 4))

        ctk.CTkLabel(period_row, text="Période :", font=ctk.CTkFont(size=13),
                     text_color="#2dd4bf").pack(side="left", padx=(0, 8))
        ctk.CTkLabel(period_row, text="du", font=ctk.CTkFont(size=13),
                     text_color=TXT_GRAY).pack(side="left", padx=(0, 6))

        self.date_from = ctk.CTkEntry(period_row, width=110, height=32,
                                      placeholder_text="01/07/2020",
                                      font=ctk.CTkFont(size=12))
        self.date_from.pack(side="left")
        self.date_from.insert(0, "01/07/2020")

        ctk.CTkLabel(period_row, text="au", font=ctk.CTkFont(size=13),
                     text_color=TXT_GRAY).pack(side="left", padx=8)

        self.date_to = ctk.CTkEntry(period_row, width=110, height=32,
                                    placeholder_text="22/09/2021",
                                    font=ctk.CTkFont(size=12))
        self.date_to.pack(side="left")
        self.date_to.insert(0, "22/09/2021")

        # Mode d'affichage
        mode_row = ctk.CTkFrame(filters, fg_color="transparent")
        mode_row.pack(anchor="w", padx=16, pady=(4, 10))

        ctk.CTkLabel(mode_row, text="Mode d'affichage :", font=ctk.CTkFont(size=13),
                     text_color="#2dd4bf").pack(side="left", padx=(0, 8))
        self.mode_var = ctk.StringVar(value="Mouvements")
        ctk.CTkOptionMenu(mode_row, variable=self.mode_var,
                          values=["Mouvements", "Soldes", "Résumé"],
                          width=180, height=32,
                          font=ctk.CTkFont(size=12)).pack(side="left")

        ctk.CTkButton(mode_row, text="Afficher", width=100, height=32,
                      font=ctk.CTkFont(size=13, weight="bold"),
                      fg_color="#0d9488", hover_color="#0f766e",
                      command=self._refresh).pack(side="left", padx=(20, 0))

        # ── Tableau 
        self._build_table()

    def _build_table(self):
        # Conteneur scrollable
        self.table_container = ctk.CTkScrollableFrame(
            self, corner_radius=10, fg_color="#111a1a"
        )
        self.table_container.pack(fill="both", expand=True)

        self._render_table(self.table_container)

    def _render_table(self, parent):
        # Vider
        for w in parent.winfo_children():
            w.destroy()

        cols   = ["Date d'opération", "Date de valeur", "Description", "Débit", "Crédit"]
        widths = [130, 120, 280, 80, 80]

        # ── En-tête 
        header = tk.Frame(parent, bg=COL_HEADER)
        header.pack(fill="x", padx=2, pady=(2, 0))
        for col, w in zip(cols, widths):
            tk.Label(header, text=col, bg=COL_HEADER, fg=TXT_HEAD,
                     font=("Helvetica", 11, "bold"),
                     width=w // 7, anchor="center", pady=10).pack(side="left")

        # ── Solde de fin 
        self._bold_row(parent,
                       f"Nouveau solde au {self.date_to.get()}",
                       SOLDE_FIN, is_credit=True)

        # ── Lignes 
        for i, (d_op, d_val, desc, debit, credit) in enumerate(TRANSACTIONS):
            bg = COL_ROW_ODD if i % 2 == 0 else COL_ROW_EVN
            row = tk.Frame(parent, bg=bg)
            row.pack(fill="x", padx=2)

            def cell(text, w, align="center", color=TXT_NORMAL):
                tk.Label(row, text=text, bg=bg, fg=color,
                         font=("Helvetica", 10),
                         width=w // 7, anchor=align, pady=7,
                         padx=6).pack(side="left")

            cell(d_op,  widths[0])
            cell(d_val, widths[1])
            cell(desc,  widths[2], align="w")

            if debit:
                cell(f"{debit:.2f}", widths[3], color=TXT_DEBIT)
                cell("-",            widths[4], color=TXT_GRAY)
            else:
                cell("-",             widths[3], color=TXT_GRAY)
                cell(f"{credit:.2f}", widths[4], color=TXT_CREDIT)

            # Séparateur
            tk.Frame(parent, bg="#2d3a3a", height=1).pack(fill="x", padx=2)

        # ── Solde de début 
        self._bold_row(parent,
                       f"Ancien solde au {self.date_from.get()}",
                       SOLDE_DEBUT, is_credit=True)

    def _bold_row(self, parent, label, amount, is_credit=True):
        row = tk.Frame(parent, bg=COL_BOLD)
        row.pack(fill="x", padx=2)
        tk.Label(row, text=label, bg=COL_BOLD, fg=TXT_HEAD,
                 font=("Helvetica", 11, "bold"),
                 anchor="w", padx=10, pady=10).pack(side="left", expand=True, fill="x")
        color = TXT_CREDIT if is_credit else TXT_DEBIT
        tk.Label(row, text=f"{amount:.2f}", bg=COL_BOLD, fg=color,
                 font=("Helvetica", 11, "bold"),
                 anchor="e", padx=16, pady=10, width=10).pack(side="right")

    def _refresh(self):
        # Reconstruire le tableau 
        for w in self.table_container.winfo_children():
            w.destroy()
        self._render_table(self.table_container)