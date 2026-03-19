import customtkinter as ctk
from scripts.logic.class_withdrawal import Withdrawal
from scripts.logic.class_deposit import Deposit
from scripts.graphic.transaction_utils import categories


class VirementWindow(ctk.CTkToplevel):
    """Fenêtre modale pour effectuer un virement."""

    def __init__(self, current_user_id, master=None, on_success=None):
        super().__init__(master)
        self.title("Nouveau virement")
        self.geometry("420x550")
        self.resizable(False, False)
        self.grab_set()
        self._on_success     = on_success
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

        # Bénéficiaire
        ctk.CTkLabel(self, text="ID du compte du bénéficiaire", anchor="w",
                     font=ctk.CTkFont(size=13)).pack(fill="x", padx=30)
        self.beneficiaire_entry = ctk.CTkEntry(
            self, placeholder_text="3", height=38)
        self.beneficiaire_entry.pack(fill="x", padx=30, pady=(4, 14))

        # Montant
        ctk.CTkLabel(self, text="Montant (€)", anchor="w",
                     font=ctk.CTkFont(size=13)).pack(fill="x", padx=30)
        self.montant_entry = ctk.CTkEntry(
            self, placeholder_text="0,00", height=38)
        self.montant_entry.pack(fill="x", padx=30, pady=(4, 14))

        # Motif
        ctk.CTkLabel(self, text="Motif", anchor="w",
                     font=ctk.CTkFont(size=13)).pack(fill="x", padx=30)
        self.motif_entry = ctk.CTkEntry(
            self, placeholder_text="Ex : Remboursement loyer", height=38)
        self.motif_entry.pack(fill="x", padx=30, pady=(4, 14))

        # Catégorie
        ctk.CTkLabel(self, text="Catégorie", anchor="w",
                     font=ctk.CTkFont(size=13)).pack(fill="x", padx=30)
        self.categorie_var = ctk.StringVar(value=categories()[1])
        ctk.CTkOptionMenu(
            self,
            variable=self.categorie_var,
            values=categories()[1:],
            height=38,
            font=ctk.CTkFont(size=13),
        ).pack(fill="x", padx=30, pady=(4, 6))

        # Label d'erreur
        self.error_label = ctk.CTkLabel(
            self, text="",
            font=ctk.CTkFont(size=11),
            text_color="#ef4444",
            anchor="w",
        )
        self.error_label.pack(fill="x", padx=30, pady=(0, 8))

        # Boutons
        btns = ctk.CTkFrame(self, fg_color="transparent")
        btns.pack(fill="x", padx=30, pady=(4, 0))

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
            fg_color="#7c3aed", hover_color="#6c28d9e7",
            font=ctk.CTkFont(size=13, weight="bold"),
            command=self._handle_virement,
        ).pack(side="left", expand=True)

    def _show_error(self, message: str):
        self.error_label.configure(text=f"⚠  {message}" if message else "")

    def _handle_virement(self):
        beneficiaire = self.beneficiaire_entry.get().strip()
        montant_str  = self.montant_entry.get().strip().replace(",", ".")
        motif        = self.motif_entry.get().strip()
        categorie    = self.categorie_var.get()

        # Validation
        if not beneficiaire:
            self._show_error("Le bénéficiaire est requis.")
            return
        if not montant_str:
            self._show_error("Le montant est requis.")
            return
        try:
            montant = float(montant_str)
        except ValueError:
            self._show_error("Le montant doit être un nombre valide.")
            return
        if montant <= 0:
            self._show_error("Le montant doit être supérieur à 0 €.")
            return

        self._show_error("")

        retrait = Withdrawal(
            description=motif,
            montant=-montant,
            categorie_id=1,       # TODO : mapper categorie → id en DB
            account_id=self.current_user_id,
            destination_account_id=None,
        )
        retrait.execute()

        depot = Deposit(
            description=motif,
            montant=montant,
            categorie_id=1,       # TODO : mapper categorie → id en DB
            account_id=beneficiaire,
            destination_account_id=None,
        )
        depot.execute()

        self.destroy()
        if self._on_success:
            self._on_success(
                "💸 Virement effectué",
                f"{montant} € envoyé au compte n° {beneficiaire}" + (f" — {motif}" if motif else ""),
            )