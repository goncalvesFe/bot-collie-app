# Gerenciamento de conexão com BD
import sqlite3
from contextlib import contextmanager
from config.settings import DATABASE_PATH

class DatabaseConnection:
    @staticmethod
    @contextmanager
    def get_connection():
        """Context manager para conexão segura"""
        conn = sqlite3.connect(DATABASE_PATH)
        conn.row_factory = sqlite3.Row  # Permite acessar colunas por nome
        try:
            yield conn
            conn.commit()
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()

    @staticmethod
    def initialize_database():
        """Cria as tabelas se não existirem"""
        with DatabaseConnection.get_connection() as conn:
            cursor = conn.cursor()
            
            # Tabela de automações
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS automations (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    description TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # Tabela de comandos
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS commands (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    automation_id INTEGER NOT NULL,
                    type TEXT,
                    subtype TEXT,
                    command TEXT, 
                    cmdOrder INTEGER
                )
            """)