import tkinter as tk
import customtkinter as ctk


def _kind_style(kind: str):
    return {
        "success": ("#14532d", "#22c55e", "✅"),
        "warning": ("#78350f", "#f59e0b", "⚠️"),
        "error":   ("#7f1d1d", "#ef4444", "❌"),
        "info":    ("#1e3a5f", "#3b82f6", "ℹ️"),
    }.get(kind, ("#1e3a5f", "#3b82f6", "ℹ️"))


class _NotifDetail(ctk.CTkFrame):
    """Vue détail d'une notification."""

    def __init__(self, master, notif: dict, on_back):
        super().__init__(master, corner_radius=0, fg_color="transparent")
        self._notif   = notif
        self._on_back = on_back
        self._build()

    def _build(self):
        bg, accent, ico = _kind_style(self._notif.get("kind", "info"))

        ctk.CTkButton(
            self, text="< Retour", width=100, height=32,
            fg_color="transparent", border_width=2,
            text_color=("gray10", "gray90"),
            font=ctk.CTkFont(size=13),
            command=self._on_back,
        ).pack(anchor="w", pady=(0, 20))

        card = ctk.CTkFrame(self, corner_radius=14,
                            fg_color=bg, border_width=1, border_color=accent)
        card.pack(fill="x", padx=4)

        ctk.CTkFrame(card, width=6, fg_color=accent,
                     corner_radius=0).pack(side="left", fill="y")

        body = ctk.CTkFrame(card, fg_color="transparent")
        body.pack(side="left", fill="both", expand=True, padx=20, pady=20)

        ctk.CTkLabel(
            body,
            text=f"{ico}  {self._notif['title']}",
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color=accent, anchor="w",
        ).pack(anchor="w")

        ctk.CTkLabel(
            body,
            text=self._notif.get("time", ""),
            font=ctk.CTkFont(size=12),
            text_color="#6b7280", anchor="w",
        ).pack(anchor="w", pady=(4, 16))

        ctk.CTkFrame(body, height=1, fg_color=accent).pack(fill="x", pady=(0, 16))

        ctk.CTkLabel(
            body,
            text=self._notif["message"],
            font=ctk.CTkFont(size=14),
            text_color="#d1d5db", anchor="w",
            wraplength=520, justify="left",
        ).pack(anchor="w")


class NotificationView(ctk.CTkFrame):
    """Vue liste + détail des notifications."""

    def __init__(self, master, notifications: list):
        super().__init__(master, corner_radius=0, fg_color="transparent")
        self._notifications = notifications
        self._build_list()

    def _clear(self):
        for w in self.winfo_children():
            w.destroy()

    def _unread_count(self) -> int:
        return len([n for n in self._notifications if not n.get("read")])

    def _refresh_count(self):
        count = self._unread_count()
        if count:
            self._unread_label.configure(
                text=f"{count} non lue{'s' if count > 1 else ''}",
                fg_color="#3b1a1a",
            )
        else:
            self._unread_label.configure(text="", fg_color="transparent")

    def _build_list(self):
        self._clear()

        top = ctk.CTkFrame(self, fg_color="transparent")
        top.pack(fill="x", pady=(0, 16))

        ctk.CTkLabel(
            top,
            text="🔔  Notifications",
            font=ctk.CTkFont(size=26, weight="bold"),
            anchor="w",
        ).pack(side="left")

        self._unread_label = ctk.CTkLabel(
            top,
            text="",
            font=ctk.CTkFont(size=12),
            text_color="#ef4444",
            fg_color="#3b1a1a",
            corner_radius=8,
            padx=8, pady=2,
        )
        self._unread_label.pack(side="left", padx=12)
        self._refresh_count()

        self._scroll = ctk.CTkScrollableFrame(self, corner_radius=0, fg_color="transparent")
        self._scroll.pack(fill="both", expand=True)

        if not self._notifications:
            empty = ctk.CTkFrame(self._scroll, corner_radius=14,
                                 fg_color="#1e1e2e", height=200)
            empty.pack(fill="x", pady=8)
            empty.pack_propagate(False)
            ctk.CTkLabel(
                empty,
                text="✅  Aucune notification pour le moment.",
                font=ctk.CTkFont(size=14),
                text_color="gray",
            ).place(relx=0.5, rely=0.5, anchor="center")
            return

        for notif in reversed(self._notifications):
            self._add_card(notif)

    def _add_card(self, notif: dict):
        bg, accent, ico = _kind_style(notif.get("kind", "info"))
        is_read = notif.get("read", False)

        # Bordure simulée via frame extérieur couleur accent,
        # packé directement dans le CTkScrollableFrame (pas d'accès aux internals)
        border = tk.Frame(self._scroll, bg=accent)
        border.pack(fill="x", pady=3)

        # Fond intérieur
        row = tk.Frame(border, bg=bg)
        row.pack(fill="both", expand=True, padx=1, pady=1)

        # Barre accent à gauche
        tk.Frame(row, bg=accent, width=4).pack(side="left", fill="y")

        # Bouton suppression
        tk.Button(
            row, text="✕",
            bg=bg, fg="#6b7280",
            activebackground=bg, activeforeground="#d1d5db",
            relief="flat", bd=0,
            font=("Helvetica", 10),
            cursor="hand2",
            command=lambda n=notif, b=border: self._delete(n, b),
        ).pack(side="right", padx=(0, 8), anchor="center")

        # Pastille non-lu
        if not is_read:
            tk.Label(
                row, text="●",
                bg=bg, fg=accent,
                font=("Helvetica", 10),
            ).pack(side="right", padx=(0, 4), anchor="center")

        # Contenu : icône + titre + heure
        content = tk.Frame(row, bg=bg, cursor="hand2")
        content.pack(side="left", fill="both", expand=True, padx=(10, 0), pady=6)

        title_lbl = tk.Label(
            content,
            text=f"{ico}  {notif['title']}",
            bg=bg, fg=accent,
            font=("Helvetica", 11, "bold"),
            anchor="w", cursor="hand2",
        )
        title_lbl.pack(side="left")

        time_lbl = tk.Label(
            content,
            text=notif.get("time", ""),
            bg=bg, fg="#6b7280",
            font=("Helvetica", 10),
            anchor="w",
        )
        time_lbl.pack(side="left", padx=(10, 0))

        # Clic sur toute la zone
        for widget in (content, title_lbl, time_lbl, row):
            widget.bind("<Button-1>", lambda e, n=notif: self._open_detail(n))

    def _open_detail(self, notif: dict):
        notif["read"] = True
        self._clear()
        _NotifDetail(self, notif, on_back=self._build_list).pack(fill="both", expand=True)

    def _delete(self, notif: dict, border_frame):
        if notif in self._notifications:
            self._notifications.remove(notif)
        border_frame.destroy()
        self._refresh_count()