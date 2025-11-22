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
            
            # Tabela de usuários
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE NOT NULL,
                    password_hash TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # Tabela de automações
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS automations (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    nome TEXT NOT NULL,
                    descricao TEXT,
                    script_path TEXT,
                    status TEXT DEFAULT 'inativa',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users (id)
                )
            """)
            
            # Tabela de logs de execução
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS execution_logs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    automation_id INTEGER NOT NULL,
                    started_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    finished_at TIMESTAMP,
                    status TEXT DEFAULT 'em_execucao',
                    log_output TEXT,
                    error_message TEXT,
                    FOREIGN KEY (automation_id) REFERENCES automations (id)
                )
            """)