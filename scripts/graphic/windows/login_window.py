import customtkinter as ctk
from scripts.logic.app.login_register import handle_login


class HomeWindow(ctk.CTkFrame):
    """Formulaire de connexion."""

    def __init__(self, master, on_login, on_register, on_back):
        super().__init__(master, corner_radius=0, fg_color="transparent")
        self._on_login    = on_login
        self._on_register = on_register
        self._on_back     = on_back
        self._pwd_visible = False
        self._build()

    def _build(self):
        container = ctk.CTkFrame(self, width=360, height=460, corner_radius=16)
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

        # Email
        ctk.CTkLabel(container, text="Email", anchor="w",
                     font=ctk.CTkFont(size=13)).pack(fill="x", padx=32)
        self.email_entry = ctk.CTkEntry(
            container, placeholder_text="exemple@email.com", height=38)
        self.email_entry.pack(fill="x", padx=32, pady=(4, 14))
        

        # Mot de passe
        ctk.CTkLabel(container, text="Mot de passe", anchor="w",
                     font=ctk.CTkFont(size=13)).pack(fill="x", padx=32)

        pwd_row = ctk.CTkFrame(container, fg_color="transparent")
        pwd_row.pack(fill="x", padx=32, pady=(4, 8))

        self.password_entry = ctk.CTkEntry(
            pwd_row, placeholder_text="••••••••", show="•", height=38)
        self.password_entry.pack(side="left", fill="x", expand=True)

        self.eye_btn = ctk.CTkButton(
            pwd_row,
            text="🙈",
            width=38, height=38,
            corner_radius=8,
            fg_color="transparent",
            hover_color=("gray85", "gray25"),
            font=ctk.CTkFont(size=16),
            command=self._toggle_password,
        )
        self.eye_btn.pack(side="left", padx=(4, 0))

        # Label d'erreur
        self.error_label = ctk.CTkLabel(
            container, text="",
            font=ctk.CTkFont(size=11),
            text_color="#ef4444",
            anchor="w",
        )
        self.error_label.pack(fill="x", padx=32, pady=(0, 16))

        # Connexion
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

    def _toggle_password(self):
        self._pwd_visible = not self._pwd_visible
        self.password_entry.configure(show="" if self._pwd_visible else "•")
        self.eye_btn.configure(text="👁" if self._pwd_visible else "🙈")

    def _handle_login(self):
        email    = self.email_entry.get().strip()
        password = self.password_entry.get()

        result = handle_login(email, password)

        # Échec — 2 valeurs
        if not result[0]:
            self.error_label.configure(text=f"⚠  {result[1]}")
            return

        # Succès — 4 valeurs : True, message, user_id, user_type
        _, _, user_id, user_type = result

        self.error_label.configure(text="")
        self._on_login(user_id, is_admin=(user_type == "admin"))