import customtkinter as ctk


class Dashboard(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, corner_radius=0, fg_color="transparent")
        self._build()

    def _build(self):
        # Titre
        ctk.CTkLabel(
            self,
            text="Dashboard",
            font=ctk.CTkFont(size=26, weight="bold"),
            anchor="w",
        ).pack(anchor="w", pady=(0, 16))

        # Cartes résumé
        cards_frame = ctk.CTkFrame(self, fg_color="transparent")
        cards_frame.pack(fill="x", pady=(0, 16))
        
        # Exemple de données pour les cartes, à remplacer par des données dynamiques réelles
        cards = [
            ("Solde total",       "$12,450.00", "#1f6aa5"),
            ("Revenus du mois",   "$5,200.00",  "#2d7a3a"),
            ("Dépenses du mois",  "$3,180.00",  "#9b3a3a"),
            
        ]
        for title, value, color in cards:
            card = ctk.CTkFrame(cards_frame, corner_radius=10)
            card.pack(side="left", expand=True, fill="both", padx=6)
            ctk.CTkLabel(
                card, text=title,
                font=ctk.CTkFont(size=12), text_color="gray"
            ).pack(anchor="w", padx=14, pady=(12, 2))
            ctk.CTkLabel(
                card, text=value,
                font=ctk.CTkFont(size=20, weight="bold"), text_color=color
            ).pack(anchor="w", padx=14, pady=(0, 12))

        # Zone graphique
        chart_box = ctk.CTkFrame(self, corner_radius=10, height=200)
        chart_box.pack(fill="x", pady=6)
        chart_box.pack_propagate(False)
        ctk.CTkLabel(
            chart_box,
            text="📉  Le graphique des dépenses s'affichera ici",
            text_color="gray",
            font=ctk.CTkFont(size=14),
        ).place(relx=0.5, rely=0.5, anchor="center")
    def refresh(self):
        # Logique de rafraichissement des donées du dashboard
        # ex: recharger les dépenses récentes, les graphiques, etc.
        # Pour l'instant, c'est juste un placeholder, mais ici tu mettra la logique pour mettre à jour les données affichées  
        pass  