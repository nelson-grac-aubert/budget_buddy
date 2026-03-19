import customtkinter as ctk
from datetime import datetime

from scripts.graphic.sidebar import Sidebar
from scripts.graphic.dashboard import Dashboard
from scripts.graphic.admin.dashboard_admin import AdminDashboard
from scripts.graphic.account_management_window import AccountManagementWindow
from scripts.graphic.register_window import RegisterWindow
from scripts.graphic.login_window import HomeWindow
from scripts.graphic.menu_home import HomeMenu
from scripts.graphic.transaction_window import TransactionWindow
from scripts.graphic.releve_view import ReleveView
from scripts.graphic.notification_view import NotificationView

from scripts.logic.dashboard_data import get_dashboard_data
from scripts.logic.dashboard_data import get_transactions_from_db


class BudgetBuddyApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Budget Buddy")
        self.geometry("900x620")
        self.minsize(700, 500)

        self._account_window = None
        self._notifications  = []
        self.current_user_id = None

        self.root_frame = ctk.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.root_frame.pack(fill="both", expand=True)

        self._show_landing()

    def _clear_root(self):
        for widget in self.root_frame.winfo_children():
            widget.destroy()

    def _clear_main(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()

    # ── Écrans pré-connexion ──

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
            on_register=self._show_login,
            on_back=self._show_landing,
        ).pack(fill="both", expand=True)

    # ── Après connexion réussie ──

    def _on_login_success(self, user_id, is_admin: bool = False):
        self.current_user_id = user_id
        self._clear_root()

        # ── Routing admin ──
        if is_admin:
            AdminDashboard(
                self.root_frame,
                on_logout=self._logout,
            ).pack(fill="both", expand=True, padx=20, pady=20)
            return

        # ── Routing utilisateur normal ──
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

    # ── Vues principales ──

    def _show_dashboard(self):
        self._clear_main()
        data = get_dashboard_data(self.current_user_id)
        Dashboard(
            self.current_user_id,
            self.main_frame,
            balance=data["balance"],
            monthly_balance=data["monthly_balance"],
            income=data["income"],
            expenses=data["expenses"],
            fullname=data["fullname"],
            on_releve=self._show_releve,
            on_notify=self._on_new_notification,
            on_logout=self._logout,
            on_refresh=self._show_dashboard,
        ).pack(fill="both", expand=True)

    def _show_transactions(self):
        self._clear_main()
        TransactionWindow(self.main_frame).pack(fill="both", expand=True)

    def _show_releve(self):
        self._clear_main()
        ReleveView(
            self.main_frame,
            on_back=self._show_dashboard,
            transactions=get_transactions_from_db(self.current_user_id),
        ).pack(fill="both", expand=True)

    def _show_reports(self):
        self._clear_main()
        self.sidebar.clear_notifications()
        NotificationView(
            self.main_frame,
            notifications=self._notifications,
        ).pack(fill="both", expand=True)

    # ── Déconnexion ──

    def _logout(self):
        self._notifications.clear()
        self.current_user_id = None
        self._show_landing()

    # ── Gestion des notifications ──

    def _on_new_notification(self, title: str, message: str, kind: str = "success"):
        self._notifications.append({
            "title":   title,
            "message": message,
            "kind":    kind,
            "time":    datetime.now().strftime("%H:%M"),
        })
        self.sidebar.add_notification()

    # ── Fenêtres secondaires ──

    def _open_account_management(self):
        if self._account_window is None or not self._account_window.winfo_exists():
            self._account_window = AccountManagementWindow(
                user_id=self.current_user_id,
                master=self,
                on_success=self._on_new_notification,
            )
            self._account_window.focus()
        else:
            self._account_window.focus()