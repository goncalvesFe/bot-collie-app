import customtkinter as ctk
from controllers.main_controller import MainController


class MainPage(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

         # Controller to handle business operations
        self.controller = MainController()

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

        # Cabeçalho da tabela
        self.header_frame = ctk.CTkFrame(master=self.frame)
        self.header_frame.pack(fill="x", padx=5, pady=5)

        ctk.CTkLabel(
            master=self.header_frame,
            text="Nome",
            font=("Roboto", 14, "bold"),
            width=200
        ).pack(side="left", padx=10)

        ctk.CTkLabel(
            master=self.header_frame,
            text="Última Execução",
            font=("Roboto", 14, "bold"),
            width=150
        ).pack(side="left", padx=10)

        ctk.CTkLabel(
            master=self.header_frame,
            text="Ações",
            font=("Roboto", 14, "bold"),
            width=250
        ).pack(side="left", padx=10)

        # Frame scrollável da tabela
        self.scrollable_frame = ctk.CTkScrollableFrame(
            master=self.frame,
            height=300
        )
        self.scrollable_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Frame para as linhas da tabela
        self.table_content_frame = ctk.CTkFrame(
            master=self.scrollable_frame,
            fg_color="transparent"
        )
        self.table_content_frame.pack(fill="both", expand=True)

        # Dados estáticos (exemplo) - adicionei mais itens para testar o scroll
        automations = [
            {"nome": "Automação 1", "ultima_execucao": "14/11/2025 10:30"},
            {"nome": "Automação 2", "ultima_execucao": "13/11/2025 15:45"},
            {"nome": "Automação 3", "ultima_execucao": "12/11/2025 09:20"},
            {"nome": "Automação 4", "ultima_execucao": "11/11/2025 14:15"},
            {"nome": "Automação 5", "ultima_execucao": "10/11/2025 11:00"},
            {"nome": "Automação 6", "ultima_execucao": "09/11/2025 16:30"},
            {"nome": "Automação 7", "ultima_execucao": "08/11/2025 08:45"},
            {"nome": "Automação 8", "ultima_execucao": "07/11/2025 13:20"},
            {"nome": "Automação 9", "ultima_execucao": "06/11/2025 10:10"},
            {"nome": "Automação 10", "ultima_execucao": "05/11/2025 15:55"},
            {"nome": "Automação 11", "ultima_execucao": "04/11/2025 09:35"},
            {"nome": "Automação 12", "ultima_execucao": "03/11/2025 14:50"},
            {"nome": "Automação 13", "ultima_execucao": "02/11/2025 11:25"},
            {"nome": "Automação 14", "ultima_execucao": "01/11/2025 16:40"},
        ]

        # Criando linhas da tabela
        for automation in automations:
            self.create_table_row(automation)

        # Botão de adicionar nova automação (fixado abaixo da tabela)
        self.add_button = ctk.CTkButton(
            master=self.frame,
            text="+ Adicionar Nova Automação",
            font=("Roboto", 14, "bold"),
            height=40,
            command=self.add_automation
        )
        self.add_button.pack(fill="x", padx=10, pady=10)

    def create_table_row(self, automation):
        """Cria uma linha da tabela com os dados da automação"""
        row_frame = ctk.CTkFrame(master=self.table_content_frame)
        row_frame.pack(fill="x", padx=5, pady=2)

        # Nome
        ctk.CTkLabel(
            master=row_frame,
            text=automation["nome"],
            font=("Roboto", 12),
            width=200,
            anchor="w"
        ).pack(side="left", padx=10, pady=10)

        # Última Execução
        ctk.CTkLabel(
            master=row_frame,
            text=automation["ultima_execucao"],
            font=("Roboto", 12),
            width=150,
            anchor="w"
        ).pack(side="left", padx=10, pady=10)

        # Frame de ações
        actions_frame = ctk.CTkFrame(master=row_frame, fg_color="transparent")
        actions_frame.pack(side="left", padx=10)

        # Botão Rodar
        ctk.CTkButton(
            master=actions_frame,
            text="▶ Rodar",
            width=70,
            height=28,
            command=lambda: self.run_automation(automation["nome"])
        ).pack(side="left", padx=2)

        # Botão Editar
        ctk.CTkButton(
            master=actions_frame,
            text="✎ Editar",
            width=70,
            height=28,
            command=lambda: self.edit_automation(automation["nome"])
        ).pack(side="left", padx=2)

        # Botão Excluir
        ctk.CTkButton(
            master=actions_frame,
            text="🗑 Excluir",
            width=70,
            height=28,
            fg_color="#dc3545",
            hover_color="#c82333",
            command=lambda: self.delete_automation(automation["nome"])
        ).pack(side="left", padx=2)

    def add_automation(self):
        """Função para adicionar nova automação"""
        self.controller.create_automation()

    def run_automation(self, nome):
        """Função para rodar a automação"""
        print(f"Rodando automação: {nome}")

    def edit_automation(self, nome):
        """Função para editar a automação"""
        print(f"Editando automação: {nome}")

    def delete_automation(self, nome):
        """Função para excluir a automação"""
        print(f"Excluindo automação: {nome}")