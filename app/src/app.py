import customtkinter as ctk
from views.pages.login_page import LoginPage
from views.pages.main_page import MainPage


class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Configuração da janela
        self.title("BotCollie")
        self.geometry("800x700")

        # Configuração do tema
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        # Estado de login
        self.logged_in = False

        # Inicia com a tela de login
        self.show_login_page()

    def show_login_page(self):
        # Remove frame atual se existir
        for widget in self.winfo_children():
            widget.destroy()

        # Cria e exibe página de login
        login_page = LoginPage(self, on_login_success=self.on_login_success)
        login_page.pack(fill="both", expand=True)

    def show_main_page(self):
        # Remove frame atual se existir
        for widget in self.winfo_children():
            widget.destroy()

        # Cria e exibe página principal
        main_page = MainPage(self)
        main_page.pack(fill="both", expand=True)

    def on_login_success(self, username):
        print(f"Login bem-sucedido - Usuário: {username}")
        self.logged_in = True
        self.show_main_page()


if __name__ == "__main__":
    app = App()
    app.mainloop()