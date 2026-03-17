import tkinter as tk
import customtkinter as ctk
from scripts.graphic.pie_chart import PieChart
from datetime import datetime


# TODO : remplacer par get_transactions(user_id) quand data.py sera prêt
def get_transactions(user_id=1):
    """
    Retourne une liste de dict :
    { date, description, categorie, type, montant (négatif=débit, positif=crédit) }
    """
    return [
        {"date": "14/12/2020", "description": "Courses Carrefour",        "categorie": "Courses",      "type": "Débit",  "montant": -52.30},
        {"date": "14/11/2020", "description": "Restaurant Le Bistrot",    "categorie": "Restaurants",  "type": "Débit",  "montant": -32.00},
        {"date": "01/10/2020", "description": "Loyer octobre",            "categorie": "Loyer",        "type": "Débit",  "montant": -750.00},
        {"date": "13/07/2020", "description": "Pharmacie",                "categorie": "Santé",        "type": "Débit",  "montant": -18.50},
        {"date": "16/12/2020", "description": "Paiement Netflix",         "categorie": "Abonnements",  "type": "Débit",  "montant": -13.99},
        {"date": "01/07/2020", "description": "Virement salaire juillet", "categorie": "Salaire",      "type": "Crédit", "montant":  1800.00},
        {"date": "16/04/2021", "description": "Virement salaire avril",   "categorie": "Salaire",      "type": "Crédit", "montant":  1800.00},
        {"date": "08/01/2021", "description": "Remboursement frais",      "categorie": "Santé",        "type": "Crédit", "montant":  45.00},
        {"date": "06/07/2020", "description": "Freelance mission",        "categorie": "Revenus",      "type": "Crédit", "montant":  320.00},
        {"date": "16/11/2020", "description": "Virement ami",             "categorie": "Loisirs",      "type": "Crédit", "montant":  20.00},
        {"date": "03/08/2020", "description": "Prime vacances",           "categorie": "Revenus",      "type": "Crédit", "montant":  150.00},
        {"date": "11/11/2020", "description": "Remboursement sécu.",      "categorie": "Santé",        "type": "Crédit", "montant":  6.94},
        {"date": "15/03/2021", "description": "Cinéma UGC",              "categorie": "Loisirs",      "type": "Débit",  "montant": -22.00},
        {"date": "20/02/2021", "description": "Essence Total",            "categorie": "Transport",    "type": "Débit",  "montant": -60.00},
        {"date": "05/01/2021", "description": "Abonnement Spotify",       "categorie": "Abonnements",  "type": "Débit",  "montant": -9.99},
    ]


# ── Constantes visuelles ─────────────────────────────────────────────────── #

COL_HEADER  = "#1a7a7a"
COL_ROW_ODD = "#1e2a2a"
COL_ROW_EVN = "#162020"
COL_BOLD    = "#0d3030"
TXT_DEBIT   = "#ef4444"
TXT_CREDIT  = "#22c55e"
TXT_HEAD    = "#ffffff"
TXT_NORMAL  = "#d1d5db"
TXT_GRAY    = "#9ca3af"

CATEGORIES  = ["Toutes", "Loyer", "Courses", "Restaurants", "Abonnements",
                "Transport", "Santé", "Loisirs", "Salaire", "Revenus"]
TYPES       = ["Tous", "Débit", "Crédit"]
TRIS        = ["Date ↓", "Date ↑", "Montant ↓", "Montant ↑"]

PIE_COLORS  = {
    "Loyer":       "#7c3aed",
    "Courses":     "#0d9488",
    "Restaurants": "#f59e0b",
    "Abonnements": "#3b82f6",
    "Transport":   "#ef4444",
    "Santé":       "#22c55e",
    "Loisirs":     "#ec4899",
    "Salaire":     "#6366f1",
    "Revenus":     "#14b8a6",
}


def _parse_date(s):
    try:
        return datetime.strptime(s, "%d/%m/%Y")
    except Exception:
        return datetime.min


# ── Vue relevé ───────────────────────────────────────────────────────────── #

class _ReleveView(ctk.CTkFrame):
    def __init__(self, master, on_back, transactions):
        super().__init__(master, corner_radius=0, fg_color="transparent")
        self._on_back     = on_back
        self._all_data    = transactions
        self._build()

    def _build(self):
        # Barre du haut
        top = ctk.CTkFrame(self, fg_color="transparent")
        top.pack(fill="x", pady=(0, 10))

        ctk.CTkButton(
            top, text="< Retour", width=100, height=32,
            fg_color="transparent", border_width=2,
            text_color=("gray10", "gray90"),
            font=ctk.CTkFont(size=13),
            command=self._on_back,
        ).pack(side="left")

        ctk.CTkLabel(
            top, text="Relevé de compte",
            font=ctk.CTkFont(size=22, weight="bold"),
        ).pack(side="left", padx=20)

        # ── Panneau de filtres ──
        filters = ctk.CTkFrame(self, corner_radius=10)
        filters.pack(fill="x", pady=(0, 10), ipady=6)

        # Ligne 1 : recherche texte + période
        row1 = ctk.CTkFrame(filters, fg_color="transparent")
        row1.pack(fill="x", padx=14, pady=(10, 4))

        ctk.CTkLabel(row1, text="🔍", font=ctk.CTkFont(size=14)).pack(side="left", padx=(0, 4))
        self.search_var = ctk.StringVar()
        ctk.CTkEntry(row1, textvariable=self.search_var,
                     placeholder_text="Rechercher une description...",
                     width=220, height=32,
                     font=ctk.CTkFont(size=12)).pack(side="left", padx=(0, 16))

        ctk.CTkLabel(row1, text="Du", font=ctk.CTkFont(size=12),
                     text_color=TXT_GRAY).pack(side="left", padx=(0, 4))
        self.date_from = ctk.CTkEntry(row1, width=100, height=32,
                                      placeholder_text="jj/mm/aaaa",
                                      font=ctk.CTkFont(size=12))
        self.date_from.pack(side="left")

        ctk.CTkLabel(row1, text="Au", font=ctk.CTkFont(size=12),
                     text_color=TXT_GRAY).pack(side="left", padx=6)
        self.date_to = ctk.CTkEntry(row1, width=100, height=32,
                                    placeholder_text="jj/mm/aaaa",
                                    font=ctk.CTkFont(size=12))
        self.date_to.pack(side="left")

        # Ligne 2 : catégorie + type + tri + bouton
        row2 = ctk.CTkFrame(filters, fg_color="transparent")
        row2.pack(fill="x", padx=14, pady=(4, 10))

        ctk.CTkLabel(row2, text="Catégorie :", font=ctk.CTkFont(size=12),
                     text_color=TXT_GRAY).pack(side="left", padx=(0, 4))
        self.cat_var = ctk.StringVar(value="Toutes")
        ctk.CTkOptionMenu(row2, variable=self.cat_var, values=CATEGORIES,
                          width=130, height=32,
                          font=ctk.CTkFont(size=12)).pack(side="left", padx=(0, 12))

        ctk.CTkLabel(row2, text="Type :", font=ctk.CTkFont(size=12),
                     text_color=TXT_GRAY).pack(side="left", padx=(0, 4))
        self.type_var = ctk.StringVar(value="Tous")
        ctk.CTkOptionMenu(row2, variable=self.type_var, values=TYPES,
                          width=100, height=32,
                          font=ctk.CTkFont(size=12)).pack(side="left", padx=(0, 12))

        ctk.CTkLabel(row2, text="Trier par :", font=ctk.CTkFont(size=12),
                     text_color=TXT_GRAY).pack(side="left", padx=(0, 4))
        self.sort_var = ctk.StringVar(value="Date ↓")
        ctk.CTkOptionMenu(row2, variable=self.sort_var, values=TRIS,
                          width=120, height=32,
                          font=ctk.CTkFont(size=12)).pack(side="left", padx=(0, 16))

        ctk.CTkButton(row2, text="Appliquer", width=100, height=32,
                      font=ctk.CTkFont(size=13, weight="bold"),
                      fg_color="#0d9488", hover_color="#0f766e",
                      command=self._refresh).pack(side="left")

        ctk.CTkButton(row2, text="Réinitialiser", width=110, height=32,
                      fg_color="transparent", border_width=2,
                      text_color=("gray10", "gray90"),
                      font=ctk.CTkFont(size=12),
                      command=self._reset_filters).pack(side="left", padx=(8, 0))

        # Compteur résultats
        self.count_label = ctk.CTkLabel(self, text="",
                                        font=ctk.CTkFont(size=12), text_color=TXT_GRAY)
        self.count_label.pack(anchor="w", padx=4, pady=(0, 4))

        # Tableau scrollable
        self.table_container = ctk.CTkScrollableFrame(
            self, corner_radius=10, fg_color="#111a1a")
        self.table_container.pack(fill="both", expand=True)

        self._refresh()

    def _get_filtered_sorted(self):
        data = list(self._all_data)

        # Filtre texte
        search = self.search_var.get().strip().lower()
        if search:
            data = [t for t in data if search in t["description"].lower()]

        # Filtre catégorie
        cat = self.cat_var.get()
        if cat != "Toutes":
            data = [t for t in data if t["categorie"] == cat]

        # Filtre type
        typ = self.type_var.get()
        if typ != "Tous":
            data = [t for t in data if t["type"] == typ]

        # Filtre dates
        df = self.date_from.get().strip()
        dt = self.date_to.get().strip()
        if df:
            try:
                d_from = datetime.strptime(df, "%d/%m/%Y")
                data = [t for t in data if _parse_date(t["date"]) >= d_from]
            except ValueError:
                pass
        if dt:
            try:
                d_to = datetime.strptime(dt, "%d/%m/%Y")
                data = [t for t in data if _parse_date(t["date"]) <= d_to]
            except ValueError:
                pass

        # Tri
        sort = self.sort_var.get()
        if sort == "Date ↓":
            data.sort(key=lambda t: _parse_date(t["date"]), reverse=True)
        elif sort == "Date ↑":
            data.sort(key=lambda t: _parse_date(t["date"]))
        elif sort == "Montant ↓":
            data.sort(key=lambda t: t["montant"])
        elif sort == "Montant ↑":
            data.sort(key=lambda t: t["montant"], reverse=True)

        return data

    def _refresh(self):
        for w in self.table_container.winfo_children():
            w.destroy()

        data = self._get_filtered_sorted()
        self.count_label.configure(text=f"{len(data)} transaction(s) trouvée(s)")

        cols   = ["Date", "Description", "Catégorie", "Type", "Montant"]
        widths = [90, 240, 110, 80, 90]

        # En-tête
        header = tk.Frame(self.table_container, bg=COL_HEADER)
        header.pack(fill="x", padx=2, pady=(2, 0))
        for col, w in zip(cols, widths):
            tk.Label(header, text=col, bg=COL_HEADER, fg=TXT_HEAD,
                     font=("Helvetica", 11, "bold"),
                     width=w // 7, anchor="center", pady=10).pack(side="left")

        if not data:
            tk.Label(self.table_container,
                     text="Aucune transaction ne correspond aux critères.",
                     bg="#111a1a", fg=TXT_GRAY,
                     font=("Helvetica", 12), pady=30).pack()
            return

        for i, t in enumerate(data):
            bg    = COL_ROW_ODD if i % 2 == 0 else COL_ROW_EVN
            row   = tk.Frame(self.table_container, bg=bg)
            row.pack(fill="x", padx=2)
            color = TXT_CREDIT if t["montant"] >= 0 else TXT_DEBIT
            sign  = "+" if t["montant"] >= 0 else ""

            def cell(text, w, align="center", fg=TXT_NORMAL, _bg=bg):
                tk.Label(row, text=text, bg=_bg, fg=fg,
                         font=("Helvetica", 10),
                         width=w // 7, anchor=align,
                         pady=8, padx=6).pack(side="left")

            cell(t["date"],        widths[0])
            cell(t["description"], widths[1], align="w")
            cell(t["categorie"],   widths[2])
            cell(t["type"],        widths[3],
                 fg=TXT_CREDIT if t["type"] == "Crédit" else TXT_DEBIT)
            cell(f"{sign}{t['montant']:,.2f} €", widths[4], fg=color)

            tk.Frame(self.table_container, bg="#2d3a3a", height=1).pack(fill="x", padx=2)

        # Totaux
        total_debit  = sum(abs(t["montant"]) for t in data if t["montant"] < 0)
        total_credit = sum(t["montant"]      for t in data if t["montant"] >= 0)
        summary = tk.Frame(self.table_container, bg=COL_BOLD)
        summary.pack(fill="x", padx=2, pady=(4, 0))
        tk.Label(summary, text="Total", bg=COL_BOLD, fg=TXT_HEAD,
                 font=("Helvetica", 11, "bold"), anchor="w",
                 padx=10, pady=10).pack(side="left", expand=True, fill="x")
        tk.Label(summary, text=f"Débits : -{total_debit:,.2f} €",
                 bg=COL_BOLD, fg=TXT_DEBIT,
                 font=("Helvetica", 10, "bold"), padx=12, pady=10).pack(side="left")
        tk.Label(summary, text=f"Crédits : +{total_credit:,.2f} €",
                 bg=COL_BOLD, fg=TXT_CREDIT,
                 font=("Helvetica", 10, "bold"), padx=12, pady=10).pack(side="left")

    def _reset_filters(self):
        self.search_var.set("")
        self.date_from.delete(0, "end")
        self.date_to.delete(0, "end")
        self.cat_var.set("Toutes")
        self.type_var.set("Tous")
        self.sort_var.set("Date ↓")
        self._refresh()


#  Vue principale transactions 

class TransactionWindow(ctk.CTkFrame):
    """Vue transactions avec camembert + filtres + relevé."""

    def __init__(self, master, user_id: int = 1):
        super().__init__(master, corner_radius=0, fg_color="transparent")
        self._all_transactions = get_transactions(user_id)
        self._build()

    def _build(self):
        self._show_transactions()

    def _clear(self):
        for w in self.winfo_children():
            w.destroy()

    def _show_transactions(self):
        self._clear()

        # Scroll global
        scroll = ctk.CTkScrollableFrame(self, corner_radius=0, fg_color="transparent")
        scroll.pack(fill="both", expand=True)

        # Titre
        ctk.CTkLabel(scroll, text="Transactions",
                     font=ctk.CTkFont(size=26, weight="bold"),
                     anchor="w").pack(anchor="w", pady=(0, 14))

        # ── Camembert ──
        debits = [(t["categorie"], abs(t["montant"]), PIE_COLORS.get(t["categorie"], "#888"))
                  for t in self._all_transactions if t["montant"] < 0]

        body = ctk.CTkFrame(scroll, fg_color="transparent")
        body.pack(fill="x", pady=(0, 16))

        chart_frame = ctk.CTkFrame(body, corner_radius=14, fg_color="#1e1e2e")
        chart_frame.pack(side="left", fill="both", expand=True, padx=(0, 12))

        total = sum(v for _, v, _ in debits)
        ctk.CTkLabel(chart_frame, text="Répartition des dépenses",
                     font=ctk.CTkFont(size=14, weight="bold"), anchor="w"
                     ).pack(anchor="w", padx=16, pady=(14, 4))
        ctk.CTkLabel(chart_frame, text=f"Total dépenses : {total:,.2f} €",
                     font=ctk.CTkFont(size=12), text_color="gray", anchor="w"
                     ).pack(anchor="w", padx=16, pady=(0, 8))

        self.pie = PieChart(chart_frame, data=debits, height=220)
        self.pie.pack(fill="x", padx=12, pady=(0, 12))

        # Légende
        legend_frame = ctk.CTkFrame(body, corner_radius=14, fg_color="#1e1e2e", width=210)
        legend_frame.pack(side="left", fill="y")
        legend_frame.pack_propagate(False)
        ctk.CTkLabel(legend_frame, text="Catégories",
                     font=ctk.CTkFont(size=14, weight="bold"), anchor="w"
                     ).pack(anchor="w", padx=16, pady=(14, 8))

        seen = {}
        for cat, val, color in debits:
            seen[cat] = seen.get(cat, 0) + val
        for cat, val in seen.items():
            pct = val / total * 100
            row = ctk.CTkFrame(legend_frame, fg_color="transparent")
            row.pack(fill="x", padx=16, pady=3)
            dot = tk.Canvas(row, width=12, height=12,
                            bg="#1e1e2e", highlightthickness=0)
            dot.pack(side="left", padx=(0, 8))
            dot.create_rectangle(2, 2, 10, 10,
                                 fill=PIE_COLORS.get(cat, "#888"), outline="")
            ctk.CTkLabel(row, text=cat, font=ctk.CTkFont(size=12),
                         anchor="w").pack(side="left", expand=True, fill="x")
            ctk.CTkLabel(row, text=f"{pct:.1f}%",
                         font=ctk.CTkFont(size=12, weight="bold"),
                         text_color=PIE_COLORS.get(cat, "#888"),
                         anchor="e", width=44).pack(side="right")

        # ── Liste récente ──
        ctk.CTkLabel(scroll, text="Transactions récentes",
                     font=ctk.CTkFont(size=14, weight="bold"), anchor="w"
                     ).pack(anchor="w", pady=(4, 8))

        list_frame = ctk.CTkFrame(scroll, corner_radius=14, fg_color="#1e1e2e")
        list_frame.pack(fill="x")

        recent = sorted(self._all_transactions,
                        key=lambda t: _parse_date(t["date"]), reverse=True)[:8]

        for i, t in enumerate(recent):
            row = ctk.CTkFrame(list_frame, fg_color="transparent")
            row.pack(fill="x", padx=14, pady=(10 if i == 0 else 4, 4))

            color = PIE_COLORS.get(t["categorie"], "#888")
            dot_c = tk.Canvas(row, width=12, height=12,
                              bg="#1e1e2e", highlightthickness=0)
            dot_c.pack(side="left", padx=(0, 10))
            dot_c.create_oval(1, 1, 11, 11, fill=color, outline="")

            ctk.CTkLabel(row, text=t["description"],
                         font=ctk.CTkFont(size=13), anchor="w"
                         ).pack(side="left", expand=True, fill="x")
            ctk.CTkLabel(row, text=t["date"],
                         font=ctk.CTkFont(size=11), text_color="gray",
                         anchor="e", width=80).pack(side="left")

            sign     = "+" if t["montant"] >= 0 else ""
            amt_col  = TXT_CREDIT if t["montant"] >= 0 else TXT_DEBIT
            ctk.CTkLabel(row, text=f"{sign}{t['montant']:,.2f} €",
                         font=ctk.CTkFont(size=13, weight="bold"),
                         text_color=amt_col, anchor="e", width=100
                         ).pack(side="right")

            if i < len(recent) - 1:
                ctk.CTkFrame(list_frame, height=1, fg_color="#2a2a3e").pack(
                    fill="x", padx=14, pady=(4, 0))

        ctk.CTkFrame(list_frame, height=10, fg_color="transparent").pack()