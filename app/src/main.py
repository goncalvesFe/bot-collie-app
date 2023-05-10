import sqlite3
from tkinter import *
from tkinter import ttk

from pynput import keyboard, mouse

root = Tk()

class Funcs():
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
    def save_commands(self):
        self.connect_database
        for command in self.commands:
            if hasattr(command, 'char'):
                insert_query = f"INSERT INTO comando (automacao_id, command) VALUES ({self.new_aut_id}, {command})"
                self.cursor.execute(insert_query)
            else:
                cmd = f"'{command}'"
                insert_query = f"INSERT INTO comando (automacao_id, command) VALUES ({self.new_aut_id}, {cmd})"
                self.cursor.execute(insert_query)
        self.conn.commit()
        self.disconnect_database()
    def save_automation(self):
        aut_id = 1
        self.connect_database()
        las_aut_id = self.cursor.execute('SELECT MAX(id) FROM automacao').fetchone()[0]
        if las_aut_id != None:
            aut_id = aut_id + las_aut_id
        aut_name = f'automacao-{aut_id}'
        self.cursor.execute(f"INSERT INTO automacao (name) VALUES ('{aut_name}')")
        self.conn.commit()
        self.new_aut_id = aut_id
        self.save_commands()
        self.disconnect_database()
        self.update_list()
    def update_list(self):
        self.aut_list.delete(*self.aut_list.get_children())
        self.connect_database()
        list = self.cursor.execute('SELECT name FROM  automacao')
        for i in list:
            self.aut_list.insert("", END, values=i)
        self.disconnect_database()
    def add_automation(self):
        print('hora do show')
        def on_press(key):
            self.commands.append(key)
            try:
                print('alphanumeric key {0} pressed'.format(key.char))
            except AttributeError:
                print('special key {0} pressed'.format(key))
        def on_release(key):
            if key == keyboard.Key.esc:
                print('stop listener')
                for command in self.commands:
                    print(command)
                self.save_automation()
                # Stop listener
                return False
        keyboard_listener = keyboard.Listener(on_press=on_press, on_release=on_release)
        keyboard_listener.start()
    def temp_check_tables(self):
        self.connect_database()
        auts = self.cursor.execute('SELECT * FROM automacao').fetchall()
        cmds = self.cursor.execute('SELECT * FROM comando').fetchall()
        self.disconnect_database()
        print('Automações: ',auts)
        print('Comandos: ',cmds)

class Application(Funcs):
    def __init__(self):
        self.commands = []
        self.new_aut_id = 0
        self.root = root
        self.screen()
        self.screen_frames()
        self.widgets_frame_1()
        self.widgets_frame_2()
        self.create_tables()
        self.update_list()
        self.temp_check_tables()
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
        self.btn_add_aut = Button(self.frame_1, text='Criar nova automação', command=self.show_add_aut_confirmation, bd=2, bg='#00A86B', fg='white')
        self.btn_add_aut.place(relx=0, rely=0.5, relwidth=0.23, relheight=0.30)
    def show_add_aut_confirmation(self):
        self.confirmation_msg = Label(self.frame_1, text='Para criar uma nova automação clique em começar', bg='#edeff2')
        self.confirmation_msg.place(relx=0.4, rely=0, relwidth=0.4, relheight=0.1)
        self.cancel_btn = Button(self.frame_1, text='Cancelar', command=self.clean_add_aut, bd=2, bg='#c93045', fg='white')
        self.cancel_btn.place(relx=0.4, rely=0.5, relwidth=0.23, relheight=0.30)
        self.add_aut_btn = Button(self.frame_1, text='Iniciar', command=self.init_msg, bd=2, bg='#00A86B', fg='white')
        self.add_aut_btn.place(relx=0.7, rely=0.5, relwidth=0.23, relheight=0.30)
    def clean_add_aut(self):
        self.confirmation_msg.destroy()
        self.cancel_btn.destroy()
        self.add_aut_btn.destroy()
    def init_msg(self):
        self.clean_add_aut()
        self.countdown_msg = Label(self.frame_1, text='Aguarde janelas minimizarem para começar', bg='#edeff2')
        self.countdown_msg.place(relx=0.4, rely=0.3, relwidth=0.4, relheight=0.1)
        self.add_automation()
    def widgets_frame_2(self):
        self.aut_list = ttk.Treeview(self.frame_2, height=3, column=('col1'))
        self.aut_list.heading('#0', text='')
        self.aut_list.heading('#1', text='nome')

        self.aut_list.column('#0', width=1)
        self.aut_list.column('#1', width=500)

        self.aut_list.place(relx=0, rely=0, relwidth=0.97, relheight=1)

        self.scroll = Scrollbar(self.frame_2, orient='vertical')
        self.aut_list.configure(yscroll=self.scroll)
        self.scroll.place(relx=0.97, rely=0, relwidth=0.02, relheight=1)


Application()
