import sqlite3
from tkinter import *
from tkinter import ttk

import add_automation

database = sqlite3.connect('db-bot-collie.db')

root = Tk()

root.title('Bot Collie')
root.configure(background='#babdc2')
root.geometry("700x500")
root.resizable(True, True)
root.maxsize(width=900, height=700) # se clicar em ampliar ele permite aumentar a tela acima desse limite
root.minsize(width=400, height=300)

frame = Frame(bd=4, bg='#edeff2', highlightbackground='blue', highlightthickness=3)
frame.place(relx=0.02, rely=0.02, relwidth=0.96, relheight=0.46)

logo = Label(frame, text="Logo aqui",bg='#edeff2')
logo.place(relx=0, rely=0, relwidth=0.3, relheight=0.3)

add_automation_button = Button(frame, text='+', command=add_automation)
add_automation_button.place(relx=0.5, rely=0, relwidth=0.055, relheight=0.2)

frame2 = Frame(bd=4, bg='#edeff2', highlightbackground='blue', highlightthickness=3)
frame2.place(relx=0.02, rely=0.5, relwidth=0.96, relheight=0.46)

# frm = ttk.Frame(root, padding=10)
# frm.grid()
# ttk.Label(frm, text="Logo aqui").grid(column=0, row=0)
# ttk.Label(frm, text="Adicionar automação").grid(column=1, row=1, padx=10)
# ttk.Button(frm, text="+", command=add_automation).grid(column=2, row=1)

root.mainloop()
