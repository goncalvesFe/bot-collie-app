# Configurações gerais (paths, constantes)
import os
from pathlib import Path

# Diretórios
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
ASSETS_DIR = BASE_DIR / "assets"

# Banco de dados
DATABASE_PATH = DATA_DIR / "bot-collie.db"

# Criar diretórios se não existirem
DATA_DIR.mkdir(exist_ok=True)
ASSETS_DIR.mkdir(exist_ok=True)

# Outras configurações
APP_NAME = "BotCollie"
APP_VERSION = "1.0.0"