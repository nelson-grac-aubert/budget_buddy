import customtkinter as ctk
from scripts.logic.login_register import update_password, update_email, validate_email


class AccountManagementWindow(ctk.CTkToplevel):
    """Modal window for changing the user's password or email address."""

    _RULES = [
        ("min10",   "10 caractères minimum"),
        ("upper",   "1 majuscule"),
        ("lower",   "1 minuscule"),
        ("digit",   "1 chiffre"),
        ("special", "1 caractère spécial (!@#$%^&*...)"),
    ]

    def __init__(self, user_id: int, master=None, on_success=None):
        super().__init__(master)
        self.user_id    = user_id
        self._on_success = on_success
        self.title("Account Management")
        self.geometry("420x300")
        self.resizable(False, False)
        self.grab_set()
        self._build_main()

    # ── Alerte ────────────────────────────────────────────────────────────── #

    def _show_alert(self, message: str, success: bool = True):
        """Affiche une alerte modale de succès ou d'erreur."""
        alert = ctk.CTkToplevel(self)
        alert.title("")
        alert.geometry("340x180")
        alert.resizable(False, False)
        alert.grab_set()
        alert.focus()

        color  = "#22c55e" if success else "#ef4444"
        bg     = "#14532d" if success else "#7f1d1d"
        icon   = "✅" if success else "❌"

        ctk.CTkFrame(alert, height=4, fg_color=color,
                     corner_radius=0).pack(fill="x")

        ctk.CTkLabel(
            alert,
            text=f"{icon}  {'Succès' if success else 'Erreur'}",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color=color,
        ).pack(pady=(20, 6))

        ctk.CTkLabel(
            alert,
            text=message,
            font=ctk.CTkFont(size=13),
            text_color="#d1d5db",
            wraplength=280,
        ).pack(pady=(0, 16))

        ctk.CTkButton(
            alert,
            text="OK",
            width=120, height=36,
            fg_color=color,
            hover_color=bg,
            font=ctk.CTkFont(size=13, weight="bold"),
            text_color="white",
            command=alert.destroy,
        ).pack()

    # ── Main menu ─────────────────────────────────────────────────────────── #

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
            text="Change Password",
            width=260, height=42,
            font=ctk.CTkFont(size=14),
            command=self._build_change_password,
        ).pack(pady=8)

        ctk.CTkButton(
            self,
            text="Update Email",
            width=260, height=42,
            font=ctk.CTkFont(size=14),
            fg_color="transparent",
            border_width=2,
            text_color=("gray10", "gray90"),
            command=self._build_update_email,
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

    # ── Change password view  #

    def _build_change_password(self):
        self._clear()
        self.geometry("420x500")
        self._pwd_visible     = False
        self._confirm_visible = False

        ctk.CTkLabel(
            self,
            text="Change Password",
            font=ctk.CTkFont(size=18, weight="bold"),
        ).pack(pady=(24, 16))

        ctk.CTkLabel(self, text="New password", anchor="w",
                     font=ctk.CTkFont(size=13)).pack(fill="x", padx=30)

        pwd_row = ctk.CTkFrame(self, fg_color="transparent")
        pwd_row.pack(fill="x", padx=30, pady=(4, 8))

        self.new_pwd_entry = ctk.CTkEntry(
            pwd_row, placeholder_text="••••••••", show="•", height=38)
        self.new_pwd_entry.pack(side="left", fill="x", expand=True)
        self.new_pwd_entry._entry.bind("<KeyRelease>", lambda e: self._check_rules())

        self.eye_btn_new = ctk.CTkButton(
            pwd_row, text="🙈", width=38, height=38,
            corner_radius=8, fg_color="transparent",
            hover_color=("gray85", "gray25"),
            font=ctk.CTkFont(size=16),
            command=self._toggle_new,
        )
        self.eye_btn_new.pack(side="left", padx=(4, 0))

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

        ctk.CTkLabel(self, text="Confirm password", anchor="w",
                     font=ctk.CTkFont(size=13)).pack(fill="x", padx=30)

        confirm_row = ctk.CTkFrame(self, fg_color="transparent")
        confirm_row.pack(fill="x", padx=30, pady=(4, 8))

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

        self.pwd_error_label = ctk.CTkLabel(
            self, text="", font=ctk.CTkFont(size=11),
            text_color="#ef4444", anchor="w")
        self.pwd_error_label.pack(fill="x", padx=30)

        btns = ctk.CTkFrame(self, fg_color="transparent")
        btns.pack(fill="x", padx=30, pady=(12, 0))

        ctk.CTkButton(
            btns, text="← Back", height=40,
            fg_color="transparent", border_width=2,
            text_color=("gray10", "gray90"),
            hover_color=("gray85", "gray25"),
            font=ctk.CTkFont(size=13),
            command=self._build_main,
        ).pack(side="left", expand=True, padx=(0, 8))

        self.save_pwd_btn = ctk.CTkButton(
            btns, text="Save", height=40,
            fg_color="#7c3aed", hover_color="#6d28d9",
            font=ctk.CTkFont(size=13, weight="bold"),
            state="disabled",
            command=self._handle_change_password,
        )
        self.save_pwd_btn.pack(side="left", expand=True)

    # ── Update email view 

    def _build_update_email(self):
        self._clear()
        self.geometry("420x320")

        ctk.CTkLabel(
            self,
            text="Update Email",
            font=ctk.CTkFont(size=18, weight="bold"),
        ).pack(pady=(24, 16))

        ctk.CTkLabel(self, text="New email address", anchor="w",
                     font=ctk.CTkFont(size=13)).pack(fill="x", padx=30)

        self.email_entry = ctk.CTkEntry(
            self, placeholder_text="example@email.com", height=38)
        self.email_entry.pack(fill="x", padx=30, pady=(4, 8))

        self.email_error_label = ctk.CTkLabel(
            self, text="", font=ctk.CTkFont(size=11),
            text_color="#ef4444", anchor="w")
        self.email_error_label.pack(fill="x", padx=30)

        btns = ctk.CTkFrame(self, fg_color="transparent")
        btns.pack(fill="x", padx=30, pady=(20, 0))

        ctk.CTkButton(
            btns, text="← Back", height=40,
            fg_color="transparent", border_width=2,
            text_color=("gray10", "gray90"),
            hover_color=("gray85", "gray25"),
            font=ctk.CTkFont(size=13),
            command=self._build_main,
        ).pack(side="left", expand=True, padx=(0, 8))

        ctk.CTkButton(
            btns, text="Save", height=40,
            fg_color="#7c3aed", hover_color="#6d28d9",
            font=ctk.CTkFont(size=13, weight="bold"),
            command=self._handle_update_email,
        ).pack(side="left", expand=True)

    # ── Visibility toggles 

    def _toggle_new(self):
        self._pwd_visible = not self._pwd_visible
        self.new_pwd_entry.configure(show="" if self._pwd_visible else "•")
        self.eye_btn_new.configure(text="👁" if self._pwd_visible else "🙈")

    def _toggle_confirm(self):
        self._confirm_visible = not self._confirm_visible
        self.confirm_pwd_entry.configure(show="" if self._confirm_visible else "•")
        self.eye_btn_confirm.configure(text="👁" if self._confirm_visible else "🙈")

    # ── Live password validation 

    def _check_rules(self):
        pwd = self.new_pwd_entry.get()
        results = {
            "min10":   len(pwd) >= 10,
            "upper":   any(c.isupper() for c in pwd),
            "lower":   any(c.islower() for c in pwd),
            "digit":   any(c.isdigit() for c in pwd),
            "special": any(c in "!@#$%^&*()_+-=[]{}|;':\",./<>?" for c in pwd),
        }
        for key, ok in results.items():
            text = dict(self._RULES)[key]
            self._rule_labels[key].configure(
                text=f"✓  {text}" if ok else f"✗  {text}",
                text_color="#22c55e" if ok else "#ef4444",
            )
        self.save_pwd_btn.configure(
            state="normal" if all(results.values()) else "disabled")

    # ── Form handlers 

    def _handle_change_password(self):
        new_pwd     = self.new_pwd_entry.get()
        confirm_pwd = self.confirm_pwd_entry.get()

        if new_pwd != confirm_pwd:
            self.pwd_error_label.configure(
                text="Passwords do not match.", text_color="#ef4444")
            return

        success, message = update_password(self.user_id, new_pwd)

        if success:
            if self._on_success:
                self._on_success("🔒 Mot de passe modifié", "Votre mot de passe a été mis à jour.", "success")
            self._build_main()
        else:
            self._show_alert(message, success=False)

    def _handle_update_email(self):
        new_email = self.email_entry.get().strip()

        if not validate_email(new_email):
            self.email_error_label.configure(
                text="Invalid email format.", text_color="#ef4444")
            return

        success, message = update_email(self.user_id, new_email)

        if success:
            if self._on_success:
                self._on_success("✉️ Email modifié", "Votre adresse email a été mise à jour.", "info")
            self._build_main()
        else:
            self._show_alert(message, success=False)

    # ── Utility 

    def _clear(self):
        for widget in self.winfo_children():
            widget.destroy()