from tkinter import *
from tkinter import ttk

root = Tk()

root.title('Bot Collie')
frm = ttk.Frame(root, padding=10)
frm.grid()
ttk.Label(frm, text="Logo aqui").grid(column=0, row=0)
ttk.Label(frm, text="Adicionar automação").grid(column=1, row=1, padx=10)
ttk.Button(frm, text="+", command=root.destroy).grid(column=2, row=1)

root.mainloop()
