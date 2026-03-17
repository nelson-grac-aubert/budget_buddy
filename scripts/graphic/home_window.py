import customtkinter as ctk


class HomeWindow(ctk.CTkFrame):
    """Formulaire de connexion."""

    def __init__(self, master, on_login, on_register, on_back):
        super().__init__(master, corner_radius=0, fg_color="transparent")
        self._on_login    = on_login
        self._on_register = on_register
        self._on_back     = on_back
        self._build()

    def _build(self):
        container = ctk.CTkFrame(self, width=360, height=440, corner_radius=16)
        container.place(relx=0.5, rely=0.5, anchor="center")
        container.pack_propagate(False)

        ctk.CTkLabel(
            container,
            text="💰 Budget Buddy",
            font=ctk.CTkFont(size=26, weight="bold"),
        ).pack(pady=(36, 4))

        ctk.CTkLabel(
            container,
            text="Connectez-vous à votre compte",
            font=ctk.CTkFont(size=13),
            text_color="gray",
        ).pack(pady=(0, 24))

        ctk.CTkLabel(container, text="Email", anchor="w",
                     font=ctk.CTkFont(size=13)).pack(fill="x", padx=32)
        self.email_entry = ctk.CTkEntry(
            container, placeholder_text="exemple@email.com", height=38)
        self.email_entry.pack(fill="x", padx=32, pady=(4, 14))

        ctk.CTkLabel(container, text="Mot de passe", anchor="w",
                     font=ctk.CTkFont(size=13)).pack(fill="x", padx=32)
        self.password_entry = ctk.CTkEntry(
            container, placeholder_text="••••••••", show="•", height=38)
        self.password_entry.pack(fill="x", padx=32, pady=(4, 24))

        ctk.CTkButton(
            container,
            text="Se connecter",
            height=42,
            font=ctk.CTkFont(size=14, weight="bold"),
            command=self._handle_login,
        ).pack(fill="x", padx=32)

        ctk.CTkButton(
            container,
            text="Pas encore de compte ? S'inscrire",
            fg_color="transparent",
            text_color="gray",
            hover_color=("gray85", "gray25"),
            font=ctk.CTkFont(size=12),
            command=self._on_register,
        ).pack(pady=(8, 0))

        ctk.CTkButton(
            container,
            text="← Retour",
            fg_color="transparent",
            text_color="gray",
            hover_color=("gray85", "gray25"),
            font=ctk.CTkFont(size=12),
            command=self._on_back,
        ).pack(pady=(4, 16))

    def _handle_login(self):
        email    = self.email_entry.get()
        password = self.password_entry.get()
        # TODO : ajouter la logique d'authentification
        print(f"Login: {email}")
        self._on_login()