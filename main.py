import customtkinter as ctk
from script.graphic.sidebar import Sidebar
from script.graphic.Dashboar import Dasboard
from script.graphic.account_management_window import AccountManagementWindow
from script.graphic.register_window import Register_windows


ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


class BudgetBuddyApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Budget Buddy")
        self.geometry("900x620")
        self.minsize(700, 500)
        self._account_window = None
        self._register_window = None

        self.sidebar = Sidebar(
            self,
            nav_commands={
                "Dashboard":    self._show_dashboard,
                "Transactions": self._show_transactions,
                "Reports":      self._show_reports,
            },
            on_account=self._open_account_management,
        )
        self.sidebar.pack(side="left", fill="y")

        self.main_frame = ctk.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.main_frame.pack(side="left", fill="both", expand=True, padx=20, pady=20)

        self._show_dashboard()

    def _clear_main(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()

    def _show_dashboard(self):
        self._clear_main()
        Dasboard(self.main_frame).pack(fill="both", expand=True)

    def _show_transactions(self):
        self._clear_main()
        frame = ctk.CTkFrame(self.main_frame, corner_radius=10, height=300)
        frame.pack(fill="x")
        frame.pack_propagate(False)
        ctk.CTkLabel(
            frame,
            text="📋  Les transactions s'afficheront ici",
            text_color="gray",
            font=ctk.CTkFont(size=14),
        ).place(relx=0.5, rely=0.5, anchor="center")

    def _show_reports(self):
        self._clear_main()
        frame = ctk.CTkFrame(self.main_frame, corner_radius=10, height=300)
        frame.pack(fill="x")
        frame.pack_propagate(False)
        ctk.CTkLabel(
            frame,
            text="📈  Les rapports s'afficheront ici",
            text_color="gray",
            font=ctk.CTkFont(size=14),
        ).place(relx=0.5, rely=0.5, anchor="center")

    def _open_account_management(self):
        if self._account_window is None or not self._account_window.winfo_exists():
            self._account_window = AccountManagementWindow(master=self)
            self._account_window.focus()
        else:
            self._account_window.focus()

    def _open_register(self):
        if self._register_window is None or not self._register_window.winfo_exists():
            self._register_window = Register_windows(master=self)
            self._register_window.focus()
        else:
            self._register_window.focus()


if __name__ == "__main__":
    app = BudgetBuddyApp()
    app.mainloop()

    

    def _open_account_management(self):
        if self._account_window is None or not self._account_window.winfo_exists():
            self._account_window = AccountManagementWindow(master=self)
            self._account_window.focus()
        else:
            self._account_window.focus()


if __name__ == "__main__":
    app = BudgetBuddyApp()
    app.mainloop()