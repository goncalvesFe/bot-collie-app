import sqlite3
import time
from tkinter import *
from tkinter import ttk, messagebox
import sys
import os
import pyautogui
from pynput import keyboard, mouse
from PIL import ImageTk, Image

special_opts = [
    'accept', 'add', 'alt', 'altleft', 'altright', 'apps', 'backspace','browserback', 'browserfavorites', 'browserforward', 
    'browserhome','browserrefresh', 'browsersearch', 'browserstop', 'capslock', 'clear','convert', 'ctrl', 'ctrlleft', 
    'ctrlright', 'decimal', 'del', 'delete','divide', 'down', 'end', 'enter', 'esc', 'escape', 'execute',
    'f1', 'f2','f3', 'f4', 'f5', 'f6', 'f7', 'f8', 'f9','f10','f11', 'f12', 'f13', 'f14', 'f15', 'f16', 'f17', 'f18', 'f19', 'f20', 'f21', 'f22', 'f23', 'f24', 
    'final', 'fn', 'hanguel', 'hangul', 'hanja', 'help', 'home', 'insert', 'junja','kana', 'kanji', 
    'launchapp1', 'launchapp2', 'launchmail','launchmediaselect', 'left', 'modechange', 'multiply', 'nexttrack','nonconvert', 
    'num0', 'num1', 'num2', 'num3', 'num4', 'num5', 'num6','num7', 'num8', 'num9', 'numlock', 'pagedown', 'pageup', 'pause', 
    'pgdn','pgup', 'playpause', 'prevtrack', 'print', 'printscreen', 'prntscrn','prtsc', 'prtscr', 'return', 'right', 'scrolllock', 
    'select', 'separator','shift', 'shiftleft', 'shiftright', 'sleep', 'space', 'stop', 'subtract', 'tab','up', 'volumedown', 
    'volumemute', 'volumeup', 'win', 'winleft', 'winright', 'yen','command', 'option', 'optionleft', 'optionright'
]

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS2
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

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
        self.cursor.execute("CREATE TABLE IF NOT EXISTS comando (id integer PRIMARY KEY, automacao_id int, type text, subtype text, command text, cmdOrder int)")
        self.conn.commit()
        self.disconnect_database()
    def delete_automation(self):
        self.connect_database()
        self.cursor.execute(f"DELETE FROM automacao WHERE id='{self.aut_id_selected}'")
        self.conn.commit()
        self.disconnect_database()
        self.delete_aut_command()
        self.update_tree()
        self.clean_del_confirm()
    def delete_aut_command(self):
        self.connect_database()
        self.cursor.execute(f"DELETE FROM comando WHERE automacao_id='{self.aut_id_selected}'")
        self.conn.commit()
        self.disconnect_database()
    def update_cmd_order(self):
        self.connect_database()
        ids = self.cursor.execute(f"SELECT id FROM comando WHERE automacao_id='{self.aut_id_selected}' AND cmdOrder > '{self.cmd_order_selected}' ORDER BY cmdOrder ASC").fetchall()
        order_to_update = self.cmd_order_selected
        for id in ids:
            self.cursor.execute(f"UPDATE comando SET cmdOrder = '{order_to_update}' WHERE id = '{id[0]}'")
            order_to_update = order_to_update + 1
        self.conn.commit()
        self.disconnect_database()
    def update_all_cmd_order(self):
        self.connect_database()
        select_query = f"SELECT id FROM comando WHERE automacao_id='{self.aut_id_selected}' ORDER BY cmdOrder ASC"
        if self.add_cmd_dir == 'below':
            select_query = f"{select_query}, id DESC"
        ids = self.cursor.execute(select_query).fetchall()
        order_to_update = 1
        for id in ids:
            self.cursor.execute(f"UPDATE comando SET cmdOrder = '{order_to_update}' WHERE id = '{id[0]}'")
            order_to_update = order_to_update + 1
        self.conn.commit()
        self.disconnect_database()
    def delete_command(self):
        self.update_cmd_order()
        self.connect_database()
        for cmd_value in self.cmd_all_values_selected:
            cmd_id = cmd_value[0]
            self.cursor.execute(f"DELETE FROM comando WHERE id='{cmd_id}'")
        self.conn.commit()
        self.disconnect_database()
        self.update_edit_tree()
        self.cmd_seleted.config(text='')
        self.reset_confirm_cmd_del()
    def save_commands(self):
        self.connect_database
        cmd_counter = 1
        for command in self.commands:
            type = f"'{command[0]}'"
            subtype = f"'{command[1]}'"
            the_command = command[2]
            if hasattr(the_command, 'char'):
                insert_query = f"INSERT INTO comando (automacao_id, type, subtype, command, cmdOrder) VALUES ({self.new_aut_id}, {type}, {subtype}, {the_command}, {cmd_counter})"
                self.cursor.execute(insert_query)
            else:
                cmd = f"'{the_command}'"
                insert_query = f"INSERT INTO comando (automacao_id, type, subtype, command, cmdOrder) VALUES ({self.new_aut_id}, {type}, {subtype}, {cmd}, {cmd_counter})"
                self.cursor.execute(insert_query)
            cmd_counter = cmd_counter + 1
        self.conn.commit()
        self.disconnect_database()
    def save_automation(self):
        aut_id = 1
        self.connect_database()
        las_aut_id = self.cursor.execute('SELECT MAX(id) FROM automacao').fetchone()[0]
        if las_aut_id != None: aut_id = aut_id + las_aut_id
        aut_name = f'automacao-{aut_id}'
        self.cursor.execute(f"INSERT INTO automacao (name) VALUES ('{aut_name}')")
        self.conn.commit()
        self.new_aut_id = aut_id
        self.save_commands()
        self.disconnect_database()
        self.update_tree()
    def edit_automation_name(self):
        new_aut_name = self.aut_name_edt_name.get()
        if len(new_aut_name) == 0: messagebox.showerror(title='Erro', message='Nome inválido')
        else:
            self.connect_database()
            self.cursor.execute(f"UPDATE automacao SET name = '{new_aut_name}' WHERE id = '{self.aut_id_selected}'")
            self.conn.commit()
            self.disconnect_database()
            self.update_tree()
            self.clean_edit_aut_name()
    def update_tree(self):
        self.tree_aut.delete(*self.tree_aut.get_children())
        self.connect_database()
        list = self.cursor.execute('SELECT id, name FROM  automacao')
        rowcount = 0
        for i in list:
            if rowcount % 2 == 0:
                self.tree_aut.insert("", END, values=i, tags=('oddrow',))
            else:
                self.tree_aut.insert("", END, values=i, tags=('evenrow',))
            rowcount += 1
        self.disconnect_database()
    def update_edit_tree(self):
        self.tree_command.delete(*self.tree_command.get_children())
        self.connect_database()
        list = self.cursor.execute(f"SELECT id, cmdOrder, subtype, command FROM comando WHERE automacao_id = '{self.aut_id_selected}' ORDER BY cmdOrder ASC")
        rowcount = 0
        for i in list:
            if rowcount % 2 == 0: 
                self.tree_command.insert("", END, values=i, tags=('oddrow',))
            else:
                self.tree_command.insert("", END, values=i, tags=('evenrow',))
            rowcount += 1
        self.disconnect_database()
    def init_listeners(self):
        # estrutura dos comandos adicionados sempre será:
        # commands = [['type', 'subtype', 'cmd'], ['type', 'subtype', 'cmd'], ...]
        pyautogui.hotkey('win', 'd')
        def on_press(key):
            if key != keyboard.Key.esc:
                self.commands.append(['keyboard', 'Pressionar', key])
            # try:
            #     print('alphanumeric key {0} pressed'.format(key.char))
            # except AttributeError:
            #     print('special key {0} pressed'.format(key))
        def on_release(key):
            if key == keyboard.Key.esc:
                self.save_automation()
                # Stop listeners
                self.mouse_listener.stop()
                self.switch_btn_state = 'normal'
                self.switch_all_screen_buttons_state()
                return False
        def on_move(x, y):
            # print('Pointer moved to {0}'.format((x, y)))
            pass
        def on_click(x, y, button, pressed):
            btn = 'Esquerdo' if button.name == 'left' else 'Direito'
            if pressed:
                # command: ‘x,y,button,num’ 
                mouse_click = f'{x},{y},{btn},1'
                # print(mouse_click)
                self.commands.append(['mouse', 'click', mouse_click])
        def on_scroll(x, y, dx, dy):
            if dx == 0:
                hscroll = dx
            elif dx == -1:
                hscroll = 'para direita'
            elif dx == 1:
                hscroll = 'para esquerda'
            if dy == 0:
                vscroll = dy
            elif dy == -1:
                vscroll = 'para baixo'
            elif dy == 1:
                vscroll = 'para cima'
            # command: ‘x,y,dx,dy’
            mouse_scroll = f'{x},{y},{hscroll},{vscroll}'
            # print(mouse_scroll)
            self.commands.append(['mouse', 'scroll', mouse_scroll])
        self.keyboard_listener = keyboard.Listener(on_press=on_press, on_release=on_release)
        self.keyboard_listener.start()
        self.mouse_listener = mouse.Listener(on_move=on_move, on_click=on_click, on_scroll=on_scroll)
        self.mouse_listener.start()
    def run_automation(self):
        def check_cmd(command):
            cmd = command.split('.')
            if len(cmd) == 1:
                return command
            else:
                special_command = cmd[1]
                if special_command == 'cmd':
                    special_command = 'win'
                return special_command
        if self.aut_name_selected == '':
            self.error_txt = 'Nenhuma automação selecionada'
            self.error_modal_screen()
        else:
            self.connect_database()
            aut_id = self.cursor.execute(f"SELECT id FROM automacao WHERE name='{self.aut_name_selected}'").fetchone()[0]
            commands = self.cursor.execute(f"SELECT * FROM comando WHERE automacao_id='{aut_id}' ORDER BY cmdOrder ASC").fetchall()
            pyautogui.hotkey('win', 'd')
            for command in commands:
                type = command[2]
                subtype = command[3]
                cmd = command[4]
                if type == 'keyboard':
                    if subtype == 'Pressionar':
                        pyautogui.press(check_cmd(cmd))
                    elif subtype == 'Escrever':
                        pyautogui.write(cmd)
                    elif subtype == 'Segurar':
                        pyautogui.keyDown(check_cmd(cmd))
                    elif subtype == 'Soltar':
                        pyautogui.keyUp(check_cmd(cmd))
                elif type == 'mouse':
                    cmd_str_split = cmd.split(',')
                    x_pos = int(cmd_str_split[0])
                    y_pos = int(cmd_str_split[1])
                    if subtype == 'click':
                        btn_click = 'left' if cmd_str_split[2] == 'Esquerdo' else 'right'
                        click_number = int(cmd_str_split[3])
                        pyautogui.click(x=x_pos, y=y_pos, button=btn_click, clicks=click_number)
                    else:
                        dx = cmd_str_split[2]
                        dy = cmd_str_split[3]
                        if dx == '0': pyautogui.scroll(10 if dy == 'para cima' else -10, x=x_pos, y=y_pos)
                        else: pyautogui.hscroll(10 if dx == 'para direita' else -10, x=x_pos, y=y_pos)
                else: time.sleep(int(cmd))
            self.disconnect_database()
    def save_special_char_cmd(self):
        if self.special_selected == '':
            messagebox.showerror(title='Erro', message='Nenhuma seleção')
        else:
            self.new_cmd = f'Key.{self.special_selected}'
            self.insert_new_cmd()
    def save_keyboard_cmd(self):
        input_len = len(self.edit_input.get())
        if input_len == 0:
            messagebox.showerror(title='Erro', message='Entrada vazia')
        elif input_len > self.entry_limit:
            messagebox.showwarning(title='Atenção!', message='Número de characters é maior que o permitido.')
        else:
            self.new_cmd = self.edit_input.get()
            if self.edit_cmd: self.update_cmd() 
            else: self.insert_new_cmd()
    def update_cmd(self):
        self.connect_database()
        self.cursor.execute(f"UPDATE comando SET command = '{self.new_cmd}' WHERE id = '{self.cmd_id_selected}'")
        self.conn.commit()
        self.disconnect_database()
        self.edit_cmd = False
        self.reload_cmd_wiget()
    def calculate_command_order(self):
        self.cmdOrder = 0
        if self.add_cmd_dir == 'above':
            self.cmdOrder = self.cmd_order_selected - 1
        else:
            self.cmdOrder = self.cmd_order_selected + 1
    def insert_new_cmd(self):
        self.calculate_command_order()
        self.connect_database()
        insert_query = f"INSERT INTO comando (automacao_id, type, subtype, command, cmdOrder) VALUES ({self.aut_id_selected}, 'keyboard', '{self.subtype_cmd}', '{self.new_cmd}', {self.cmdOrder})"
        self.cursor.execute(insert_query)
        self.conn.commit()
        self.disconnect_database()
        self.update_all_cmd_order()
        self.reload_cmd_wiget()
    def reload_cmd_wiget(self):
        self.root_add_cmd.destroy()
        self.command_selected = ''
        self.cmd_seleted.config(text=self.command_selected)
        self.update_edit_tree()
    def save_new_mouse_click(self):
        self.subtype_mouse_cmd = 'click'
        self.save_new_mouse_command()
    def save_new_mouse_scroll(self):
        self.subtype_mouse_cmd = 'scroll'
        self.save_new_mouse_command()
    def save_new_mouse_command(self):
        if len(self.xpos.get()) == 0 or len(self.ypos.get()) == 0:
            messagebox.showerror(title='Erro', message='Campo posição do mouse vazio')
        else:
            if self.edit_cmd:
                self.build_mouse_command()
                self.new_cmd = self.mouse_cmd
                self.update_cmd()
            else:
                self.insert_new_mouse_cmd()
    def build_mouse_command(self):
        mouse_pos = f'{self.xpos.get()},{self.ypos.get()},'
        self.mouse_cmd = ''
        if self.subtype_mouse_cmd == 'click':
            num_click = 1 if self.num_clicked.get() == 'Simples' else 2
            self.mouse_cmd = mouse_pos + f'{self.choices_clicked.get()},{num_click}'
        if self.subtype_mouse_cmd == 'scroll':
            self.mouse_cmd = mouse_pos + f'0,{self.scroll_clicked.get()}' if self.scroll_sense == 'vertical' else mouse_pos + f'{self.scroll_clicked.get()},0'
    def insert_new_mouse_cmd(self):
        self.calculate_command_order()
        self.build_mouse_command()
        self.connect_database()
        insert_query = f"INSERT INTO comando (automacao_id, type, subtype, command, cmdOrder) VALUES ({self.aut_id_selected}, 'mouse', 'click', '{self.mouse_cmd}', {self.cmdOrder})"
        self.cursor.execute(insert_query)
        self.conn.commit()
        self.disconnect_database()
        self.update_all_cmd_order()
        self.reload_cmd_wiget()
    def save_wait_command(self):
        self.wait_in_sec = self.entry_add_cmd_wait.get()
        if len(self.wait_in_sec) == 0:
            messagebox.showerror(title='Erro', message='Não é possível adicionar um tempo vazio')
        else:
            if self.edit_cmd: self.update_waiting_time()
            else: self.insert_waiting_time()
    def insert_waiting_time(self):
        self.calculate_command_order()
        self.connect_database()
        insert_query = f"INSERT INTO comando (automacao_id, type, subtype, command, cmdOrder) VALUES ({self.aut_id_selected}, 'wait', 'aguardar', '{self.wait_in_sec}', {self.cmdOrder})"
        self.cursor.execute(insert_query)
        self.conn.commit()
        self.disconnect_database()
        self.update_all_cmd_order()
        self.reload_cmd_wiget()
    def update_waiting_time(self):
        self.connect_database()
        self.cursor.execute(f"UPDATE comando SET command = '{self.wait_in_sec}' WHERE id = '{self.cmd_id_selected}'")
        self.conn.commit()
        self.disconnect_database()
        self.edit_cmd = False
        self.reload_cmd_wiget()
    def temp_check_tables(self):
        self.connect_database()
        las_aut_id = self.cursor.execute('SELECT MAX(id) FROM automacao').fetchone()[0]
        comandos = self.cursor.execute(f'SELECT type, subtype, command, cmdOrder FROM comando WHERE automacao_id = {las_aut_id}').fetchall()
        print('comandos: ',comandos)
        self.disconnect_database()

class Application(Funcs):
    def __init__(self):
        self.config_constants()
        # self.temp_check_tables()
        self.error_txt = 'Ocorreu um erro'
        self.confirm_cmd_del = False
        self.commands = []
        self.switch_btn_state = ''
        self.new_aut_id = 0
        self.root = root
        self.screen()
        self.screen_frames()
        self.widgets_frame_1()
        self.widgets_frame_2()
        self.create_tables()
        self.update_tree()
        root.mainloop()
    def config_constants(self):
        self.app_version = '1.0'
        self.title = f'Bot Collie - v_{self.app_version}'
        #trout #4c5760
        #cornflower #89ace3
        #linkwater #e1eff6
        #casablanca #f3b94d
        #shark #25282a
        self.root_bg_color = '#4c5760'
        self.frame_bg_color = '#e1eff6'
        self.edit_btn_color = '#89ace3'
    def screen(self):
        self.root.title(self.title)
        self.root.configure(background=self.root_bg_color)
        self.root.geometry("800x700")
        self.root.resizable(True, True)
        self.root.maxsize(width=1100, height=900)
        self.root.minsize(width=400, height=300)
    def edit_screen(self):
        if self.aut_name_selected == '':
            self.error_txt = 'Nenhuma automação selecionada'
            self.error_modal_screen()
        else:
            self.root_edit = Toplevel()
            self.root_edit.configure(background=self.root_bg_color)
            self.root_edit.geometry("900x700")
            self.root_edit.resizable(True, True)
            self.root_edit.maxsize(width=1100, height=900)
            self.root_edit.minsize(width=400, height=300)
            self.edit_frame = Frame(self.root_edit, bd=4, bg=self.frame_bg_color, highlightbackground='white', highlightthickness=3)
            self.edit_frame.place(relx=0.02, rely=0.02, relwidth=0.96, relheight=0.96)
            self.edit_widget_frame()
            self.update_edit_tree()
    def error_modal_screen(self):
        self.root_error_modal = Toplevel()
        self.root_error_modal.configure(background=self.root_bg_color)
        self.root_error_modal.geometry("450x350")
        self.root_error_modal.resizable(True, True)
        self.root_error_modal.maxsize(width=900, height=450)
        self.root_error_modal.minsize(width=100, height=100)
        self.error_modal_frame = Frame(self.root_error_modal, bd=4, bg=self.frame_bg_color, highlightbackground='white', highlightthickness=3)
        self.error_modal_frame.place(relx=0.02, rely=0.02, relwidth=0.96, relheight=0.96)
        if self.confirm_cmd_del:
            self.widget_confirm_cmd_del()
        else:
            self.widget_error_modal()
    def widget_confirm_cmd_del(self):
        text_msg = f'Deseja excluir {"os comandos" if self.cmd_multiple_selections else "o comando"}?'
        self.del_cmd_msg = Label(self.error_modal_frame, text=text_msg, bg=self.frame_bg_color, font=('Arial', 14))
        self.del_cmd_msg.place(relx=0, rely=0.1, relwidth=1, relheight=0.3)
        self.Ndel_cmd_confirm_btn = Button(self.error_modal_frame, text='Cancelar', command=self.reset_confirm_cmd_del, bd=2, bg='#00A86B', fg='white')
        self.Ndel_cmd_confirm_btn.place(relx= 0.15, rely=0.5, relwidth=0.3, relheight=0.15)
        self.del_cmd_confirm_btn = Button(self.error_modal_frame, text='Excluir', command=self.delete_command, bd=2, bg='#c93045', fg='white')
        self.del_cmd_confirm_btn.place(relx= 0.55, rely=0.5, relwidth=0.3, relheight=0.15)
    def widget_error_modal(self):
        self.error_msg = Label(self.error_modal_frame, text=self.error_txt, bg=self.frame_bg_color, font=('Arial', 14))
        self.error_msg.place(relx=0, rely=0.1, relwidth=1, relheight=0.3)
        self.confirm_btn = Button(self.error_modal_frame, text='Ok', command=self.root_error_modal.destroy, bd=2, bg=self.root_bg_color, fg='white')
        self.confirm_btn.place(relx= 0.1, rely=0.5, relwidth=0.8, relheight=0.15)
    def screen_frames(self):
        self.frame_1 = Frame(self.root, bd=4, bg=self.frame_bg_color, highlightbackground='white', highlightthickness=3)
        self.frame_1.place(relx=0.02, rely=0.02, relwidth=0.96, relheight=0.25)
        self.frame_2 = Frame(self.root, bd=4, bg=self.frame_bg_color, highlightbackground='white', highlightthickness=3)
        self.frame_2.place(relx=0.02, rely=0.3, relwidth=0.96, relheight=0.68)
    def widgets_frame_1(self):
        # tamanho da imagem original: 360X360
        logo = Image.open('logo-trout.png')
        resized = logo.resize((160,160))
        #self.logo_img = PhotoImage(file=resource_path('logo-link-water.png'))
        self.logo_img = ImageTk.PhotoImage(resized)
        self.logo = Label(self.frame_1, image=self.logo_img, bg=self.frame_bg_color)
        self.logo.place(relx=0, rely=0)
        self.btn_add_aut = Button(self.frame_1, text='Criar nova automação', command=self.show_add_aut_confirmation, bd=2, bg='#00A86B', fg='white')
        self.btn_add_aut.place(relx=0.62, rely=0.5, relwidth=0.36, relheight=0.30)
    def show_add_aut_confirmation(self):
        self.btn_add_aut.destroy()
        self.confirmation_msg = Label(self.frame_1, text='Para criar uma nova automação clique em Iniciar', bg=self.frame_bg_color, font=('Arial', 13))
        self.confirmation_msg.place(relx=0.2, rely=0.1, relwidth=0.6, relheight=0.1)
        self.cancel_btn = Button(self.frame_1, text='Cancelar', command=self.clean_add_aut, bd=2, bg='#c93045', fg='white')
        self.cancel_btn.place(relx=0.25, rely=0.5, relwidth=0.23, relheight=0.30)
        self.add_aut_btn = Button(self.frame_1, text='Iniciar', command=self.init_aut, bd=2, bg='#00A86B', fg='white')
        self.add_aut_btn.place(relx=0.55, rely=0.5, relwidth=0.23, relheight=0.30)
    def clean_add_aut(self):
        self.confirmation_msg.destroy()
        self.cancel_btn.destroy()
        self.add_aut_btn.destroy()
        self.widgets_frame_1()
    def init_aut(self):
        self.clean_add_aut()
        self.switch_btn_state = 'disabled'
        self.switch_all_screen_buttons_state()
        self.init_listeners()
    def widgets_frame_2(self):
        self.tree_aut = ttk.Treeview(self.frame_2, height=3, column=('col1', 'col2'), show='headings')
        self.tree_aut.tag_configure('oddrow', background='white')
        self.tree_aut.tag_configure('evenrow', background=self.frame_bg_color)
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

        self.scroll = Scrollbar(self.frame_2, orient='vertical', troughcolor=self.frame_bg_color, bd=2)
        self.tree_aut.configure(yscroll=self.scroll.set)
        self.scroll.place(relx=0.57, rely=0, relwidth=0.02, relheight=1)

        self.auto_selected = Label(self.frame_2, text='Selecione a automação', bg=self.edit_btn_color, font=('Arial', 15))
        self.auto_selected.place(relx=0.62, rely=0.03, relwidth=0.36, relheight=0.09)

        self.btn_edit_nome_aut = Button(self.frame_2, text='Alterar nome da automação', command=self.show_edit_aut_name, bd=2, bg=self.edit_btn_color)
        self.btn_edit_nome_aut.place(relx=0.62, rely=0.13, relwidth=0.36, relheight=0.07)

        self.btn_run_aut = Button(self.frame_2, text='Rodar automação', command=self.run_automation, bd=2, bg='#00A86B', fg='white')
        self.btn_run_aut.place(relx=0.62, rely=0.25, relwidth=0.36, relheight=0.09)

        self.btn_edit_aut = Button(self.frame_2, text='Editar automação', command=self.edit_screen, bd=2, bg='#5a4aed', fg='white')
        self.btn_edit_aut.place(relx=0.62, rely=0.45, relwidth=0.36, relheight=0.09)

        self.btn_del_aut = Button(self.frame_2, text='Excluir automação', command=self.delete_aut_confirmation, bd=2, bg='#c93045', fg='white')
        self.btn_del_aut.place(relx=0.62, rely=0.55, relwidth=0.36, relheight=0.09)
    def edit_widget_frame(self):
        self.tree_command = ttk.Treeview(self.edit_frame, height=3, column=('col1', 'col2', 'col3', 'col4'), show='headings')
        self.tree_command.tag_configure('oddrow', background='white')
        self.tree_command.tag_configure('evenrow', background=self.frame_bg_color)
        self.tree_command.heading('#0', text='')
        self.tree_command.heading('#1', text='ID')
        self.tree_command.heading('#2', text='Ordem')
        self.tree_command.heading('#3', text='Tipo')
        self.tree_command.heading('#4', text='Comando')
        self.tree_command.column('#0', width=1)
        self.tree_command.column('#1', width=30)
        self.tree_command.column('#2', width=70)
        self.tree_command.column('#3', width=100)
        self.tree_command.column('#4', width=300)
        self.tree_command.place(relx=0, rely=0, relwidth=0.57, relheight=1)

        self.command_selected = []
        self.cmd_order_selected = 0
        self.cmd_id_selected = 0
        self.cmd_subtype = ''
        self.cmd_multiple_selections = False
        self.cmd_all_values_selected = []
        def build_text_cmd(cmds_selected):
            if len(cmds_selected) == 0:
                return ''
            if len(cmds_selected) == 1:
                return cmds_selected[0]
            response = ''
            for cmd_selected in cmds_selected:
                response = cmd_selected if response == '' else f'{response} | {cmd_selected}'

            return response
        def get_cmd_selected(event):
            self.command_selected = []
            self.cmd_all_values_selected = []
            for cmd_item in self.tree_command.selection():
                values = self.tree_command.item(cmd_item)['values']
                self.cmd_id_selected = values[0]
                self.cmd_order_selected = values[1]
                self.cmd_subtype = values[2]
                self.command_selected.append(values[3])
                self.cmd_all_values_selected.append(values)
            self.cmd_seleted.config(text=build_text_cmd(self.command_selected))
            self.cmd_multiple_selections = True if len(self.command_selected) > 1 else False
        self.tree_command.bind('<<TreeviewSelect>>', get_cmd_selected)

        self.ed_scroll = Scrollbar(self.edit_frame, orient='vertical', troughcolor=self.frame_bg_color, bd=2)
        self.tree_command.configure(yscroll=self.ed_scroll.set)
        self.ed_scroll.place(relx=0.57, rely=0, relwidth=0.02, relheight=1)

        self.add_above_lbl = Label(self.edit_frame, text='Adicionar comando acima', bg=self.frame_bg_color, font=('Arial', 13))
        self.add_above_lbl.place(relx=0.62, rely=0.03, relwidth=0.36, relheight=0.09)
        self.add_above_btn = Button(self.edit_frame, text='+', command=self.set_add_cmd_above, bd=2, bg=self.edit_btn_color)
        self.add_above_btn.place(relx=0.62, rely=0.1, relwidth=0.36, relheight=0.05)

        self.cmd_seleted = Label(self.edit_frame, text='Selecione o comando', bg=self.edit_btn_color, font=('Arial', 15))
        self.cmd_seleted.place(relx=0.62, rely=0.3, relwidth=0.36, relheight=0.09)
        self.btn_edt_cmd = Button(self.edit_frame, text='Editar comando', command=self.edit_command, bd=2, bg='#5a4aed', fg='white')
        self.btn_edt_cmd.place(relx=0.62, rely=0.40, relwidth=0.36, relheight=0.07)
        self.btn_del_cmd = Button(self.edit_frame, text='Excluir comando', command=self.confirm_del_cmd, bd=2, bg='#c93045', fg='white')
        self.btn_del_cmd.place(relx=0.62, rely=0.50, relwidth=0.36, relheight=0.06)

        self.add_below_lbl = Label(self.edit_frame, text='Adicionar comando abaixo', bg=self.frame_bg_color, font=('Arial', 13))
        self.add_below_lbl.place(relx=0.62, rely=0.8, relwidth=0.36, relheight=0.09)
        self.add_below_btn = Button(self.edit_frame, text='+', command=self.set_add_cmd_below, bd=2, bg=self.edit_btn_color)
        self.add_below_btn.place(relx=0.62, rely=0.77, relwidth=0.36, relheight=0.05)
    def confirm_del_cmd(self):
        if len(self.command_selected) == 0:
            self.error_txt = 'Nenhum comando selecionado'
        else:
            self.confirm_cmd_del = True
        self.error_modal_screen()
    def reset_confirm_cmd_del(self):
        self.confirm_cmd_del = False
        self.root_error_modal.destroy()
    def clean_del_confirm(self):
        self.aut_name_selected = ''
        self.auto_selected.config(text=self.aut_name_selected)
        self.update_tree()
        self.del_confirmation_msg.destroy()
        self.del_cancel_btn.destroy()
        self.del_confirm_btn.destroy()
        self.widgets_frame_1()
    def clean_edit_aut_name(self):
        self.aut_name_edt_name.destroy()
        self.edt_cancel_btn.destroy()
        self.edt_save_btn.destroy()
        self.widgets_frame_1()
    def show_edit_aut_name(self):
        if self.aut_name_selected == '':
            self.error_txt = 'Nenhuma automação selecionada'
            self.error_modal_screen()
        else:
            self.btn_add_aut.destroy()
            self.aut_name_edt_name = Entry(self.frame_1, bg=self.edit_btn_color, justify='center', font=('Arial', 15))
            self.aut_name_edt_name.insert(0, self.aut_name_selected)
            self.aut_name_edt_name.place(relx=0.25, rely=0.2, relwidth=0.53, relheight=0.30)
            self.edt_cancel_btn = Button(self.frame_1, text='Voltar', command=self.clean_edit_aut_name, bd=2, bg='#c93045', fg='white')
            self.edt_cancel_btn.place(relx=0.25, rely=0.57, relwidth=0.23, relheight=0.25)
            self.edt_save_btn = Button(self.frame_1, text='Salvar', command=self.edit_automation_name, bd=2, bg='#00A86B', fg='white')
            self.edt_save_btn.place(relx=0.55, rely=0.57, relwidth=0.23, relheight=0.25)
    def delete_aut_confirmation(self):
        if self.aut_name_selected == '':
            self.error_txt = 'Nenhuma automação selecionada'
            self.error_modal_screen()
        else:
            self.btn_add_aut.destroy()
            self.del_confirmation_msg = Label(self.frame_1, text='Deseja excluir a automação?', bg=self.frame_bg_color, font=('Arial', 13))
            self.del_confirmation_msg.place(relx=0.2, rely=0.1, relwidth=0.6, relheight=0.1)
            self.del_cancel_btn = Button(self.frame_1, text='Cancelar', command=self.clean_del_confirm, bd=2, bg='#00A86B', fg='white')
            self.del_cancel_btn.place(relx=0.25, rely=0.5, relwidth=0.23, relheight=0.30)
            self.del_confirm_btn = Button(self.frame_1, text='Excluir', command=self.delete_automation, bd=2, bg='#c93045', fg='white')
            self.del_confirm_btn.place(relx=0.55, rely=0.5, relwidth=0.23, relheight=0.30)
    def show_none_cmd_selected_err(self):
        self.error_txt = 'Nenhum comando selecionado'
        self.error_modal_screen()
    def show_cmd_multiple_selected_err(self):
        self.error_txt = 'Selecione apenas um comando'
        self.error_modal_screen()
    def set_add_cmd_above(self):
        if  len(self.command_selected) == 0:
            self.show_none_cmd_selected_err()
        elif self.cmd_multiple_selections:
            self.show_cmd_multiple_selected_err()
        else:
            self.add_cmd_dir = 'above'
            self.edit_cmd = False
            self.add_cmd()
    def set_add_cmd_below(self):
        if len(self.command_selected) == 0:
            self.show_none_cmd_selected_err()
        elif self.cmd_multiple_selections:
            self.show_cmd_multiple_selected_err()
        else:
            self.add_cmd_dir = 'below'
            self.edit_cmd = False
            self.add_cmd()
    def add_cmd(self):
            self.root_add_cmd = Toplevel()
            self.root_add_cmd.configure(background=self.root_bg_color)
            self.root_add_cmd.geometry("700x500")
            self.root_add_cmd.resizable(True, True)
            self.root_add_cmd.maxsize(width=1100, height=900)
            self.root_add_cmd.minsize(width=400, height=300)
            self.add_cmd_frame = Frame(self.root_add_cmd, bd=4, bg=self.frame_bg_color, highlightbackground='white', highlightthickness=3)
            self.add_cmd_frame.place(relx=0.02, rely=0.02, relwidth=0.96, relheight=0.96)
            if  not self.edit_cmd: self.add_cmd_wiget_frame()
    def add_cmd_wiget_frame(self):
        self.btn_keyboard_opt = Button(self.add_cmd_frame, text='Comandos teclado', command=self.open_keyboard_cmds, bd=2, bg=self.edit_btn_color)
        self.btn_keyboard_opt.place(relx=0.3, rely=0.1, relwidth=0.4, relheight=0.1)
        self.btn_mouse_opt = Button(self.add_cmd_frame, text='Comandos mouse', command=self.open_mouse_cmds, bd=2, bg=self.edit_btn_color)
        self.btn_mouse_opt.place(relx=0.3, rely=0.3, relwidth=0.4, relheight=0.1)
        self.btn_wait_opt = Button(self.add_cmd_frame, text='Aguardar', command=self.open_wait_cmd, bd=2, bg=self.edit_btn_color)
        self.btn_wait_opt.place(relx=0.3, rely=0.5, relwidth=0.4, relheight=0.1)
    def clean_types_commands(self):
        self.btn_keyboard_opt.destroy()
        self.btn_mouse_opt.destroy()
        self.btn_wait_opt.destroy()
    def open_keyboard_cmds(self):
        self.clean_types_commands()
        self.add_cmd_keyboard_title = Label(self.add_cmd_frame, text='Selecione o tipo de comando', bg=self.frame_bg_color, font=('Arial', 15))
        self.add_cmd_keyboard_title.place(relx=0, rely=0, relwidth=1, relheight=0.2)

        self.btn_press = Button(self.add_cmd_frame, text='Pressionar', command=self.keyboard_press, bd=2, bg=self.edit_btn_color)
        self.btn_press.place(relx=0.1667, rely=0.25, relwidth=0.25, relheight=0.1)

        self.btn_write= Button(self.add_cmd_frame, text='Escrever',command=self.keyboard_write, bd=2, bg=self.edit_btn_color)
        self.btn_write.place(relx=0.5834, rely=0.25, relwidth=0.25, relheight=0.1)

        self.btn_hold = Button(self.add_cmd_frame, text='Segurar', command=self.keyboard_hold, bd=2, bg=self.edit_btn_color)
        self.btn_hold.place(relx=0.1667, rely=0.4, relwidth=0.25, relheight=0.1)

        self.btn_key_up= Button(self.add_cmd_frame, text='Soltar', command=self.keyboard_release, bd=2, bg=self.edit_btn_color)
        self.btn_key_up.place(relx=0.5834, rely=0.4, relwidth=0.25, relheight=0.1)
    def clean_open_keyboard_cmds(self):
        self.add_cmd_keyboard_title.destroy()
        self.btn_press.destroy()
        self.btn_write.destroy()
        self.btn_hold.destroy()
        self.btn_key_up.destroy()
    def keyboard_press(self):
        self.subtype_cmd = 'Pressionar'
        self.entry_limit = 1
        self.open_add_cmds()
    def keyboard_write(self):
        self.subtype_cmd = 'Escrever'
        self.entry_limit = 250
        self.open_add_cmds()
    def keyboard_hold(self):
        self.subtype_cmd = 'Segurar'
        self.entry_limit = 1
        self.open_add_cmds()
    def keyboard_release(self):
        self.subtype_cmd = 'Soltar'
        self.entry_limit = 1
        self.open_add_cmds()
    def open_add_cmds(self):
        self.press_label = Label(self.add_cmd_frame, text=self.subtype_cmd, bg=self.frame_bg_color, font=('Arial', 15))
        self.press_label.place(relx=0, rely=0, relwidth=1, relheight=0.15)
        if self.edit_cmd:
            if self.entry_limit == 1:
                if len(self.command_selected.split('.')) == 1:
                    self.show_character()
                else:
                    self.show_special_opts()
            else:
                self.open_edit_entry()
        else:
            self.clean_open_keyboard_cmds()
            if self.entry_limit == 1:
                self.character_btn = Button(self.add_cmd_frame, text='Character', command=self.show_character, bd=2, bg=self.edit_btn_color)
                self.character_btn.place(relx=0.1667, rely=0.2, relwidth=0.25, relheight=0.1)
                self.special_btn = Button(self.add_cmd_frame, text='Especial', command=self.show_special_opts, bd=2, bg=self.edit_btn_color)
                self.special_btn.place(relx=0.5834, rely=0.2, relwidth=0.25, relheight=0.1)
            else:
                self.open_edit_entry()
    def clean_opt_btns(self):
        self.character_btn.destroy()
        self.special_btn.destroy()
    def show_character(self):
        if not self.edit_cmd: self.clean_opt_btns()
        self.edit_input = Entry(self.add_cmd_frame, bg=self.edit_btn_color)
        if self.edit_cmd: self.edit_input.insert(0, self.command_selected)
        self.edit_input.place(relx=0.375, rely=0.2, relwidth=0.25, relheight=0.1)
        self.btn_save = Button(self.add_cmd_frame, text='Salvar', command=self.save_keyboard_cmd, bd=2, bg=self.edit_btn_color)
        self.btn_save.place(relx=0.375, rely=0.35, relwidth=0.25, relheight=0.1)
    def open_edit_entry(self):
        self.edit_input = Entry(self.add_cmd_frame, bg=self.edit_btn_color)
        if self.edit_cmd: self.edit_input.insert(0, self.command_selected)
        self.edit_input.place(relx=0.375, rely=0.2, relwidth=0.25, relheight=0.1)
        self.btn_save = Button(self.add_cmd_frame, text='Salvar', command=self.save_keyboard_cmd, bd=2, bg=self.edit_btn_color)
        self.btn_save.place(relx=0.375, rely=0.35, relwidth=0.25, relheight=0.1)
    def show_special_opts(self):
        if not self.edit_cmd: self.clean_opt_btns()
        self.tree_special_opts = ttk.Treeview(self.add_cmd_frame, height=3, column=('col1'), show='headings')
        self.tree_special_opts.tag_configure('oddrow', background='white')
        self.tree_special_opts.tag_configure('evenrow', background=self.frame_bg_color)
        rowcount = 0
        for opt in special_opts:
            if rowcount % 2 == 0: 
                self.tree_special_opts.insert("", END, values=opt, tags=('oddrow',))
            else:
                self.tree_special_opts.insert("", END, values=opt, tags=('evenrow',))
            rowcount += 1
        self.tree_special_opts.heading('#0', text='')
        self.tree_special_opts.heading('#1', text='opções')
        self.tree_special_opts.column('#0', width=1)
        self.tree_special_opts.column('#1', width=500)
        self.tree_special_opts.place(relx=0.375, rely=0.15, relwidth=0.25, relheight=0.7)

        self.special_selected = ''
        def get_opt_selected(event):
            for opt_item in self.tree_special_opts.selection():
                item = self.tree_special_opts.item(opt_item)
                self.special_selected = item['values'][0]
        self.tree_special_opts.bind('<<TreeviewSelect>>', get_opt_selected)

        self.opt_scroll = Scrollbar(self.add_cmd_frame, orient='vertical', troughcolor=self.frame_bg_color, bd=2)
        self.tree_special_opts.configure(yscroll=self.opt_scroll.set)
        self.opt_scroll.place(relx=0.625, rely=0.15, relwidth=0.02, relheight=0.7)

        self.btn_save = Button(self.add_cmd_frame, text='Salvar', command=self.save_special_char_cmd, bd=2, bg=self.edit_btn_color)
        self.btn_save.place(relx=0.375, rely=0.88, relwidth=0.25, relheight=0.1)
    def open_mouse_cmds(self):
        def validate_mouse_pos(text):
            if text == '': return True
            try:
                value = float(text)
            except ValueError:
                return False
            return 0 <= value <= 100000
        self.vcmd = (self.root.register(validate_mouse_pos), '%P')

        if not self.edit_cmd: self.clean_types_commands()
        self.add_cmd_mouse_title = Label(self.add_cmd_frame, text='Selecione o tipo de comando', bg=self.frame_bg_color, font=('Arial', 15))
        self.add_cmd_mouse_title.place(relx=0, rely=0, relwidth=1, relheight=0.2)

        self.lbl_mouse_pos = Label(self.add_cmd_frame, text='posição do mouse', bg=self.frame_bg_color, font=('Arial', 15))
        self.lbl_mouse_pos.place(relx=0.25, rely=0.25, relwidth=0.25, relheight=0.1)
        self.lbl_xpos = Label(self.add_cmd_frame, text='x:', bg=self.frame_bg_color, font=('Arial', 15))
        self.lbl_xpos.place(relx=0.53, rely=0.25, relwidth=0.05, relheight=0.1)
        self.xpos = Entry(self.add_cmd_frame, bg=self.edit_btn_color, validate='key', validatecommand=self.vcmd)
        self.xpos.place(relx=0.58, rely=0.25, relwidth=0.1, relheight=0.1)
        self.lbl_ypos = Label(self.add_cmd_frame, text='y:', bg=self.frame_bg_color, font=('Arial', 15))
        self.lbl_ypos.place(relx=0.68, rely=0.25, relwidth=0.05, relheight=0.1)
        self.ypos = Entry(self.add_cmd_frame, bg=self.edit_btn_color, validate='key', validatecommand=self.vcmd)
        self.ypos.place(relx=0.73, rely=0.25, relwidth=0.1, relheight=0.1)

        self.btn_click = Button(self.add_cmd_frame, text='click', command=self.open_click_mouse_opts, bd=2, bg=self.edit_btn_color)
        self.btn_click.place(relx=0.25, rely=0.4, relwidth=0.25, relheight=0.1)

        self.btn_scroll= Button(self.add_cmd_frame, text='scroll', command=self.open_scroll_mouse_opts, bd=2, bg=self.edit_btn_color)
        self.btn_scroll.place(relx=0.55, rely=0.4, relwidth=0.25, relheight=0.1)
    def clean_mouse_btn(self):
        self.btn_click.destroy()
        self.btn_scroll.destroy()
    def open_click_mouse_opts(self):
        self.clean_mouse_btn()
        self.btn_choices_lbl = Label(self.add_cmd_frame, text='Botão', bg=self.frame_bg_color, font=('Arial', 15))
        self.btn_choices_lbl.place(relx=0.2, rely=0.4, relwidth=0.17, relheight=0.1)
        btn_opts = ['Esquerdo', 'Direito']
        self.choices_clicked = StringVar()
        self.choices_clicked.set('Esquerdo')
        self.btn_choices = OptionMenu(self.add_cmd_frame, self.choices_clicked, *btn_opts)
        self.btn_choices.place(relx=0.37, rely=0.4, relwidth=0.17, relheight=0.1)

        self.num_clicks_lbl = Label(self.add_cmd_frame, text='Click', bg=self.frame_bg_color, font=('Arial', 15))
        self.num_clicks_lbl.place(relx=0.2, rely=0.63, relwidth=0.17, relheight=0.1)
        num_opts = ['Simples', 'Duplo']
        self.num_clicked = StringVar()
        self.num_clicked.set('Simples')
        self.num_clicks = OptionMenu(self.add_cmd_frame, self.num_clicked, *num_opts)
        self.num_clicks.place(relx=0.37, rely=0.63, relwidth=0.17, relheight=0.1)

        self.save_new_mouse_cmd = Button(self.add_cmd_frame, text='Salvar', command=self.save_new_mouse_click, bd=2, bg=self.edit_btn_color)
        self.save_new_mouse_cmd.place(relx=0.37, rely=0.85, relwidth=0.25, relheight=0.1)
    def open_scroll_mouse_opts(self):
        self.clean_mouse_btn()
        self.scroll_opts = []
        self.scroll_clicked = StringVar()
        def set_vertical_scroll_opts():
            self.scroll_sense = 'vertical'
            self.scroll_opts.append('para cima')
            self.scroll_opts.append('para baixo')
            self.scroll_clicked.set('para cima')
            self.show_scroll_opts()
        def set_horizontal_scroll_opts():
            self.scroll_sense = 'horizontal'
            self.scroll_opts.append('para direita')
            self.scroll_opts.append('para esquerda')
            self.scroll_clicked.set('para direita')
            self.show_scroll_opts()

        self.scroll_vertical = Button(self.add_cmd_frame, text='vertical', command=set_vertical_scroll_opts, bd=2, bg=self.edit_btn_color)
        self.scroll_vertical.place(relx=0.25, rely=0.4, relwidth=0.25, relheight=0.1)

        self.scroll_horizontal= Button(self.add_cmd_frame, text='horizontal', command=set_horizontal_scroll_opts, bd=2, bg=self.edit_btn_color)
        self.scroll_horizontal.place(relx=0.55, rely=0.4, relwidth=0.25, relheight=0.1)
    def show_scroll_opts(self):
        self.scroll_vertical.destroy()
        self.scroll_horizontal.destroy()
        self.scroll_options = OptionMenu(self.add_cmd_frame, self.scroll_clicked, *self.scroll_opts)
        self.scroll_options.place(relx=0.37, rely=0.4, relwidth=0.25, relheight=0.1)

        self.save_new_mouse_cmd = Button(self.add_cmd_frame, text='Salvar', command=self.save_new_mouse_scroll, bd=2, bg=self.edit_btn_color)
        self.save_new_mouse_cmd.place(relx=0.37, rely=0.7, relwidth=0.25, relheight=0.1)
    def open_wait_cmd(self):
        def validate_wait_entry(text):
            if text == '': return True
            try:
                value = int(text)
            except ValueError:
                return False
            return 0 <= value <= 10000000000
        self.validate_wait = (self.root.register(validate_wait_entry), '%P')
        if not self.edit_cmd: self.clean_types_commands()
        self.add_cmd_wait_title = Label(self.add_cmd_frame, text='Aguardar', bg=self.frame_bg_color, font=('Arial', 15))
        self.add_cmd_wait_title.place(relx=0, rely=0, relwidth=1, relheight=0.2)

        self.lbl_add_cmd_wait = Label(self.add_cmd_frame, text='Coloque abaixo o tempo em segundos', bg=self.frame_bg_color, font=('Arial', 15))
        self.lbl_add_cmd_wait.place(relx=0, rely=0.2, relwidth=1, relheight=0.2)
        self.entry_add_cmd_wait = Entry(self.add_cmd_frame, bg=self.edit_btn_color, validate='key', validatecommand=self.validate_wait, justify='center', font=('Arial', 15))
        self.entry_add_cmd_wait.place(relx=0.35, rely=0.4, relwidth=0.3, relheight=0.1)

        self.btn_save_wait_cmd = Button(self.add_cmd_frame, text='Salvar', command=self.save_wait_command, bd=2, bg=self.edit_btn_color)
        self.btn_save_wait_cmd.place(relx=0.35, rely=0.7, relwidth=0.3, relheight=0.1)
    def edit_command(self):
        def get_mouse_command(cmd_str, cmd_idx):
            mouse_commands = cmd_str.split(',')
            return mouse_commands[cmd_idx]
        def set_mouse_position():
            self.xpos.insert(0, get_mouse_command(self.command_selected, 0))
            self.ypos.insert(0, get_mouse_command(self.command_selected, 1))

        if len(self.command_selected) == 0:
            self.show_none_cmd_selected_err()
        elif self.cmd_multiple_selections:
            self.show_cmd_multiple_selected_err()
        else:
            self.edit_cmd = True
            self.add_cmd()
            if self.cmd_subtype == 'Pressionar':
                self.keyboard_press()
            elif self.cmd_subtype == 'Escrever':
                self.keyboard_write()
            elif self.cmd_subtype == 'Segurar':
                self.keyboard_hold()
            elif self.cmd_subtype == 'Soltar':
                self.keyboard_release()
            elif self.cmd_subtype == 'click':
                self.open_mouse_cmds()
                self.open_click_mouse_opts()
                set_mouse_position()
                self.choices_clicked.set(get_mouse_command(self.command_selected, 2))
                self.num_clicked.set('Simples' if get_mouse_command(self.command_selected, 3) == '1' else 'Duplo')
            elif self.cmd_subtype == 'scroll':
                self.open_mouse_cmds()
                self.open_scroll_mouse_opts()
                set_mouse_position()
                if get_mouse_command(self.command_selected, 2) == '0':
                    self.scroll_sense = 'vertical'
                    self.scroll_opts.append('para cima')
                    self.scroll_opts.append('para baixo')
                    self.scroll_clicked.set(get_mouse_command(self.command_selected, 3))
                    self.show_scroll_opts()
                else:
                    self.scroll_sense = 'horizontal'
                    self.scroll_opts.append('para direita')
                    self.scroll_opts.append('para esquerda')
                    self.scroll_clicked.set(get_mouse_command(self.command_selected, 2))
                    self.show_scroll_opts()
            elif self.cmd_subtype == 'aguardar':
                self.open_wait_cmd()
                self.entry_add_cmd_wait.insert(0, int(self.command_selected))
    def switch_all_screen_buttons_state(self):
        btns_main_screen = [self.btn_add_aut, self.btn_edit_nome_aut, self.btn_run_aut, self.btn_edit_aut, self.btn_del_aut]
        for btn in btns_main_screen:
            btn['state'] = self.switch_btn_state


Application()
