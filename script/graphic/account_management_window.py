import customtkinter as ctk


class AccountManagementWindow(ctk.CTkToplevel):
    """Fenêtre modale de gestion du compte utilisateur."""

    def __init__(self, master=None):
        super().__init__(master)
        self.title("Account Management")
        self.geometry("420x340")
        self.resizable(False, False)
        self.grab_set()
        self._build()

    def _build(self):
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

        # Séparateur
        ctk.CTkFrame(self, height=1, fg_color="#3a3a3a").pack(
            fill="x", padx=30, pady=(0, 20))

        # Changer le mot de passe
        ctk.CTkButton(
            self,
            text="🔒  Change Password",
            width=260,
            height=42,
            font=ctk.CTkFont(size=14),
            command=self._change_password,
        ).pack(pady=8)

        # Mettre à jour l'email
        ctk.CTkButton(
            self,
            text="✉️  Update Email",
            width=260,
            height=42,
            font=ctk.CTkFont(size=14),
            fg_color="transparent",
            border_width=2,
            text_color=("gray10", "gray90"),
            command=self._update_email,
        ).pack(pady=8)

        # Fermer
        ctk.CTkButton(
            self,
            text="Close",
            width=260,
            height=36,
            font=ctk.CTkFont(size=13),
            fg_color="transparent",
            text_color="gray",
            hover_color=("gray85", "gray25"),
            command=self.destroy,
        ).pack(pady=(12, 0))

    def _change_password(self):
        # TODO : implémenter le changement de mot de passe
        print("Change Password clicked")

    def _update_email(self):
        # TODO : implémenter la mise à jour de l'email
        print("Update Email clicked")