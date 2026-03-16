import customtkinter as ctk

class Dasboard(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, corner_radius=0, fg_color="transparent")
        self._build()

    def _build(self):
        ctk.CTkLabel(
            self,
            text="Dashboard",
            font=ctk.CTkFont(size=24, weight="bold"),
        ).pack(pady=20)
    def refresh(self):
        # Logique de rafraichissement des donées du dashboard
        # ex: recharger les dépenses récentes, les graphiques, etc.
        # Pour l'instant, c'est juste un placeholder, mais ici tu mettra la logique pour mettre à jour les données affichées  
        pass  