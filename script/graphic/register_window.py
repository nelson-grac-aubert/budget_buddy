import customtkinter as ctk
class Register_windows(ctk.CTkFrame):
    def __init__(self, master, on_register):
        super().__init__(master, corner_radius=0, fg_color="transparent")
        self._on_register = on_register
        self._build()

    def _build(self):
        # Conteneur centré
        container = ctk.CTkFrame(self, width=360, height=420, corner_radius=16)
        container.place(relx=0.5, rely=0.5, anchor="center")
        container.pack_propagate(False)

        # Logo / titre
        ctk.CTkLabel(
            container,
            text="💰 Budget Buddy",
            font=ctk.CTkFont(size=26, weight="bold"),
        ).pack(pady=(36, 4))

        ctk.CTkLabel(
            container,
            text="Créez votre compte",
            font=ctk.CTkFont(size=13),
            text_color="gray",
        ).pack(pady=(0, 24))