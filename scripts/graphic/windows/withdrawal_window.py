import customtkinter as ctk
from scripts.logic.bank_operations.class_withdrawal import Withdrawal
from scripts.graphic.modules.transaction_utils import categories, get_categorie_id
from scripts.logic.app.dashboard_data import get_account_balance


class RetraitWindow(ctk.CTkToplevel):
    """Fenêtre modale pour effectuer un retrait."""

    def __init__(self, current_user_id, master=None, on_success=None, on_overdraft=None):
        super().__init__(master)
        self.title("Retrait")
        self.geometry("420x470")
        self.resizable(False, False)
        self.grab_set()
        self._on_success     = on_success
        self._on_overdraft   = on_overdraft
        self.current_user_id = current_user_id
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

        # Description — texte libre
        ctk.CTkLabel(self, text="Description", anchor="w",
                     font=ctk.CTkFont(size=13)).pack(fill="x", padx=30)
        self.description_entry = ctk.CTkEntry(
            self, placeholder_text="Courses au marché", height=38)
        self.description_entry.pack(fill="x", padx=30, pady=(4, 14))

        # Montant
        ctk.CTkLabel(self, text="Montant (€)", anchor="w",
                     font=ctk.CTkFont(size=13)).pack(fill="x", padx=30)
        self.montant_entry = ctk.CTkEntry(
            self, placeholder_text="0,00", height=38)
        self.montant_entry.pack(fill="x", padx=30, pady=(4, 14))

        # Catégorie — menu déroulant
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
        self.error_label.pack(fill="x", padx=30)

        # Boutons
        btns = ctk.CTkFrame(self, fg_color="transparent")
        btns.pack(fill="x", padx=30, pady=(20, 0))

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
            command=self._handle_retrait,
        ).pack(side="left", expand=True)

    def _show_error(self, message: str):
        self.error_label.configure(text=f"⚠  {message}" if message else "")

    def _handle_retrait(self):
        description = self.description_entry.get().strip()
        montant_str = self.montant_entry.get().strip().replace(",", ".")
        categorie   = self.categorie_var.get()

        if not description:
            self._show_error("La description est requise.")
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
            description=description,
            montant=-montant,
            categorie_id=get_categorie_id(categorie),
            account_id=self.current_user_id,
            destination_account_id=None,
        )
        retrait.execute()

        # Vérifier le solde avant de fermer et de déclencher les callbacks.
        # on_overdraft doit être appelé EN PREMIER : il utilise _notify_no_refresh
        # (sans refresh), donc le Dashboard est encore vivant quand on_success
        # arrive et déclenche le refresh qui le recrée.
        new_balance  = get_account_balance(self.current_user_id)
        is_overdraft = new_balance < 0

        self.destroy()

        if is_overdraft and self._on_overdraft:
            self._on_overdraft(
                "Solde négatif",
                f"Votre solde est passé en négatif ({new_balance:,.2f} €). "
                "Veuillez régulariser votre situation.",
            )

        if self._on_success:
            self._on_success(
                "💵 Retrait effectué",
                f"{montant:.2f} € retirés\n"
                f"Description : {description}  |  Catégorie : {categorie}",
            )