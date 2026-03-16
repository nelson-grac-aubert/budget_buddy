import customtkinter as ctk


class AccountManagementWindow(ctk.CTkToplevel):
    def __init__(self, master=None):
        super().__init__(master)
        self.title("Account Management")
        self.geometry("420x340")
        self.resizable(False, False)
        self.grab_set()  # Make it modal
        self.create_widgets()

    def create_widgets(self):
        # Title
        title = ctk.CTkLabel(
            self,
            text="Account Management",
            font=ctk.CTkFont(size=20, weight="bold"),
        )
        title.pack(pady=(24, 4))

        subtitle = ctk.CTkLabel(
            self,
            text="Manage your account settings below.",
            font=ctk.CTkFont(size=13),
            text_color="gray",
        )
        subtitle.pack(pady=(0, 20))

        # Divider
        divider = ctk.CTkFrame(self, height=1, fg_color="#3a3a3a")
        divider.pack(fill="x", padx=30, pady=(0, 20))

        # Change Password
        self.change_password_button = ctk.CTkButton(
            self,
            text="🔒  Change Password",
            width=260,
            height=42,
            font=ctk.CTkFont(size=14),
            command=self.change_password,
        )
        self.change_password_button.pack(pady=8)

        # Update Email
        self.update_email_button = ctk.CTkButton(
            self,
            text="✉️  Update Email",
            width=260,
            height=42,
            font=ctk.CTkFont(size=14),
            fg_color="transparent",
            border_width=2,
            text_color=("gray10", "gray90"),
            command=self.update_email,
        )
        self.update_email_button.pack(pady=8)

        # Close button
        close_btn = ctk.CTkButton(
            self,
            text="Close",
            width=260,
            height=36,
            font=ctk.CTkFont(size=13),
            fg_color="transparent",
            text_color="gray",
            hover_color=("gray85", "gray25"),
            command=self.destroy,
        )
        close_btn.pack(pady=(12, 0))

    def change_password(self):
        print("Change Password button clicked")

    def update_email(self):
        print("Update Email button clicked")