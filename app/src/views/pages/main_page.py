import customtkinter as ctk


class MainPage(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        # Frame principal
        self.frame = ctk.CTkFrame(master=self)
        self.frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Label do título
        self.title_label = ctk.CTkLabel(
            master=self.frame, 
            text="BotCollie", 
            font=("Roboto", 36)
        )
        self.title_label.pack(pady=20)

        # Aqui você pode adicionar mais componentes da página principal
        self.welcome_label = ctk.CTkLabel(
            master=self.frame, 
            text="Bem-vindo ao BotCollie!", 
            font=("Roboto", 18)
        )
        self.welcome_label.pack(pady=10)