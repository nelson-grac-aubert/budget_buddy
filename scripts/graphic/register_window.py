import customtkinter as ctk
from scripts.logic.login_register import handle_register   # ← liaison interne


class RegisterWindow(ctk.CTkFrame):
    """Formulaire d'inscription avec validation du mot de passe."""

    _RULES = [
        ("min10",   "10 caractères minimum"),
        ("upper",   "1 majuscule"),
        ("lower",   "1 minuscule"),
        ("special", "1 caractère spécial (!@#$%^&*...)"),
    ]

    def __init__(self, master, on_register, on_back):
        super().__init__(master, corner_radius=0, fg_color="transparent")
        self._on_register = on_register   # ← utilisé après succès
        self._on_back = on_back
        self._build()

    def _build(self):
        container = ctk.CTkFrame(self, width=380, height=640, corner_radius=16)
        container.place(relx=0.5, rely=0.5, anchor="center")
        container.pack_propagate(False)

        ctk.CTkLabel(
            container,
            text="💰 Budget Buddy",
            font=ctk.CTkFont(size=26, weight="bold"),
        ).pack(pady=(24, 4))

        ctk.CTkLabel(
            container,
            text="Créez votre compte",
            font=ctk.CTkFont(size=13),
            text_color="gray",
        ).pack(pady=(0, 14))

        # Nom
        ctk.CTkLabel(container, text="Nom", anchor="w",
                     font=ctk.CTkFont(size=13)).pack(fill="x", padx=32)
        self.last_name_entry = ctk.CTkEntry(
            container, placeholder_text="Dupont", height=38)
        self.last_name_entry.pack(fill="x", padx=32, pady=(4, 10))

        # Prénom
        ctk.CTkLabel(container, text="Prénom", anchor="w",
                     font=ctk.CTkFont(size=13)).pack(fill="x", padx=32)
        self.first_name_entry = ctk.CTkEntry(
            container, placeholder_text="Jean", height=38)
        self.first_name_entry.pack(fill="x", padx=32, pady=(4, 10))

        # Email
        ctk.CTkLabel(container, text="Email", anchor="w",
                     font=ctk.CTkFont(size=13)).pack(fill="x", padx=32)
        self.email_entry = ctk.CTkEntry(
            container, placeholder_text="exemple@gmail.com", height=38)
        self.email_entry.pack(fill="x", padx=32, pady=(4, 10))

        # Mot de passe
        ctk.CTkLabel(container, text="Mot de passe", anchor="w",
                     font=ctk.CTkFont(size=13)).pack(fill="x", padx=32)
        self.password_entry = ctk.CTkEntry(
            container, placeholder_text="••••••••", show="•", height=38)
        self.password_entry.pack(fill="x", padx=32, pady=(4, 8))
        self.password_entry.bind("<KeyRelease>", lambda e: self._check_rules())

        # Indicateurs de règles
        self._rule_labels = {}
        rules_frame = ctk.CTkFrame(container, fg_color="transparent")
        rules_frame.pack(fill="x", padx=32, pady=(0, 12))

        for key, text in self._RULES:
            lbl = ctk.CTkLabel(
                rules_frame,
                text=f"✗  {text}",
                font=ctk.CTkFont(size=11),
                text_color="#ef4444",
                anchor="w",
            )
            lbl.pack(anchor="w")
            self._rule_labels[key] = lbl

        # Bouton inscription
        self.submit_btn = ctk.CTkButton(
            container,
            text="S'inscrire",
            height=42,
            font=ctk.CTkFont(size=14, weight="bold"),
            state="disabled",
            fg_color="#7c3aed",
            hover_color="#6d28d9",
            command=self._handle_register,
        )
        self.submit_btn.pack(fill="x", padx=32)

        # Retour
        ctk.CTkButton(
            container,
            text="← Retour",
            fg_color="transparent",
            text_color="gray",
            hover_color=("gray85", "gray25"),
            font=ctk.CTkFont(size=12),
            command=self._on_back,
        ).pack(pady=(8, 16))

    # Vérification dynamique des règles du mot de passe
    def _check_rules(self):
        pwd = self.password_entry.get()
        results = {
            "min10":   len(pwd) >= 10,
            "upper":   any(c.isupper() for c in pwd),
            "lower":   any(c.islower() for c in pwd),
            "special": any(c in "!@#$%^&*()_+-=[]{}|;':\",./<>?" for c in pwd),
        }
        for key, ok in results.items():
            text = dict(self._RULES)[key]
            self._rule_labels[key].configure(
                text=f"✓  {text}" if ok else f"✗  {text}",
                text_color="#22c55e" if ok else "#ef4444",
            )
        self.submit_btn.configure(
            state="normal" if all(results.values()) else "disabled")

    # Handler d'inscription
    def _handle_register(self):
        first_name = self.first_name_entry.get()
        last_name  = self.last_name_entry.get()
        email      = self.email_entry.get()
        password   = self.password_entry.get()

        success, message = handle_register(first_name, last_name, email, password)

        if success:
            print("Inscription OK :", message)
            self._on_register()  # ← redirection vers _on_login_success
        else:
            print("Erreur :", message)
