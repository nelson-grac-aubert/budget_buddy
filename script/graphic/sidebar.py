import customtkinter as ctk


class Sidebar(ctk.CTkFrame):
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

        # Nav buttons
        nav_icons = {
            "Dashboard": "📊",
            "Transactions": "📁",
            "Reports": "📈",
        }
        for label, cmd in nav_commands.items():
            icon = nav_icons.get(label, "•")
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

        # Spacer
        ctk.CTkFrame(self, fg_color="transparent").pack(fill="both", expand=True)

        # Account button (bas)
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