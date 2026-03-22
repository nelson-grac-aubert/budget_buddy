import customtkinter as ctk
 
 
class Sidebar(ctk.CTkFrame):
    """Sidebar navigation with notification badge."""
 
    NAV_ICONS = {
        "Accueil":       "🏠",
        "Dashboard":     "📊",
        "Transactions":  "📁",
        "Notifications": "🔔",
    }
 
    def __init__(self, master, nav_commands: dict, on_account):
        super().__init__(master, width=200, corner_radius=0)
        self.pack_propagate(False)
        self._notif_count = 0
        self._badge_label = None
        self._notif_btn   = None
        self._build(nav_commands, on_account)
 
    def _build(self, nav_commands, on_account):
        # Logo
        ctk.CTkLabel(
            self,
            text="💰 Budget\n    Buddy",
            font=ctk.CTkFont(size=22, weight="bold"),
            justify="left",
        ).pack(pady=(28, 24), padx=20, anchor="w")
 
        # navigation buttons
        for label, cmd in nav_commands.items():
            icon = self.NAV_ICONS.get(label, "•")
 
            if label == "Notifications":
                # Container for button with badge
                row = ctk.CTkFrame(self, fg_color="transparent")
                row.pack(fill="x", padx=12, pady=3)
 
                self._notif_btn = ctk.CTkButton(
                    row,
                    text=f"{icon}  {label}",
                    anchor="w",
                    height=40,
                    fg_color="transparent",
                    text_color=("gray10", "gray90"),
                    hover_color=("gray85", "gray25"),
                    font=ctk.CTkFont(size=14),
                    command=cmd,
                )
                self._notif_btn.pack(side="left", fill="x", expand=True)
 
                # Red badge (hide by default)
                self._badge_label = ctk.CTkLabel(
                    row,
                    text="",
                    width=20, height=20,
                    corner_radius=10,
                    fg_color="#ef4444",
                    text_color="white",
                    font=ctk.CTkFont(size=10, weight="bold"),
                )
                
 
            else:
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
 
        # spacer
        ctk.CTkFrame(self, fg_color="transparent").pack(fill="both", expand=True)
 
        # button account(bottom)
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
 
    def add_notification(self):
        """Increment the notification badge."""
        self._notif_count += 1
        if self._badge_label:
            self._badge_label.configure(text=str(self._notif_count))
            self._badge_label.pack(side="right", padx=(4, 0))
 
    def clear_notifications(self):
        """Reset the notification badge to zero (call when the user opens Notifications)."""
        self._notif_count = 0
        if self._badge_label:
            self._badge_label.configure(text="")
            self._badge_label.pack_forget()
