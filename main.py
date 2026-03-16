import customtkinter as ctk
from script.graphic.sidebar import Sidebar
from script.graphic.dashboard import Dasboard
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

    

   

    

    def _open_account_management(self):
        if self._account_window is None or not self._account_window.winfo_exists():
            self._account_window = AccountManagementWindow(master=self)
            self._account_window.focus()
        else:
            self._account_window.focus()


if __name__ == "__main__":
    app = BudgetBuddyApp()
    app.mainloop()