# arquivo cria banco e tabelas, rodar apenas uma vez
import sqlite3

database = sqlite3.connect('db-bot-collie.db')

cursor = database.cursor()

cursor.execute("CREATE TABLE automacao (id int, name text)")

cursor.execute("CREATE TABLE comando (id int, automacao_id int, command text)")

database.commit()
