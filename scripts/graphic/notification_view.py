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

        count = len(self._notifications)
        if count:
            ctk.CTkLabel(
                top,
                text=f"{count} non lue{'s' if count > 1 else ''}",
                font=ctk.CTkFont(size=12),
                text_color="#ef4444",
                fg_color="#3b1a1a",
                corner_radius=8,
                padx=8, pady=2,
            ).pack(side="left", padx=12)

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

        card = ctk.CTkFrame(self._scroll, corner_radius=12,
                            fg_color=bg, border_width=1, border_color=accent,
                            cursor="hand2")
        card.pack(fill="x", pady=5)

        ctk.CTkFrame(card, width=4, fg_color=accent,
                     corner_radius=0).pack(side="left", fill="y")

        content = ctk.CTkFrame(card, fg_color="transparent", cursor="hand2")
        content.pack(side="left", fill="both", expand=True, padx=14, pady=12)
        content.bind("<Button-1>", lambda e, n=notif: self._open_detail(n))

        header = ctk.CTkFrame(content, fg_color="transparent")
        header.pack(fill="x")
        header.bind("<Button-1>", lambda e, n=notif: self._open_detail(n))

        title_lbl = ctk.CTkLabel(
            header,
            text=f"{ico}  {notif['title']}",
            font=ctk.CTkFont(size=13, weight="bold"),
            text_color=accent, anchor="w", cursor="hand2",
        )
        title_lbl.pack(side="left")
        title_lbl.bind("<Button-1>", lambda e, n=notif: self._open_detail(n))

        ctk.CTkLabel(
            header,
            text=notif.get("time", ""),
            font=ctk.CTkFont(size=11),
            text_color="#6b7280", anchor="e",
        ).pack(side="right")

        msg_lbl = ctk.CTkLabel(
            content,
            text=notif["message"],
            font=ctk.CTkFont(size=12),
            text_color="#d1d5db", anchor="w",
            wraplength=440, justify="left", cursor="hand2",
        )
        msg_lbl.pack(anchor="w", pady=(4, 0))
        msg_lbl.bind("<Button-1>", lambda e, n=notif: self._open_detail(n))

        ctk.CTkButton(
            card,
            text="✕", width=28, height=28,
            corner_radius=14,
            fg_color="transparent",
            text_color="#6b7280",
            hover_color=bg,
            font=ctk.CTkFont(size=12),
            command=lambda n=notif, c=card: self._delete(n, c),
        ).pack(side="right", padx=8, pady=8, anchor="n")

    def _open_detail(self, notif: dict):
        self._clear()
        _NotifDetail(self, notif, on_back=self._build_list).pack(fill="both", expand=True)

    def _delete(self, notif: dict, card):
        if notif in self._notifications:
            self._notifications.remove(notif)
        card.destroy()