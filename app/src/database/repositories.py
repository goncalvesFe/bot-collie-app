# Operações CRUD
from typing import List, Optional
from datetime import datetime
from database.connection import DatabaseConnection
from database.models import User, Automation, ExecutionLog

class UserRepository:
    @staticmethod
    def create(user: User) -> int | None:
        """Cria novo usuário"""
        with DatabaseConnection.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO users (username, password_hash) VALUES (?, ?)",
                (user.username, user.password_hash)
            )
            return cursor.lastrowid

    @staticmethod
    def find_by_username(username: str) -> Optional[User]:
        """Busca usuário por username"""
        with DatabaseConnection.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
            row = cursor.fetchone()
            if row:
                return User(
                    id=row['id'],
                    username=row['username'],
                    password_hash=row['password_hash'],
                    created_at=row['created_at']
                )
        return None

class AutomationRepository:
    @staticmethod
    def create(automation: Automation) -> int | None:
        """Cria nova automação"""
        with DatabaseConnection.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO automations 
                (user_id, nome, descricao, script_path, status)
                VALUES (?, ?, ?, ?, ?)
            """, (
                automation.user_id,
                automation.nome,
                automation.descricao,
                automation.script_path,
                automation.status
            ))
            return cursor.lastrowid

    @staticmethod
    def find_all_by_user(user_id: int) -> List[Automation]:
        """Lista todas automações de um usuário"""
        with DatabaseConnection.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT * FROM automations WHERE user_id = ? ORDER BY created_at DESC",
                (user_id,)
            )
            rows = cursor.fetchall()
            return [
                Automation(
                    id=row['id'],
                    user_id=row['user_id'],
                    nome=row['nome'],
                    descricao=row['descricao'],
                    script_path=row['script_path'],
                    status=row['status'],
                    created_at=row['created_at'],
                    updated_at=row['updated_at']
                )
                for row in rows
            ]

    @staticmethod
    def update(automation: Automation) -> bool:
        """Atualiza automação"""
        with DatabaseConnection.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE automations 
                SET nome = ?, descricao = ?, script_path = ?, 
                    status = ?, updated_at = CURRENT_TIMESTAMP
                WHERE id = ?
            """, (
                automation.nome,
                automation.descricao,
                automation.script_path,
                automation.status,
                automation.id
            ))
            return cursor.rowcount > 0

    @staticmethod
    def delete(automation_id: int) -> bool:
        """Deleta automação"""
        with DatabaseConnection.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM automations WHERE id = ?", (automation_id,))
            return cursor.rowcount > 0

    @staticmethod
    def find_by_id(automation_id: int) -> Optional[Automation]:
        """Busca automação por ID"""
        with DatabaseConnection.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM automations WHERE id = ?", (automation_id,))
            row = cursor.fetchone()
            if row:
                return Automation(
                    id=row['id'],
                    user_id=row['user_id'],
                    nome=row['nome'],
                    descricao=row['descricao'],
                    script_path=row['script_path'],
                    status=row['status'],
                    created_at=row['created_at'],
                    updated_at=row['updated_at']
                )
        return None

class ExecutionLogRepository:
    @staticmethod
    def create(log: ExecutionLog) -> int | None:
        """Cria log de execução"""
        with DatabaseConnection.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO execution_logs 
                (automation_id, status, log_output)
                VALUES (?, ?, ?)
            """, (log.automation_id, log.status, log.log_output))
            return cursor.lastrowid

    @staticmethod
    def get_last_execution(automation_id: int | None) -> Optional[ExecutionLog]:
        """Busca última execução de uma automação"""
        with DatabaseConnection.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT * FROM execution_logs 
                WHERE automation_id = ? 
                ORDER BY started_at DESC 
                LIMIT 1
            """, (automation_id,))
            row = cursor.fetchone()
            if row:
                return ExecutionLog(
                    id=row['id'],
                    automation_id=row['automation_id'],
                    started_at=row['started_at'],
                    finished_at=row['finished_at'],
                    status=row['status'],
                    log_output=row['log_output'],
                    error_message=row['error_message']
                )
        return None

    @staticmethod
    def update_execution(log_id: int, status: str, log_output: str, 
                        error_message: Optional[str] = None) -> bool:
        """Atualiza log de execução"""
        with DatabaseConnection.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE execution_logs 
                SET finished_at = CURRENT_TIMESTAMP, status = ?, 
                    log_output = ?, error_message = ?
                WHERE id = ?
            """, (status, log_output, error_message, log_id))
            return cursor.rowcount > 0