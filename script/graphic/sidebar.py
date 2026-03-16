import customtkinter as ctk

class Sidebar(ctk.CTkFrame):
    def __init__(self, master, nav_commands, on_account):
        super().__init__(master, width=200, corner_radius=0, fg_color="#2a2a2a")
        self.nav_commands = nav_commands
        self.on_account = on_account
        self._build()

    def _build(self):
        # Logo / titre
        ctk.CTkLabel(
            self,
            text="💰 Budget Buddy",
            font=ctk.CTkFont(size=20, weight="bold"),
        ).pack(pady=(24, 12))

        # Boutons de navigation
        for name, cmd in self.nav_commands.items():
            ctk.CTkButton(
                self,
                text=name,
                width=180,
                height=40,
                font=ctk.CTkFont(size=14),
                fg_color="transparent",
                border_width=0,
                text_color=("gray10", "gray90"),
                command=cmd,
            ).pack(pady=8)

        # Spacer
        ctk.CTkFrame(self, fg_color="transparent").pack(expand=True)

        # Bouton compte
        ctk.CTkButton(
            self,
            text="⚙️ Account",
            width=180,
            height=40,
            font=ctk.CTkFont(size=14),
            fg_color="transparent",
            border_width=0,
            text_color=("gray10", "gray90"),
            command=self.on_account,
        ).pack(pady=(0, 24))