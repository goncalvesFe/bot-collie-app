# Modelos/esquemas das tabelas
from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class User:
    id: Optional[int] = None
    username: str = ""
    password_hash: str = ""
    created_at: Optional[datetime] = None

@dataclass
class Automation:
    id: Optional[int] = None
    user_id: int = 0
    nome: str = ""
    descricao: str = ""
    script_path: str = ""  # Caminho do script de automação
    status: str = "inativa"  # ativa, inativa, executando
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

@dataclass
class ExecutionLog:
    id: Optional[int] = None
    automation_id: int = 0
    started_at: Optional[datetime] = None
    finished_at: Optional[datetime] = None
    status: str = ""  # sucesso, erro, em_execucao
    log_output: str = ""
    error_message: Optional[str] = None