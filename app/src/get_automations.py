import sqlite3


def get_automations():
    database = sqlite3.connect('db-bot-collie.db', check_same_thread=False)
    cursor = database.cursor()

    automations = cursor.execute('SELECT * FROM automacao').fetchall()
    
    return automations
