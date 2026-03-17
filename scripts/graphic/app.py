import customtkinter as ctk
from scripts.graphic.sidebar import Sidebar
from scripts.graphic.dashboard import Dashboard
from scripts.graphic.account_management_window import AccountManagementWindow
from scripts.graphic.register_window import RegisterWindow
from scripts.graphic.home_window import HomeWindow
from scripts.graphic.menu_home import HomeMenu


class BudgetBuddyApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Budget Buddy")
        self.geometry("900x620")
        self.minsize(700, 500)

        self._account_window = None

        self.root_frame = ctk.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.root_frame.pack(fill="both", expand=True)

        self._show_landing()

    # ── Helpers 

    def _clear_root(self):
        for widget in self.root_frame.winfo_children():
            widget.destroy()

    def _clear_main(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()

    # ── Écrans pré-connexion 

    def _show_landing(self):
        self._clear_root()
        HomeMenu(
            self.root_frame,
            on_login=self._show_login,
            on_register=self._show_register,
        ).pack(fill="both", expand=True)

    def _show_login(self):
        self._clear_root()
        HomeWindow(
            self.root_frame,
            on_login=self._on_login_success,
            on_register=self._show_register,
            on_back=self._show_landing,
        ).pack(fill="both", expand=True)

    def _show_register(self):
        self._clear_root()
        RegisterWindow(
            self.root_frame,
            on_register=self._show_login,   # ← redirection vers login
            on_back=self._show_landing,
        ).pack(fill="both", expand=True)

    # ── Après connexion réussie 

    def _on_login_success(self):
        self._clear_root()

        self.sidebar = Sidebar(
            self.root_frame,
            nav_commands={
                "Dashboard":     self._show_dashboard,
                "Transactions":  self._show_transactions,
                "Notifications": self._show_reports,
            },
            on_account=self._open_account_management,
        )
        self.sidebar.pack(side="left", fill="y")

        self.main_frame = ctk.CTkFrame(
            self.root_frame, corner_radius=0, fg_color="transparent")
        self.main_frame.pack(side="left", fill="both", expand=True, padx=20, pady=20)

        self._show_dashboard()

    # ── Vues principales 

    def _show_dashboard(self):
        self._clear_main()
        Dashboard(self.main_frame).pack(fill="both", expand=True)

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

    # ── Fenêtres secondaires 

    def _open_account_management(self):
        if self._account_window is None or not self._account_window.winfo_exists():
            self._account_window = AccountManagementWindow(master=self)
            self._account_window.focus()
        else:
            self._account_window.focus()