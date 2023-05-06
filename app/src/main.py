import random
import sqlite3
import string
from tkinter import *
from tkinter import ttk

root = Tk()

class Funcs():
    def get_automations(self):
        print('vou buscar mais tarde')
    def connect_database(self):
        self.conn = sqlite3.connect('bot-collie.db', check_same_thread=False)
        self.cursor = self.conn.cursor()
    def disconnect_database(self):
        self.conn.close()
    def create_tables(self):
        self.connect_database()
        self.cursor.execute('CREATE TABLE IF NOT EXISTS automacao (id integer PRIMARY KEY, name text)')
        self.cursor.execute("CREATE TABLE IF NOT EXISTS comando (id integer PRIMARY KEY, automacao_id int, command text)")
        self.conn.commit()
        self.disconnect_database()
    def add_automation(self):
        self.connect_database()
        self.auts = self.cursor.execute('SELECT * FROM automacao').fetchall()
        # quando for salvar o nome de uma automacao usar o padrao: automacao-id_da_aut
        print(self.auts)
        self.disconnect_database()

class Application(Funcs):
    def __init__(self):
        self.root = root
        self.screen()
        self.screen_frames()
        self.widgets_frame_1()
        self.widgets_frame_2()
        self.get_automations()
        self.create_tables()
        root.mainloop()
    def screen(self):
        self.root.title('Bot Collie')
        self.root.configure(background='#babdc2')
        self.root.geometry("900x700")
        self.root.resizable(True, True)
        self.root.maxsize(width=1100, height=900)
        self.root.minsize(width=400, height=300)
    def screen_frames(self):
        self.frame_1 = Frame(self.root, bd=4, bg='#edeff2', highlightbackground='white', highlightthickness=3)
        self.frame_1.place(relx=0.02, rely=0.02, relwidth=0.96, relheight=0.25)
        self.frame_2 = Frame(self.root, bd=4, bg='#edeff2', highlightbackground='white', highlightthickness=3)
        self.frame_2.place(relx=0.02, rely=0.3, relwidth=0.96, relheight=0.68)
    def widgets_frame_1(self):
        self.logo = Label(self.frame_1, text='Logo aqui', bg='#edeff2')
        self.logo.place(relx=0, rely=0, relwidth=0.1, relheight=0.1)
        self.btn_add_aut = Button(self.frame_1, text='Criar nova automação', bd=2, bg='#00A86B', fg='white')
        self.btn_add_aut.place(relx=0, rely=0.5, relwidth=0.23, relheight=0.30)
    def widgets_frame_2(self):
        self.aut_list = ttk.Treeview(self.frame_2, height=3, column=('col1', 'col2', 'col3', 'col4'))
        self.aut_list.heading('#0', text='')
        self.aut_list.heading('#1', text='codigo')
        self.aut_list.heading('#2', text='nome')
        self.aut_list.heading('#3', text='telefone')
        self.aut_list.heading('#4', text='cidade')

        self.aut_list.column('#0', width=1)
        self.aut_list.column('#1', width=50)
        self.aut_list.column('#2', width=200)
        self.aut_list.column('#3', width=125)
        self.aut_list.column('#4', width=125)

        self.aut_list.place(relx=0, rely=0, relwidth=0.97, relheight=1)

        self.scroll = Scrollbar(self.frame_2, orient='vertical')
        self.aut_list.configure(yscroll=self.scroll)
        self.scroll.place(relx=0.97, rely=0, relwidth=0.02, relheight=1)


Application()
