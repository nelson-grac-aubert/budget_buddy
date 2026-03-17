import customtkinter as ctk


class RetraitWindow(ctk.CTkToplevel):
    """Fenêtre modale pour effectuer un retrait."""

    def __init__(self, master=None):
        super().__init__(master)
        self.title("Retrait")
        self.geometry("420x380")
        self.resizable(False, False)
        self.grab_set()
        self._build()

    def _build(self):
        ctk.CTkLabel(
            self,
            text="💵  Faire un retrait",
            font=ctk.CTkFont(size=20, weight="bold"),
        ).pack(pady=(24, 4))

        ctk.CTkLabel(
            self,
            text="Renseignez les informations du retrait.",
            font=ctk.CTkFont(size=13),
            text_color="gray",
        ).pack(pady=(0, 20))

        ctk.CTkFrame(self, height=1, fg_color="#3a3a3a").pack(
            fill="x", padx=30, pady=(0, 20))

        # Bénéficiaire
        ctk.CTkLabel(self, text="Bénéficiaire", anchor="w",
                     font=ctk.CTkFont(size=13)).pack(fill="x", padx=30)
        self.beneficiaire_entry = ctk.CTkEntry(
            self, placeholder_text="Nom ou IBAN", height=38)
        self.beneficiaire_entry.pack(fill="x", padx=30, pady=(4, 14))

        # Somme
        ctk.CTkLabel(self, text="Somme (€)", anchor="w",
                     font=ctk.CTkFont(size=13)).pack(fill="x", padx=30)
        self.somme_entry = ctk.CTkEntry(
            self, placeholder_text="0,00", height=38)
        self.somme_entry.pack(fill="x", padx=30, pady=(4, 6))

        # Erreur en cas de validation echouée
        self.error_label = ctk.CTkLabel(
            self, text="",
            font=ctk.CTkFont(size=11),
            text_color="#ef4444",
            anchor="w",
        )
        self.error_label.pack(fill="x", padx=30)

        # Boutons
        btns = ctk.CTkFrame(self, fg_color="transparent")
        btns.pack(fill="x", padx=30, pady=(20, 0))

        ctk.CTkButton(
            btns,
            text="Annuler",
            height=40,
            fg_color="transparent",
            border_width=2,
            text_color=("gray10", "gray90"),
            hover_color=("gray85", "gray25"),
            font=ctk.CTkFont(size=13),
            command=self.destroy,
        ).pack(side="left", expand=True, padx=(0, 8))

        ctk.CTkButton(
            btns,
            text="Confirmer",
            height=40,
            fg_color="#7c3aed",
            hover_color="#6d28d9",
            font=ctk.CTkFont(size=13, weight="bold"),
            command=self._handle_retrait,
        ).pack(side="left", expand=True)

    def _handle_retrait(self):
        beneficiaire = self.beneficiaire_entry.get().strip()
        somme_str    = self.somme_entry.get().strip().replace(",", ".")

        # Validation
        if not beneficiaire:
            self._show_error("Le bénéficiaire est requis.")
            return

        if not somme_str:
            self._show_error("La somme est requise.")
            return

        try:
            somme = float(somme_str)
        except ValueError:
            self._show_error("La somme doit être un nombre valide.")
            return

        if somme <= 0:
            self._show_error("La somme doit être supérieure à 0 €.")
            return

        # TODO : vérifier le solde disponible et enregistrer en DB
        self._show_error("")
        print(f"Retrait → {beneficiaire} | {somme:.2f} €")
        self.destroy()

    def _show_error(self, message: str):
        self.error_label.configure(text=f"⚠  {message}" if message else "")