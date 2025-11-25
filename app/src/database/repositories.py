# Operações CRUD
from typing import List, Optional
# Operações CRUD
from typing import List, Optional
from datetime import datetime
from database.connection import DatabaseConnection
from database.models import Automation, Command


class AutomationRepository:
    @staticmethod
    def create(automation: Automation) -> int | None:
        """Cria nova automação"""
        with DatabaseConnection.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO automations
                (name, description)
                VALUES (?, ?)
            """, (
                automation.name,
                automation.description,
            ))
            return cursor.lastrowid

    @staticmethod
    def update(automation: Automation) -> bool:
        """Atualiza automação"""
        return True

    @staticmethod
    def delete(automation_id: int) -> bool:
        """Deleta automação"""
        return True

class CommandRepository:
    @staticmethod
    def create(command: Command) -> int | None:
        """Cria log de execução"""
        with DatabaseConnection.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO commands
                (automation_id, type, subtype, command, cmdOrder)
                VALUES (?, ?, ?, ?, ?)
            """, (
                command.automation_id,
                command.type,
                command.subtype,
                command.command,
                command.cmdOrder
            ))
            return cursor.lastrowid