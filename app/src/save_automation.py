import sqlite3

database = sqlite3.connect('db-bot-collie.db', check_same_thread=False)

cursor = database.cursor()


def save_automation():
    aut_id = 1

    # buscar no banco qual foi a ultima automação salva
    last_automation_id = cursor.execute('SELECT MAX(id) FROM automacao').fetchone()[0]
    print(last_automation_id)
    if (last_automation_id != None):
        aut_id = last_automation_id + 1

    # salvar nova automação na tabela automação com o id somando 1 em relação ao último
    # salvar na tabela comando os comandos passados por parametro
