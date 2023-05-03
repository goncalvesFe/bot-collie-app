import random
import sqlite3
import string

database = sqlite3.connect('db-bot-collie.db', check_same_thread=False)

cursor = database.cursor()

def get_random(choices, range_number):
    random_choices = ''
    for i in range(range_number):
        random_choices = random_choices + random.choice(choices)
    
    return random_choices

def get_random_default_aut_name():
    default_name = ''
    str_lowercase = string.ascii_lowercase
    digits = string.digits
    special_char = string.punctuation

    default_name = default_name + get_random(str_lowercase, 3)
    default_name = default_name + get_random(special_char, 1)
    default_name = default_name + get_random(digits, 5)

    return default_name

def insert_command(id, aut_id, command):
    insert_cmd = f"INSERT INTO comando (id, automacao_id, command) VALUES ({id}, {aut_id}, {command})"
    cursor.execute(insert_cmd)

def save_automation(commands):
    aut_id = 1
    cmd_id = 1

    # buscar no banco os ultimos ids salvos
    last_automation_id = cursor.execute('SELECT MAX(id) FROM automacao').fetchone()[0]
    last_command_id = cursor.execute('SELECT MAX(id) FROM comando').fetchone()[0]

    if (last_automation_id != None):
        aut_id = aut_id + last_automation_id

    if (last_command_id != None):
        cmd_id = cmd_id + last_command_id

    # salvar nova automação na tabela automação com o id somando 1 em relação ao último
    automation_name = 'aut-' + get_random_default_aut_name()
    insert_aut = f"INSERT INTO automacao (id, name) VALUES ({aut_id}, '{automation_name}')"
    cursor.execute(insert_aut)

    # salvar na tabela comando os comandos passados por parametro
    for comando in commands:
        if hasattr(comando, 'char'):
            insert_command(cmd_id, aut_id, comando)
        else:
            cmd = f"'{comando}'"
            insert_command(cmd_id, aut_id, cmd)
        
        cmd_id = cmd_id + 1

    database.commit()

# DEPOIS TENTAR VOLTAR COM AQUELA VERIFICAÇÃO DO LISTENER DO KEYBOARD
# TRATAR OS COMANDO PRIMEIRO LÁ ANTES DE ENVIAR PARA CÁ
