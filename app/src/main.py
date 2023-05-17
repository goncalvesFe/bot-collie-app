import sqlite3
from tkinter import *
from tkinter import ttk

import pyautogui
from pynput import keyboard, mouse

pyautogui.PAUSE = 1
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
        self.cursor.execute("CREATE TABLE IF NOT EXISTS comando (id integer PRIMARY KEY, automacao_id int, command text, cmdOrder int)")
        self.conn.commit()
        self.disconnect_database()
    def delete_automation(self):
        self.connect_database()
        self.cursor.execute(f"DELETE FROM automacao WHERE id='{self.aut_id_selected}'")
        self.cursor.execute(f"DELETE FROM comando WHERE automacao_id='{self.aut_id_selected}'")
        self.conn.commit()
        self.disconnect_database()
        self.update_tree()
    def update_cmd_order(self):
        self.connect_database()
        ids = self.cursor.execute(f"SELECT id FROM comando WHERE automacao_id='{self.aut_id_selected}' AND cmdOrder > '{self.cmd_order_selected}' ORDER BY cmdOrder ASC").fetchall()
        order_to_update = self.cmd_order_selected
        for id in ids:
            self.cursor.execute(f"UPDATE comando SET cmdOrder = '{order_to_update}' WHERE id = '{id[0]}'")
            order_to_update = order_to_update + 1
        self.conn.commit()
        self.disconnect_database()
    def delete_command(self):
        self.update_cmd_order()
        self.connect_database()
        self.cursor.execute(f"DELETE FROM comando WHERE id='{self.cmd_id_selected}'")
        self.conn.commit()
        self.disconnect_database()
        self.update_edit_tree()
    def save_commands(self):
        self.connect_database
        cmd_counter = 1
        for command in self.commands:
            if hasattr(command, 'char'):
                insert_query = f"INSERT INTO comando (automacao_id, command, cmdOrder) VALUES ({self.new_aut_id}, {command}, {cmd_counter})"
                self.cursor.execute(insert_query)
            else:
                cmd = f"'{command}'"
                insert_query = f"INSERT INTO comando (automacao_id, command, cmdOrder) VALUES ({self.new_aut_id}, {cmd}, {cmd_counter})"
                self.cursor.execute(insert_query)
            cmd_counter = cmd_counter + 1
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
        self.update_tree()
    def update_tree(self):
        self.tree_aut.delete(*self.tree_aut.get_children())
        self.connect_database()
        list = self.cursor.execute('SELECT id, name FROM  automacao')
        for i in list:
            self.tree_aut.insert("", END, values=i)
        self.disconnect_database()
    def update_edit_tree(self):
        self.tree_command.delete(*self.tree_command.get_children())
        self.connect_database()
        list = self.cursor.execute(f"SELECT id, cmdOrder, command FROM comando WHERE automacao_id = '{self.aut_id_selected}' ORDER BY cmdOrder ASC")
        for i in list:
            self.tree_command.insert("", END, values=i)
        self.disconnect_database()
    def init_listeners(self):
        pyautogui.hotkey('win', 'd')
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
                # Stop listeners
                self.mouse_listener.stop()
                return False
        def on_move(x, y):
            # print('Pointer moved to {0}'.format((x, y)))
            pass
        def on_click(x, y, button, pressed):
            if pressed:
                mouse_click = f'click -  x: {x}, y: {y}, button: {button}'
                print(mouse_click)
                self.commands.append(mouse_click)
        def on_scroll(x, y, dx, dy):
            mouse_scroll = f'scroll - x: {x}, y: {y}, dx: {dx}, dy: {dy}'
            print(mouse_scroll)
            print('Scrolled {0} at {1}'.format('down' if dy < 0 else 'up', (x, y)))
            self.commands.append(mouse_scroll)
        self.keyboard_listener = keyboard.Listener(on_press=on_press, on_release=on_release)
        self.keyboard_listener.start()
        self.mouse_listener = mouse.Listener(on_move=on_move, on_click=on_click, on_scroll=on_scroll)
        self.mouse_listener.start()
    def run_automation(self):
        self.connect_database()
        aut_id = self.cursor.execute(f"SELECT id FROM automacao WHERE name='{self.aut_name_selected}'").fetchone()[0]
        commands = self.cursor.execute(f"SELECT * FROM comando WHERE automacao_id='{aut_id}'").fetchall()
        pyautogui.hotkey('win', 'd')
        for command in commands:
            cmd = command[2]
            if len(cmd.split('.')) == 1:
                print('tecla normal')
                print(cmd)
                pyautogui.press(cmd)
            else:
                print('tecla especial')
                special_cmd = cmd.split('.')[1]
                if special_cmd == 'cmd':
                    special_cmd = 'win'
                print(special_cmd)
                pyautogui.press(special_cmd)
        self.disconnect_database()
    def temp_check_tables(self):
        self.connect_database()
        las_aut_id = self.cursor.execute('SELECT MAX(id) FROM automacao').fetchone()[0]
        comandos = self.cursor.execute(f'SELECT command, cmdOrder FROM comando WHERE automacao_id = {las_aut_id}').fetchall()
        print('comandos: ',comandos)
        self.disconnect_database()

class Application(Funcs):
    def __init__(self):
        # self.temp_check_tables()
        self.commands = []
        self.new_aut_id = 0
        self.root = root
        self.screen()
        self.screen_frames()
        self.widgets_frame_1()
        self.widgets_frame_2()
        self.create_tables()
        self.update_tree()
        root.mainloop()
    def screen(self):
        self.root.title('Bot Collie')
        self.root.configure(background='#babdc2')
        self.root.geometry("900x700")
        self.root.resizable(True, True)
        self.root.maxsize(width=1100, height=900)
        self.root.minsize(width=400, height=300)
    def edit_screen(self):
        self.root_edit = Toplevel()
        self.root_edit.configure(background='#babdc2')
        self.root_edit.geometry("900x700")
        self.root_edit.resizable(True, True)
        self.root_edit.maxsize(width=1100, height=900)
        self.root_edit.minsize(width=400, height=300)
        self.edit_frame = Frame(self.root_edit, bd=4, bg='#edeff2', highlightbackground='white', highlightthickness=3)
        self.edit_frame.place(relx=0.02, rely=0.02, relwidth=0.96, relheight=0.96)
        self.edit_widget_frame()
        self.update_edit_tree()
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
        self.init_listeners()
    def widgets_frame_2(self):
        self.tree_aut = ttk.Treeview(self.frame_2, height=3, column=('col1', 'col2'), show='headings')
        self.tree_aut.heading('#0', text='')
        self.tree_aut.heading('#1', text='ID')
        self.tree_aut.heading('#2', text='Automações')
        self.tree_aut.column('#0', width=1)
        self.tree_aut.column('#1', width=50)
        self.tree_aut.column('#2', width=450)
        self.tree_aut.place(relx=0, rely=0, relwidth=0.57, relheight=1)

        self.aut_id_selected = 0
        self.aut_name_selected = ''
        def get_item_selected(event):
            for seleted_item in self.tree_aut.selection():
                item = self.tree_aut.item(seleted_item)
                self.aut_id_selected = item['values'][0]
                self.aut_name_selected = item['values'][1]
                self.auto_selected.config(text=self.aut_name_selected)
        self.tree_aut.bind('<<TreeviewSelect>>', get_item_selected)

        self.scroll = Scrollbar(self.frame_2, orient='vertical')
        self.tree_aut.configure(yscroll=self.scroll)
        self.scroll.place(relx=0.57, rely=0, relwidth=0.02, relheight=1)

        self.auto_selected = Label(self.frame_2, text='Selecione a automação', bg='#dae1eb', font=('Arial', 15))
        self.auto_selected.place(relx=0.62, rely=0.03, relwidth=0.36, relheight=0.09)

        self.btn_run_aut = Button(self.frame_2, text='Rodar automação', command=self.run_automation, bd=2, bg='#00A86B', fg='white')
        self.btn_run_aut.place(relx=0.62, rely=0.25, relwidth=0.36, relheight=0.09)

        self.btn_edit_aut = Button(self.frame_2, text='Editar automação', command=self.edit_screen, bd=2, bg='#5a4aed', fg='white')
        self.btn_edit_aut.place(relx=0.62, rely=0.45, relwidth=0.36, relheight=0.09)

        self.btn_del_aut = Button(self.frame_2, text='Excluir automação', command=self.delete_automation, bd=2, bg='#c93045', fg='white')
        self.btn_del_aut.place(relx=0.62, rely=0.55, relwidth=0.36, relheight=0.09)
    def edit_widget_frame(self):
        self.tree_command = ttk.Treeview(self.edit_frame, height=3, column=('col1', 'col2', 'col3'), show='headings')
        self.tree_command.heading('#0', text='')
        self.tree_command.heading('#1', text='ID')
        self.tree_command.heading('#2', text='Ordem')
        self.tree_command.heading('#3', text='Comando')
        self.tree_command.column('#0', width=1)
        self.tree_command.column('#1', width=50)
        self.tree_command.column('#2', width=200)
        self.tree_command.column('#3', width=250)
        self.tree_command.place(relx=0, rely=0, relwidth=0.57, relheight=1)

        self.command_selected = ''
        self.cmd_order_selected = 0
        self.cmd_id_selected = 0
        def get_cmd_selected(event):
            for cmd_item in self.tree_command.selection():
                item = self.tree_command.item(cmd_item)
                self.cmd_id_selected = item['values'][0]
                self.cmd_order_selected = item['values'][1]
                self.command_selected = item['values'][2]
                self.cmd_seleted.config(text=self.command_selected)
        self.tree_command.bind('<<TreeviewSelect>>', get_cmd_selected)

        self.ed_scroll = Scrollbar(self.edit_frame, orient='vertical')
        self.tree_command.configure(yscroll=self.scroll)
        self.ed_scroll.place(relx=0.57, rely=0, relwidth=0.02, relheight=1)

        self.add_above_lbl = Label(self.edit_frame, text='Adicionar comando acima', bg='#edeff2', font=('Arial', 13))
        self.add_above_lbl.place(relx=0.62, rely=0.03, relwidth=0.36, relheight=0.09)
        self.add_above_btn = Button(self.edit_frame, text='+', bd=2, bg='#dae1eb')
        self.add_above_btn.place(relx=0.62, rely=0.1, relwidth=0.36, relheight=0.05)

        self.cmd_seleted = Label(self.edit_frame, text='Selecione o comando', bg='#dae1eb', font=('Arial', 15))
        self.cmd_seleted.place(relx=0.62, rely=0.3, relwidth=0.36, relheight=0.09)
        self.btn_edt_cmd = Button(self.edit_frame, text='Editar comando', command=self.edit_command_widgets, bd=2, bg='#5a4aed', fg='white')
        self.btn_edt_cmd.place(relx=0.62, rely=0.40, relwidth=0.36, relheight=0.07)
        self.btn_del_cmd = Button(self.edit_frame, text='Excluir comando', command=self.delete_command, bd=2, bg='#c93045', fg='white')
        self.btn_del_cmd.place(relx=0.62, rely=0.50, relwidth=0.36, relheight=0.06)

        self.add_below_lbl = Label(self.edit_frame, text='Adicionar comando abaixo', bg='#edeff2', font=('Arial', 13))
        self.add_below_lbl.place(relx=0.62, rely=0.8, relwidth=0.36, relheight=0.09)
        self.add_below_btn = Button(self.edit_frame, text='+', bd=2, bg='#dae1eb')
        self.add_below_btn.place(relx=0.62, rely=0.77, relwidth=0.36, relheight=0.05)
    def show_keyboard_opt(self):
        pass
    def show_mouse_opt(self):
        pass
    def edit_command_widgets(self):
        self.tree_command.destroy()
        self.ed_scroll.destroy()
        self.add_above_lbl.destroy()
        self.add_above_btn.destroy()
        self.cmd_seleted.destroy()
        self.btn_edt_cmd.destroy()
        self.btn_del_cmd.destroy()
        self.add_below_lbl.destroy()
        self.add_below_btn.destroy()

        self.btn_keyboard_opt = Button(self.edit_frame, text='Comandos teclado', bd=2, bg='#dae1eb')
        self.btn_keyboard_opt.place(relx=0.05, rely=0.02, relwidth=0.4, relheight=0.07)
        self.btn_mouse_opt = Button(self.edit_frame, text='Comandos mouse', bd=2, bg='#dae1eb')
        self.btn_mouse_opt.place(relx=0.55, rely=0.02, relwidth=0.4, relheight=0.07)


Application()
