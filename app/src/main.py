import sqlite3
from tkinter import *
from tkinter import ttk

import add_automation

database = sqlite3.connect('db-bot-collie.db')

root = Tk()

root.title('Bot Collie')
root.configure(background='red')
root.geometry("700x500")
root.resizable(True, True)
root.maxsize(width=900, height=700) # se clicar em ampliar ele permite aumentar a tela acima desse limite
root.minsize(width=400, height=300)
frm = ttk.Frame(root, padding=10)
frm.grid()
ttk.Label(frm, text="Logo aqui").grid(column=0, row=0)
ttk.Label(frm, text="Adicionar automação").grid(column=1, row=1, padx=10)
ttk.Button(frm, text="+", command=add_automation).grid(column=2, row=1)

root.mainloop()
