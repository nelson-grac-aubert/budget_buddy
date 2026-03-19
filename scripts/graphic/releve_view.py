import tkinter as tk
import customtkinter as ctk
from datetime import datetime
from scripts.graphic.transaction_utils import (
    col, categories, categories_depot, types, tris, parse_date
)


class ReleveView(ctk.CTkFrame):
    def __init__(self, master, on_back, transactions):
        super().__init__(master, corner_radius=0, fg_color="transparent")
        self._on_back  = on_back
        self._all_data = transactions
        self._build()

    def _build(self):
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

        filters = ctk.CTkFrame(self, corner_radius=10)
        filters.pack(fill="x", pady=(0, 10), ipady=6)

        row1 = ctk.CTkFrame(filters, fg_color="transparent")
        row1.pack(fill="x", padx=14, pady=(10, 4))

        ctk.CTkLabel(row1, text="🔍", font=ctk.CTkFont(size=14)).pack(side="left", padx=(0, 4))
        self.search_var = ctk.StringVar()
        ctk.CTkEntry(row1, textvariable=self.search_var,
                     placeholder_text="Rechercher une description...",
                     width=220, height=32,
                     font=ctk.CTkFont(size=12)).pack(side="left", padx=(0, 16))

        ctk.CTkLabel(row1, text="Du", font=ctk.CTkFont(size=12),
                     text_color=col("gray")).pack(side="left", padx=(0, 4))
        self.date_from = ctk.CTkEntry(row1, width=100, height=32,
                                      placeholder_text="jj/mm/aaaa",
                                      font=ctk.CTkFont(size=12))
        self.date_from.pack(side="left")

        ctk.CTkLabel(row1, text="Au", font=ctk.CTkFont(size=12),
                     text_color=col("gray")).pack(side="left", padx=6)
        self.date_to = ctk.CTkEntry(row1, width=100, height=32,
                                    placeholder_text="jj/mm/aaaa",
                                    font=ctk.CTkFont(size=12))
        self.date_to.pack(side="left")

        row2 = ctk.CTkFrame(filters, fg_color="transparent")
        row2.pack(fill="x", padx=14, pady=(4, 10))

        ctk.CTkLabel(row2, text="Catégorie :", font=ctk.CTkFont(size=12),
                     text_color=col("gray")).pack(side="left", padx=(0, 4))
        self.cat_var = ctk.StringVar(value="Toutes")
        ctk.CTkOptionMenu(row2, variable=self.cat_var,
                          values=["Toutes"] + categories_depot() + categories()[1:],
                          width=130, height=32,
                          font=ctk.CTkFont(size=12)).pack(side="left", padx=(0, 12))

        ctk.CTkLabel(row2, text="Type :", font=ctk.CTkFont(size=12),
                     text_color=col("gray")).pack(side="left", padx=(0, 4))
        self.type_var = ctk.StringVar(value="Tous")
        ctk.CTkOptionMenu(row2, variable=self.type_var, values=types(),
                          width=100, height=32,
                          font=ctk.CTkFont(size=12)).pack(side="left", padx=(0, 12))

        ctk.CTkLabel(row2, text="Trier par :", font=ctk.CTkFont(size=12),
                     text_color=col("gray")).pack(side="left", padx=(0, 4))
        self.sort_var = ctk.StringVar(value="Date ↓")
        ctk.CTkOptionMenu(row2, variable=self.sort_var, values=tris(),
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

        self.count_label = ctk.CTkLabel(self, text="",
                                        font=ctk.CTkFont(size=12),
                                        text_color=col("gray"))
        self.count_label.pack(anchor="w", padx=4, pady=(0, 4))

        # Conteneur avec scroll vertical ET horizontal
        canvas_frame = tk.Frame(self, bg="#111a1a")
        canvas_frame.pack(fill="both", expand=True)

        self._canvas = tk.Canvas(canvas_frame, bg="#111a1a", highlightthickness=0)
        vscroll = tk.Scrollbar(canvas_frame, orient="vertical", command=self._canvas.yview)
        hscroll = tk.Scrollbar(canvas_frame, orient="horizontal", command=self._canvas.xview)

        self._canvas.configure(yscrollcommand=vscroll.set, xscrollcommand=hscroll.set)

        vscroll.pack(side="right", fill="y")
        hscroll.pack(side="bottom", fill="x")
        self._canvas.pack(side="left", fill="both", expand=True)

        self.table_container = tk.Frame(self._canvas, bg="#111a1a")
        self._canvas_window = self._canvas.create_window((0, 0), window=self.table_container, anchor="nw")

        def _on_frame_configure(e):
            self._canvas.configure(scrollregion=self._canvas.bbox("all"))

        def _on_canvas_configure(e):
            self._canvas.itemconfig(self._canvas_window, width=max(e.width, self.table_container.winfo_reqwidth()))

        self.table_container.bind("<Configure>", _on_frame_configure)
        self._canvas.bind("<Configure>", _on_canvas_configure)

        def _on_mousewheel(e):
            self._canvas.yview_scroll(int(-1 * (e.delta / 120)), "units")
        self._canvas.bind_all("<MouseWheel>", _on_mousewheel)

        self._refresh()

    def _get_filtered_sorted(self):
        data = list(self._all_data)

        search = self.search_var.get().strip().lower()
        if search:
            data = [t for t in data if search in t["description"].lower()]

        cat = self.cat_var.get()
        if cat != "Toutes":
            data = [t for t in data if t["categorie"] == cat]

        typ = self.type_var.get()
        if typ != "Tous":
            data = [t for t in data if t["type"] == typ]

        df = self.date_from.get().strip()
        dt = self.date_to.get().strip()
        if df:
            try:
                d_from = datetime.strptime(df, "%d/%m/%Y")
                data = [t for t in data if parse_date(t["date"]) >= d_from]
            except ValueError:
                pass
        if dt:
            try:
                d_to = datetime.strptime(dt, "%d/%m/%Y")
                data = [t for t in data if parse_date(t["date"]) <= d_to]
            except ValueError:
                pass

        sort = self.sort_var.get()
        if sort == "Date ↓":
            data.sort(key=lambda t: parse_date(t["date"]), reverse=True)
        elif sort == "Date ↑":
            data.sort(key=lambda t: parse_date(t["date"]))
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

        cols   = ["Référence", "Date", "Description", "Catégorie", "Type", "Montant"]
        widths = [120, 90, 240, 110, 80, 90]

        header = tk.Frame(self.table_container, bg=col("header"))
        header.pack(fill="x", padx=2, pady=(2, 0))
        for c, w in zip(cols, widths):
            tk.Label(header, text=c, bg=col("header"), fg=col("head"),
                     font=("Helvetica", 11, "bold"),
                     width=w // 7, anchor="w", pady=10).pack(side="left")

        if not data:
            tk.Label(self.table_container,
                     text="Aucune transaction ne correspond aux critères.",
                     bg="#111a1a", fg=col("gray"),
                     font=("Helvetica", 12), pady=30).pack()
            return

        for i, t in enumerate(data):
            bg   = col("row_odd") if i % 2 == 0 else col("row_even")
            row  = tk.Frame(self.table_container, bg=bg)
            row.pack(fill="x", padx=2)
            sign = "+" if t["montant"] >= 0 else ""

            def cell(text, w, align="w", fg=None, _bg=bg):
                tk.Label(row, text=text, bg=_bg, fg=fg or col("normal"),
                         font=("Helvetica", 10),
                         width=w // 7, anchor=align,
                         pady=8, padx=6).pack(side="left")

            cell(t["reference"],   widths[0])
            cell(t["date"],        widths[1])
            cell(t["description"], widths[2])
            cell(t["categorie"],   widths[3])
            cell(t["type"],        widths[4],
                fg=col("credit") if t["type"] == "Crédit" else col("debit"))
            cell(f"{sign}{t['montant']:,.2f} €", widths[5],
                fg=col("credit") if t["montant"] >= 0 else col("debit"))


            tk.Frame(self.table_container, bg="#2d3a3a", height=1).pack(fill="x", padx=2)

        total_debit  = sum(abs(t["montant"]) for t in data if t["montant"] < 0)
        total_credit = sum(t["montant"]      for t in data if t["montant"] >= 0)
        summary = tk.Frame(self.table_container, bg=col("bold"))
        summary.pack(fill="x", padx=2, pady=(4, 0))
        tk.Label(summary, text="Total", bg=col("bold"), fg=col("head"),
                 font=("Helvetica", 11, "bold"), anchor="w",
                 padx=10, pady=10).pack(side="left", expand=True, fill="x")
        tk.Label(summary, text=f"Débits : -{total_debit:,.2f} €",
                 bg=col("bold"), fg=col("debit"),
                 font=("Helvetica", 10, "bold"), padx=12, pady=10).pack(side="left")
        tk.Label(summary, text=f"Crédits : +{total_credit:,.2f} €",
                 bg=col("bold"), fg=col("credit"),
                 font=("Helvetica", 10, "bold"), padx=12, pady=10).pack(side="left")

    def _reset_filters(self):
        self.search_var.set("")
        self.date_from.delete(0, "end")
        self.date_to.delete(0, "end")
        self.cat_var.set("Toutes")
        self.type_var.set("Tous")
        self.sort_var.set("Date ↓")
        self._refresh()