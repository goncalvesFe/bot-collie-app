# Regras de negócio
import hashlib
from typing import Optional, List, Dict
from database.repositories import (
    UserRepository, 
    AutomationRepository, 
    ExecutionLogRepository
)
from database.models import User, Automation, ExecutionLog
import subprocess
import threading

class AuthService:
    @staticmethod
    def hash_password(password: str) -> str:
        """Cria hash da senha"""
        return hashlib.sha256(password.encode()).hexdigest()

    @staticmethod
    def register_user(username: str, password: str) -> bool:
        """Registra novo usuário"""
        try:
            user = User(
                username=username,
                password_hash=AuthService.hash_password(password)
            )
            UserRepository.create(user)
            return True
        except Exception as e:
            print(f"Erro ao registrar usuário: {e}")
            return False

    @staticmethod
    def authenticate(username: str, password: str) -> Optional[User]:
        """Autentica usuário"""
        user = UserRepository.find_by_username(username)
        if user and user.password_hash == AuthService.hash_password(password):
            return user
        return None

class AutomationService:
    @staticmethod
    def create_automation(user_id: int, nome: str, descricao: str = "", 
                         script_path: str = "") -> Optional[int]:
        """Cria nova automação"""
        try:
            automation = Automation(
                user_id=user_id,
                nome=nome,
                descricao=descricao,
                script_path=script_path,
                status="inativa"
            )
            return AutomationRepository.create(automation)
        except Exception as e:
            print(f"Erro ao criar automação: {e}")
            return None

    @staticmethod
    def get_user_automations(user_id: int) -> List[Dict]:
        """Retorna automações com última execução"""
        automations = AutomationRepository.find_all_by_user(user_id)
        result = []
        
        for auto in automations:
            last_exec = ExecutionLogRepository.get_last_execution(auto.id)
            result.append({
                "id": auto.id,
                "nome": auto.nome,
                "descricao": auto.descricao,
                "status": auto.status,
                "ultima_execucao": last_exec.finished_at if last_exec else "Nunca executada"
            })
        
        return result

    @staticmethod
    def execute_automation(automation_id: int) -> bool:
        """Executa automação em thread separada"""
        automation = AutomationRepository.find_by_id(automation_id)
        if not automation or not automation.script_path:
            return False

        # Cria log de início
        log = ExecutionLog(
            automation_id=automation_id,
            status="em_execucao"
        )
        log_id = ExecutionLogRepository.create(log)

        # Executa em thread
        thread = threading.Thread(
            target=AutomationService._run_script,
            args=(automation.script_path, log_id)
        )
        thread.start()
        return True

    @staticmethod
    def _run_script(script_path: str, log_id: int):
        """Executa script e atualiza log"""
        try:
            result = subprocess.run(
                ["python", script_path],
                capture_output=True,
                text=True,
                timeout=300  # 5 minutos timeout
            )
            
            status = "sucesso" if result.returncode == 0 else "erro"
            log_output = result.stdout
            error_msg = result.stderr if result.returncode != 0 else None
            
            ExecutionLogRepository.update_execution(
                log_id, status, log_output, error_msg
            )
        except Exception as e:
            ExecutionLogRepository.update_execution(
                log_id, "erro", "", str(e)
            )

    @staticmethod
    def update_automation(automation_id: int, **kwargs) -> bool:
        """Atualiza automação"""
        automation = AutomationRepository.find_by_id(automation_id)
        if not automation:
            return False

        for key, value in kwargs.items():
            if hasattr(automation, key):
                setattr(automation, key, value)

        return AutomationRepository.update(automation)

    @staticmethod
    def delete_automation(automation_id: int) -> bool:
        """Deleta automação"""
        return AutomationRepository.delete(automation_id)