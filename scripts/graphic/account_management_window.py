import customtkinter as ctk


class AccountManagementWindow(ctk.CTkToplevel):
    """Fenêtre modale de gestion du compte utilisateur."""

    _RULES = [
        ("min10",   "10 caractères minimum"),
        ("upper",   "1 majuscule"),
        ("lower",   "1 minuscule"),
        ("special", "1 caractère spécial (!@#$%^&*...)"),
    ]

    def __init__(self, master=None):
        super().__init__(master)
        self.title("Account Management")
        self.geometry("420x300")
        self.resizable(False, False)
        self.grab_set()
        self._build_main()

    # ── Vue principale 

    def _build_main(self):
        self._clear()
        self.geometry("420x300")

        ctk.CTkLabel(
            self,
            text="Account Management",
            font=ctk.CTkFont(size=20, weight="bold"),
        ).pack(pady=(24, 4))

        ctk.CTkLabel(
            self,
            text="Manage your account settings below.",
            font=ctk.CTkFont(size=13),
            text_color="gray",
        ).pack(pady=(0, 20))

        ctk.CTkFrame(self, height=1, fg_color="#3a3a3a").pack(
            fill="x", padx=30, pady=(0, 20))

        ctk.CTkButton(
            self,
            text="🔒  Change Password",
            width=260, height=42,
            font=ctk.CTkFont(size=14),
            command=self._build_change_password,
        ).pack(pady=8)

        ctk.CTkButton(
            self,
            text="✉️  Update Email",
            width=260, height=42,
            font=ctk.CTkFont(size=14),
            fg_color="transparent",
            border_width=2,
            text_color=("gray10", "gray90"),
            command=self._update_email,
        ).pack(pady=8)

        ctk.CTkButton(
            self,
            text="Close",
            width=260, height=36,
            font=ctk.CTkFont(size=13),
            fg_color="transparent",
            text_color="gray",
            hover_color=("gray85", "gray25"),
            command=self.destroy,
        ).pack(pady=(12, 0))

    # ── Vue changement de mot de passe 

    def _build_change_password(self):
        self._clear()
        self.geometry("420x500")
        self._pwd_visible     = False
        self._confirm_visible = False

        ctk.CTkLabel(
            self,
            text="🔒  Changer le mot de passe",
            font=ctk.CTkFont(size=18, weight="bold"),
        ).pack(pady=(24, 16))

        # Nouveau mot de passe + toggle
        ctk.CTkLabel(self, text="Nouveau mot de passe", anchor="w",
                     font=ctk.CTkFont(size=13)).pack(fill="x", padx=30)

        pwd_row = ctk.CTkFrame(self, fg_color="transparent")
        pwd_row.pack(fill="x", padx=30, pady=(4, 8))

        self.new_pwd_entry = ctk.CTkEntry(
            pwd_row, placeholder_text="••••••••", show="•", height=38)
        self.new_pwd_entry.pack(side="left", fill="x", expand=True)
        # Bind sur le widget interne pour garantir la détection de frappe
        self.new_pwd_entry._entry.bind("<KeyRelease>", lambda e: self._check_rules())

        self.eye_btn_new = ctk.CTkButton(
            pwd_row, text="🙈", width=38, height=38,
            corner_radius=8, fg_color="transparent",
            hover_color=("gray85", "gray25"),
            font=ctk.CTkFont(size=16),
            command=self._toggle_new,
        )
        self.eye_btn_new.pack(side="left", padx=(4, 0))

        # Indicateurs de règles
        self._rule_labels = {}
        rules_frame = ctk.CTkFrame(self, fg_color="transparent")
        rules_frame.pack(fill="x", padx=30, pady=(0, 16))

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

        # Confirmation + toggle
        ctk.CTkLabel(self, text="Confirmer le mot de passe", anchor="w",
                     font=ctk.CTkFont(size=13)).pack(fill="x", padx=30)

        confirm_row = ctk.CTkFrame(self, fg_color="transparent")
        confirm_row.pack(fill="x", padx=30, pady=(4, 16))

        self.confirm_pwd_entry = ctk.CTkEntry(
            confirm_row, placeholder_text="••••••••", show="•", height=38)
        self.confirm_pwd_entry.pack(side="left", fill="x", expand=True)

        self.eye_btn_confirm = ctk.CTkButton(
            confirm_row, text="🙈", width=38, height=38,
            corner_radius=8, fg_color="transparent",
            hover_color=("gray85", "gray25"),
            font=ctk.CTkFont(size=16),
            command=self._toggle_confirm,
        )
        self.eye_btn_confirm.pack(side="left", padx=(4, 0))

        # Boutons
        btns = ctk.CTkFrame(self, fg_color="transparent")
        btns.pack(fill="x", padx=30)

        ctk.CTkButton(
            btns,
            text="← Retour",
            height=40,
            fg_color="transparent",
            border_width=2,
            text_color=("gray10", "gray90"),
            hover_color=("gray85", "gray25"),
            font=ctk.CTkFont(size=13),
            command=self._build_main,
        ).pack(side="left", expand=True, padx=(0, 8))

        self.save_btn = ctk.CTkButton(
            btns,
            text="Enregistrer",
            height=40,
            fg_color="#7c3aed",
            hover_color="#6d28d9",
            font=ctk.CTkFont(size=13, weight="bold"),
            state="disabled",
            command=self._handle_change_password,
        )
        self.save_btn.pack(side="left", expand=True)

    # ── Toggles visibilité 

    def _toggle_new(self):
        self._pwd_visible = not self._pwd_visible
        self.new_pwd_entry.configure(show="" if self._pwd_visible else "•")
        self.eye_btn_new.configure(text="👁" if self._pwd_visible else "🙈")

    def _toggle_confirm(self):
        self._confirm_visible = not self._confirm_visible
        self.confirm_pwd_entry.configure(show="" if self._confirm_visible else "•")
        self.eye_btn_confirm.configure(text="👁" if self._confirm_visible else "🙈")

    # ── Validation 

    def _check_rules(self):
        pwd = self.new_pwd_entry.get()
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
        self.save_btn.configure(
            state="normal" if all(results.values()) else "disabled")

    # ── Handlers 

    def _handle_change_password(self):
        new_pwd     = self.new_pwd_entry.get()
        confirm_pwd = self.confirm_pwd_entry.get()
        if new_pwd != confirm_pwd:
            self.confirm_pwd_entry.configure(border_color="#ef4444")
            return
        # TODO : implémenter la logique de changement de mot de passe
        print("Password changed")
        self._build_main()

    def _update_email(self):
        # TODO : implémenter la mise à jour de l'email
        print("Update Email clicked")

   

    def _clear(self):
        for widget in self.winfo_children():
            widget.destroy()