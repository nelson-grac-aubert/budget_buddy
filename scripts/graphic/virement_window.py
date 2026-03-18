import customtkinter as ctk
from scripts.logic.class_withdrawal import Withdrawal
from scripts.logic.class_deposit import Deposit


class VirementWindow(ctk.CTkToplevel):
    """Fenêtre modale pour effectuer un virement."""

    def __init__(self, current_user_id, master=None, on_success=None):
        super().__init__(master)
        self.title("Nouveau virement")
        self.geometry("420x420")
        self.resizable(False, False)
        self.grab_set()
        self._on_success = on_success
        self.current_user_id = current_user_id
        self._build()

    def _build(self):
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

        ctk.CTkFrame(self, height=1, fg_color="#3a3a3a").pack(
            fill="x", padx=30, pady=(0, 20))

        ctk.CTkLabel(self, text="ID du compte du bénéficiaire", anchor="w",
                     font=ctk.CTkFont(size=13)).pack(fill="x", padx=30)
        self.beneficiaire_entry = ctk.CTkEntry(
            self, placeholder_text="3", height=38)
        self.beneficiaire_entry.pack(fill="x", padx=30, pady=(4, 14))

        ctk.CTkLabel(self, text="Montant (€)", anchor="w",
                     font=ctk.CTkFont(size=13)).pack(fill="x", padx=30)
        self.montant_entry = ctk.CTkEntry(
            self, placeholder_text="0,00", height=38)
        self.montant_entry.pack(fill="x", padx=30, pady=(4, 14))

        ctk.CTkLabel(self, text="Motif (optionnel)", anchor="w",
                     font=ctk.CTkFont(size=13)).pack(fill="x", padx=30)
        self.motif_entry = ctk.CTkEntry(
            self, placeholder_text="Ex : Remboursement loyer", height=38)
        self.motif_entry.pack(fill="x", padx=30, pady=(4, 24))

        btns = ctk.CTkFrame(self, fg_color="transparent")
        btns.pack(fill="x", padx=30)

        ctk.CTkButton(
            btns, text="Annuler", height=40,
            fg_color="transparent", border_width=2,
            text_color=("gray10", "gray90"),
            hover_color=("gray85", "gray25"),
            font=ctk.CTkFont(size=13),
            command=self.destroy,
        ).pack(side="left", expand=True, padx=(0, 8))

        ctk.CTkButton(
            btns, text="Confirmer", height=40,
            fg_color="#7c3aed", hover_color="#6d28d9",
            font=ctk.CTkFont(size=13, weight="bold"),
            command=self._handle_virement,
        ).pack(side="left", expand=True)

    def _handle_virement(self):
        beneficiaire = self.beneficiaire_entry.get().strip()
        montant      = self.montant_entry.get().strip().replace(",", ".")
        motif        = self.motif_entry.get().strip()

        if not beneficiaire:
            self._show_error("Le description est requis.")
            return
        if not montant:
            self._show_error("La montant est requise.")
            return
        try:
            montant = float(montant)
        except ValueError:
            self._show_error("La montant doit être un nombre valide.")
            return
        if montant <= 0:
            self._show_error("La montant doit être supérieur à 0 €.")
            return
        
        account_id = self.current_user_id

        retrait = Withdrawal(
        description=motif,
        montant=-montant,          # retrait = montant négatif
        categorie_id=1,       # on verra plus tard pour les catégories
        account_id=account_id,
        destination_account_id=None,
    )

        retrait.execute()

        depot = Deposit(
        description=motif,
        montant=montant,          # depot = montant négatif
        categorie_id=1,       # on verra plus tard pour les catégories
        account_id=beneficiaire,
        destination_account_id=None,
    )

        depot.execute()

        self.destroy()
        if self._on_success:
            self._on_success(
                "💸 Virement effectué",
                f"{montant} € envoyé à {beneficiaire}" + (f" — {motif}" if motif else ""),
            )