import customtkinter as ctk


USER_NAME = "Alexandre Dupont"


class HomeMenu(ctk.CTkFrame):
    """Écran d'accueil après connexion — message de bienvenue personnalisé."""

    def __init__(self, master, on_dashboard):
        super().__init__(master, corner_radius=0, fg_color="transparent")
        self._on_dashboard = on_dashboard
        self._build()

    def _build(self):
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        container = ctk.CTkFrame(self, fg_color="transparent")
        container.grid(row=0, column=0)

        # Logo
        ctk.CTkLabel(
            container,
            text="💰",
            font=ctk.CTkFont(size=56),
        ).pack(pady=(0, 12))

        # Titre
        ctk.CTkLabel(
            container,
            text=f"Bonjour, {USER_NAME} 👋",
            font=ctk.CTkFont(size=28, weight="bold"),
        ).pack(pady=(0, 8))

        # Sous-titre
        ctk.CTkLabel(
            container,
            text="Bienvenue sur Budget Buddy.\nConsultez votre dashboard pour un aperçu de vos finances.",
            font=ctk.CTkFont(size=14),
            text_color="gray",
            justify="center",
        ).pack(pady=(0, 32))

        # Bouton CTA
        ctk.CTkButton(
            container,
            text="Voir mon Dashboard →",
            height=44,
            width=220,
            corner_radius=22,
            font=ctk.CTkFont(size=14, weight="bold"),
            fg_color="#7c3aed",
            hover_color="#6d28d9",
            command=self._on_dashboard,
        ).pack()