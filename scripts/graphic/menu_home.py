import customtkinter as ctk


class HomeMenu(ctk.CTkFrame):
    """Page d'accueil — landing page avec boutons Login et Register."""

    def __init__(self, master, on_login, on_register):
        super().__init__(master, corner_radius=0, fg_color="transparent")
        self._on_login    = on_login
        self._on_register = on_register
        self._build()

    def _build(self):
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        container = ctk.CTkFrame(self, fg_color="transparent")
        container.grid(row=0, column=0)

        ctk.CTkLabel(
            container,
            text="💰",
            font=ctk.CTkFont(size=64),
        ).pack(pady=(0, 12))

        ctk.CTkLabel(
            container,
            text="Budget Buddy",
            font=ctk.CTkFont(size=32, weight="bold"),
        ).pack(pady=(0, 8))

        ctk.CTkLabel(
            container,
            text="Gérez vos finances en toute simplicité.",
            font=ctk.CTkFont(size=14),
            text_color="gray",
        ).pack(pady=(0, 40))

        ctk.CTkButton(
            container,
            text="Se connecter",
            height=44, width=240,
            corner_radius=22,
            font=ctk.CTkFont(size=14, weight="bold"),
            fg_color="#7c3aed",
            hover_color="#6d28d9",
            command=self._on_login,
        ).pack(pady=(0, 12))

        ctk.CTkButton(
            container,
            text="Créer un compte",
            height=44, width=240,
            corner_radius=22,
            font=ctk.CTkFont(size=14, weight="bold"),
            fg_color="transparent",
            border_width=2,
            border_color="#7c3aed",
            text_color=("gray10", "gray90"),
            hover_color=("gray85", "gray25"),
            command=self._on_register,
        ).pack()
