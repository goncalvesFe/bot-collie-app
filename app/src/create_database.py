# arquivo cria banco e tabelas, rodar apenas uma vez
# https://pypi.org/project/db-sqlite3/
import sqlite3

database = sqlite3.connect('db-bot-collie.db')

cursor = database.cursor()

cursor.execute("CREATE TABLE automacao (id int, name text)")

cursor.execute("CREATE TABLE comando (id int, automacao_id int, command text)")

database.commit()

# cursor = database.cursor()
# cursor.execute("SELECT * FROM automacao")
# print('automacao')
# print(cursor.fetchall())
# cursor.execute("SELECT * FROM comando")
# print('comando')
# print(cursor.fetchall())
