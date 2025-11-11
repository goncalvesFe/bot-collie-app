import customtkinter as ctk

class LoginWindow(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        # Configuração da janela
        self.title("Login - Bot Collie")
        self.geometry("1000x700")
        
        # Configuração do tema
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        # Frame principal
        self.frame = ctk.CTkFrame(master=self)
        self.frame.pack(pady=20, padx=40, fill="both", expand=True)
        
        # Label do título
        self.label = ctk.CTkLabel(master=self.frame, text="Login Sistema", font=("Roboto", 24))
        self.label.pack(pady=12, padx=10)
        
        # Campo de usuário
        self.username_entry = ctk.CTkEntry(master=self.frame, placeholder_text="Usuário", width=200, height=30)
        self.username_entry.pack(pady=12, padx=10)
        
        # Campo de senha
        self.password_entry = ctk.CTkEntry(master=self.frame, placeholder_text="Senha", show="*", width=200, height=30)
        self.password_entry.pack(pady=12, padx=10)
        
        # Botão de login
        self.login_button = ctk.CTkButton(master=self.frame, text="Entrar", command=self.login_event, width=200, height=30)
        self.login_button.pack(pady=12, padx=10)
    
    def login_event(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        # Aqui você pode adicionar a lógica de autenticação
        print(f"Tentativa de login - Usuário: {username}")

if __name__ == "__main__":
    app = LoginWindow()
    app.mainloop()