# Conecta views e services
from typing import Optional, List, Dict
from services.business_logic import AutomationService


class MainController:
    def __init__(self):
        #self.current_user: Optional[User] = None
        pass

    def login(self, username: str, password: str) -> bool:
        """Realiza login"""
        return True

    def logout(self):
        """Realiza logout"""
        pass

    def create_automation(self) -> bool:
        """Cria nova automação"""
        # Inicia listeners para captura de comandos
        AutomationService.init_listeners()
        return True

    def run_automation(self, automation_id: int) -> bool:
        """Executa automação"""
        return AutomationService.execute_automation(automation_id)

    def update_automation(self, automation_id: int, **kwargs) -> bool:
        """Atualiza automação"""
        return AutomationService.update_automation(automation_id, **kwargs)

    def delete_automation(self, automation_id: int) -> bool:
        """Deleta automação"""
        return AutomationService.delete_automation(automation_id)