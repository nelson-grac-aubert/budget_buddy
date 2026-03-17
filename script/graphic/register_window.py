import customtkinter as ctk


class RegisterWindow(ctk.CTkFrame):
    """Formulaire d'inscription."""

    def __init__(self, master, on_register, on_back):
        super().__init__(master, corner_radius=0, fg_color="transparent")
        self._on_register = on_register
        self._on_back     = on_back
        self._build()

    def _build(self):
        container = ctk.CTkFrame(self, width=360, height=500, corner_radius=16)
        container.place(relx=0.5, rely=0.5, anchor="center")
        container.pack_propagate(False)

        ctk.CTkLabel(
            container,
            text="💰 Budget Buddy",
            font=ctk.CTkFont(size=26, weight="bold"),
        ).pack(pady=(36, 4))

        ctk.CTkLabel(
            container,
            text="Créez votre compte",
            font=ctk.CTkFont(size=13),
            text_color="gray",
        ).pack(pady=(0, 24))

        ctk.CTkLabel(container, text="Nom d'utilisateur", anchor="w",
                     font=ctk.CTkFont(size=13)).pack(fill="x", padx=32)
        self.username_entry = ctk.CTkEntry(
            container, placeholder_text="Jean Dupont", height=38)
        self.username_entry.pack(fill="x", padx=32, pady=(4, 14))

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
            text="S'inscrire",
            height=42,
            font=ctk.CTkFont(size=14, weight="bold"),
            command=self._handle_register,
        ).pack(fill="x", padx=32)

        ctk.CTkButton(
            container,
            text="← Retour",
            fg_color="transparent",
            text_color="gray",
            hover_color=("gray85", "gray25"),
            font=ctk.CTkFont(size=12),
            command=self._on_back,
        ).pack(pady=(12, 24))

    def _handle_register(self):
        username = self.username_entry.get()
        email    = self.email_entry.get()
        password = self.password_entry.get()
        # TODO : ajouter la logique d'inscription
        print(f"Register: {username} / {email}")
        self._on_register()