# Conecta views e services
from typing import Optional, List, Dict
from services.business_logic import AuthService, AutomationService
from database.models import User

class MainController:
    def __init__(self):
        self.current_user: Optional[User] = None

    def login(self, username: str, password: str) -> bool:
        """Realiza login"""
        user = AuthService.authenticate(username, password)
        if user:
            self.current_user = user
            return True
        return False

    def logout(self):
        """Realiza logout"""
        self.current_user = None

    def get_automations(self) -> List[Dict]:
        """Retorna automações do usuário logado"""
        if not self.current_user:
            return []
        return AutomationService.get_user_automations(self.current_user.id)

    def create_automation(self, nome: str, descricao: str = "", 
                         script_path: str = "") -> bool:
        """Cria nova automação"""
        if not self.current_user:
            return False
        result = AutomationService.create_automation(
            self.current_user.id, nome, descricao, script_path
        )
        return result is not None

    def run_automation(self, automation_id: int) -> bool:
        """Executa automação"""
        return AutomationService.execute_automation(automation_id)

    def update_automation(self, automation_id: int, **kwargs) -> bool:
        """Atualiza automação"""
        return AutomationService.update_automation(automation_id, **kwargs)

    def delete_automation(self, automation_id: int) -> bool:
        """Deleta automação"""
        return AutomationService.delete_automation(automation_id)