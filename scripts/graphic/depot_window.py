import customtkinter as ctk
from scripts.logic.class_deposit import Deposit
from scripts.graphic.transaction_utils import categories_depot, get_categorie_id


class DepotWindow(ctk.CTkToplevel):
    """Fenêtre modale pour effectuer un dépôt."""

    def __init__(self, current_user_id, master=None, on_success=None):
        super().__init__(master)
        self.title("Dépôt")
        self.geometry("420x470")
        self.resizable(False, False)
        self.grab_set()
        self._on_success     = on_success
        self.current_user_id = current_user_id
        self._build()

    def _build(self):
        ctk.CTkLabel(
            self,
            text="💶  Faire un dépôt",
            font=ctk.CTkFont(size=20, weight="bold"),
        ).pack(pady=(24, 4))

        ctk.CTkLabel(
            self,
            text="Renseignez les informations du dépôt.",
            font=ctk.CTkFont(size=13),
            text_color="gray",
        ).pack(pady=(0, 20))

        ctk.CTkFrame(self, height=1, fg_color="#3a3a3a").pack(
            fill="x", padx=30, pady=(0, 20))

        # Description — champ texte libre
        ctk.CTkLabel(self, text="Description", anchor="w",
                     font=ctk.CTkFont(size=13)).pack(fill="x", padx=30)
        self.description_entry = ctk.CTkEntry(
            self, placeholder_text="Cadeau de mamie", height=38)
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
        _cats = categories_depot()
        self.categorie_var = ctk.StringVar(value=_cats[0])
        ctk.CTkOptionMenu(
            self,
            variable=self.categorie_var,
            values=_cats,
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
            command=self._handle_depot,
        ).pack(side="left", expand=True)

    def _show_error(self, message: str):
        self.error_label.configure(text=f"⚠  {message}" if message else "")

    def _handle_depot(self):
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

        depot = Deposit(
            description=description,
            montant=montant,
            categorie_id=get_categorie_id(categorie),
            account_id=self.current_user_id,
            destination_account_id=None,
        )
        depot.execute()

        self.destroy()
        if self._on_success:
            self._on_success(
                "💶 Dépôt effectué",
                f"{montant:.2f} € déposés\n"
                f"Description : {description}  |  Catégorie : {categorie}",
            )