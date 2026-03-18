import customtkinter as ctk
from scripts.logic.class_withdrawal import Withdrawal


class RetraitWindow(ctk.CTkToplevel):
    """Fenêtre modale pour effectuer un retrait."""

    def __init__(self, master=None, on_success=None):
        super().__init__(master)
        self.title("Retrait")
        self.geometry("420x380")
        self.resizable(False, False)
        self.grab_set()
        self._on_success = on_success
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

        ctk.CTkLabel(self, text="Description", anchor="w",
                     font=ctk.CTkFont(size=13)).pack(fill="x", padx=30)
        self.description_entry = ctk.CTkEntry(
            self, placeholder_text="Courses au marché", height=38)
        self.description_entry.pack(fill="x", padx=30, pady=(4, 14))

        ctk.CTkLabel(self, text="Montant (€)", anchor="w",
                     font=ctk.CTkFont(size=13)).pack(fill="x", padx=30)
        self.montant_entry = ctk.CTkEntry(
            self, placeholder_text="0,00", height=38)
        self.montant_entry.pack(fill="x", padx=30, pady=(4, 6))

        self.error_label = ctk.CTkLabel(
            self, text="",
            font=ctk.CTkFont(size=11),
            text_color="#ef4444",
            anchor="w",
        )
        self.error_label.pack(fill="x", padx=30)

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

    def _handle_retrait(self):
        description = self.description_entry.get().strip()
        montant_str    = self.montant_entry.get().strip().replace(",", ".")

        if not description:
            self._show_error("Le description est requis.")
            return
        if not montant_str:
            self._show_error("La montant est requise.")
            return
        try:
            montant = float(montant_str)
        except ValueError:
            self._show_error("La montant doit être un nombre valide.")
            return
        if montant <= 0:
            self._show_error("La montant doit être supérieur à 0 €.")
            return

        # Renseigner les éléments du retrait 

        account_id = 1

        retrait = Withdrawal(
        description=description,
        montant=-montant,          # retrait = montant négatif
        categorie_id=1,       # on verra plus tard pour les catégories
        account_id=account_id,
        destination_account_id=None,
    )

        retrait.execute()

        self._show_error("")
        print(f"Retrait → {description} | {montant:.2f} €")
        self.destroy()
        if self._on_success:
            self._on_success(
                "💵 Retrait effectué",
                f"{montant:.2f} € retiré pour {description}",
            )

    def _show_error(self, message: str):
        self.error_label.configure(text=f"⚠  {message}" if message else "")