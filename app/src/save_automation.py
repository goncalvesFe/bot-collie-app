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
    str_uppercase = string.ascii_uppercase
    digits = string.digits
    special_char = string.punctuation

    default_name = default_name + get_random(str_lowercase, 3)
    default_name = default_name + get_random(special_char, 1)
    default_name = default_name + get_random(digits, 5)
    default_name = default_name + get_random(special_char, 1)
    default_name = default_name + get_random(str_uppercase, 2)

    return default_name

def save_automation(commands):
    print(commands)
    aut_id = 1
    cmd_id = 1

    # buscar no banco os ultimos ids salvos
    last_automation_id = cursor.execute('SELECT MAX(id) FROM automacao').fetchone()[0]
    last_command_id = cursor.execute('SELECT MAX(id) FROM comando').fetchone()[0]

    # só pra ver se os dados estão sendo salvos - deletar depois
    data_aut = cursor.execute('SELECT * FROM automacao').fetchall()
    print(data_aut)
    data_cmd = cursor.execute('SELECT * FROM comando').fetchall()
    print(data_cmd)

    if (last_automation_id != None):
        aut_id = aut_id + last_automation_id

    if (last_command_id != None):
        cmd_id = cmd_id + last_command_id

    # salvar nova automação na tabela automação com o id somando 1 em relação ao último
    automation_name = 'aut-' + get_random_default_aut_name()
    insert_aut = f"INSERT INTO automacao (id, name) VALUES ({aut_id}, '{automation_name}')"
    print(insert_aut)
    cursor.execute(insert_aut)

    # salvar na tabela comando os comandos passados por parametro
    for comando in commands:
        print(type(comando))
        insert_cmd = f"INSERT INTO comando (id, automacao_id, command) VALUES ({cmd_id}, {aut_id}, {comando})"
        print(insert_cmd)
        cursor.execute(insert_cmd)
        cmd_id = cmd_id + 1

# DEPOIS TENTAR VOLTAR COM AQUELA VERIFICAÇÃO DO LISTENER DO KEYBOARD
# TRATAR OS COMANDO PRIMEIRO LÁ ANTES DE ENVIAR PARA CÁ
