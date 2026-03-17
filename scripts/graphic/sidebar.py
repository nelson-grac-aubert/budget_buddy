import customtkinter as ctk


class Sidebar(ctk.CTkFrame):
    """Barre de navigation latérale."""

    NAV_ICONS = {
        "Accueil":       "🏠",
        "Dashboard":     "📊",
        "Transactions":  "📁",
        "Notifications": "📈",
    }

    def __init__(self, master, nav_commands: dict, on_account):
        super().__init__(master, width=200, corner_radius=0)
        self.pack_propagate(False)
        self._build(nav_commands, on_account)

    def _build(self, nav_commands, on_account):
        # Logo
        ctk.CTkLabel(
            self,
            text="💰 Budget\n    Buddy",
            font=ctk.CTkFont(size=22, weight="bold"),
            justify="left",
        ).pack(pady=(28, 24), padx=20, anchor="w")

        # Boutons de navigation
        for label, cmd in nav_commands.items():
            icon = self.NAV_ICONS.get(label, "•")
            ctk.CTkButton(
                self,
                text=f"{icon}  {label}",
                anchor="w",
                height=40,
                fg_color="transparent",
                text_color=("gray10", "gray90"),
                hover_color=("gray85", "gray25"),
                font=ctk.CTkFont(size=14),
                command=cmd,
            ).pack(fill="x", padx=12, pady=3)

        # Espaceur
        ctk.CTkFrame(self, fg_color="transparent").pack(fill="both", expand=True)

        # Bouton compte (bas)
        ctk.CTkButton(
            self,
            text="⚙️  Account",
            anchor="w",
            height=40,
            fg_color="transparent",
            text_color=("gray10", "gray90"),
            hover_color=("gray85", "gray25"),
            font=ctk.CTkFont(size=14),
            command=on_account,
        ).pack(fill="x", padx=12, pady=(0, 16))