import customtkinter as ctk


class LoginPage(ctk.CTkFrame):
    def __init__(self, master, on_login_success=None):
        super().__init__(master)

        self.on_login_success = on_login_success

        # Frame central
        self.frame = ctk.CTkFrame(master=self)
        self.frame.pack(pady=20, padx=40, fill="both", expand=True)

        # Label do título
        self.label = ctk.CTkLabel(
            master=self.frame, 
            text="Login", 
            font=("Roboto", 40)
        )
        self.label.pack(pady=12, padx=10)

        # Campo de usuário
        self.username_entry = ctk.CTkEntry(
            master=self.frame, 
            placeholder_text="Usuário", 
            width=300, 
            height=40
        )
        self.username_entry.pack(pady=12, padx=10)

        # Campo de senha
        self.password_entry = ctk.CTkEntry(
            master=self.frame, 
            placeholder_text="Senha", 
            show="*", 
            width=300, 
            height=40
        )
        self.password_entry.pack(pady=12, padx=10)

        # Botão de login
        self.login_button = ctk.CTkButton(
            master=self.frame, 
            text="Entrar", 
            command=self.login_event, 
            width=300, 
            height=40
        )
        self.login_button.pack(pady=12, padx=10)

        # Bind da tecla Enter para fazer login
        self.password_entry.bind("<Return>", lambda event: self.login_event())

    def login_event(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        # Aqui você pode adicionar validação de credenciais
        if username and password:
            print(f"Tentativa de login - Usuário: {username}")
            
            # Chama callback de sucesso se fornecido
            if self.on_login_success:
                self.on_login_success(username)
        else:
            print("Por favor, preencha todos os campos")