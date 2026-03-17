import customtkinter as ctk


class VirementWindow(ctk.CTkToplevel):
    """Fenêtre modale pour effectuer un virement."""

    def __init__(self, master=None):
        super().__init__(master)
        self.title("Nouveau virement")
        self.geometry("420x420")
        self.resizable(False, False)
        self.grab_set()
        self._build()

    def _build(self):
        # Titre
        ctk.CTkLabel(
            self,
            text="💸  Faire un virement",
            font=ctk.CTkFont(size=20, weight="bold"),
        ).pack(pady=(24, 4))

        ctk.CTkLabel(
            self,
            text="Renseignez les informations du virement.",
            font=ctk.CTkFont(size=13),
            text_color="gray",
        ).pack(pady=(0, 20))

        # Séparateur
        ctk.CTkFrame(self, height=1, fg_color="#3a3a3a").pack(
            fill="x", padx=30, pady=(0, 20))

        # Bénéficiaire
        ctk.CTkLabel(self, text="Bénéficiaire", anchor="w",
                     font=ctk.CTkFont(size=13)).pack(fill="x", padx=30)
        self.beneficiaire_entry = ctk.CTkEntry(
            self, placeholder_text="Nom ou IBAN", height=38)
        self.beneficiaire_entry.pack(fill="x", padx=30, pady=(4, 14))

        # Montant
        ctk.CTkLabel(self, text="Montant (€)", anchor="w",
                     font=ctk.CTkFont(size=13)).pack(fill="x", padx=30)
        self.montant_entry = ctk.CTkEntry(
            self, placeholder_text="0,00", height=38)
        self.montant_entry.pack(fill="x", padx=30, pady=(4, 14))

        # Motif
        ctk.CTkLabel(self, text="Motif (optionnel)", anchor="w",
                     font=ctk.CTkFont(size=13)).pack(fill="x", padx=30)
        self.motif_entry = ctk.CTkEntry(
            self, placeholder_text="Ex : Remboursement loyer", height=38)
        self.motif_entry.pack(fill="x", padx=30, pady=(4, 24))

        # Boutons
        btns = ctk.CTkFrame(self, fg_color="transparent")
        btns.pack(fill="x", padx=30)

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
            command=self._handle_virement,
        ).pack(side="left", expand=True)

    def _handle_virement(self):
        beneficiaire = self.beneficiaire_entry.get()
        montant      = self.montant_entry.get()
        motif        = self.motif_entry.get()
        # TODO : ajouter la logique de virement
        print(f"Virement → {beneficiaire} | {montant} € | {motif}")
        self.destroy()