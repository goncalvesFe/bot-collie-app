import sqlite3
from tkinter import *
from tkinter import ttk, messagebox

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
        self.cursor.execute("CREATE TABLE IF NOT EXISTS comando (id integer PRIMARY KEY, automacao_id int, type text, subtype text, command text, cmdOrder int)")
        self.conn.commit()
        self.disconnect_database()
    def delete_automation(self):
        self.connect_database()
        self.cursor.execute(f"DELETE FROM automacao WHERE id='{self.aut_id_selected}'")
        self.cursor.execute(f"DELETE FROM comando WHERE automacao_id='{self.aut_id_selected}'")
        self.conn.commit()
        self.disconnect_database()
        self.update_tree()
        self.clean_del_confirm()
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
        ids = self.cursor.execute(f"SELECT id FROM comando WHERE automacao_id='{self.aut_id_selected}' ORDER BY cmdOrder ASC").fetchall()
        order_to_update = 1
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
        # estrutura dos comandos adicionados sempre será:
        # commands = [['type', 'subtype', 'cmd'], ['type', 'subtype', 'cmd'], ...]
        pyautogui.hotkey('win', 'd')
        def on_press(key):
            self.commands.append(['keyboard', 'press', key])
            try:
                print('alphanumeric key {0} pressed'.format(key.char))
            except AttributeError:
                print('special key {0} pressed'.format(key))
        def on_release(key):
            if key == keyboard.Key.esc:
                self.save_automation()
                # Stop listeners
                # self.mouse_listener.stop()
                return False
        def on_move(x, y):
            # print('Pointer moved to {0}'.format((x, y)))
            pass
        def on_click(x, y, button, pressed):
            if pressed:
                mouse_click = f'click-x:{x},y:{y},button:{button}'
                print(mouse_click)
                self.commands.append(mouse_click)
        def on_scroll(x, y, dx, dy):
            if dx == 0:
                hscroll = dx
            elif dx == -1:
                hscroll = 'right'
            elif dx == 1:
                hscroll = 'left'
            if dy == 0:
                vscroll = dy
            elif dy == -1:
                vscroll = 'down'
            elif dy == 1:
                vscroll = 'up'
            mouse_scroll = f'scroll-x:{x},y:{y},dx:{hscroll},dy:{vscroll}'
            print(mouse_scroll)
            self.commands.append(mouse_scroll)
        self.keyboard_listener = keyboard.Listener(on_press=on_press, on_release=on_release)
        self.keyboard_listener.start()
        # self.mouse_listener = mouse.Listener(on_move=on_move, on_click=on_click, on_scroll=on_scroll)
        # self.mouse_listener.start()
        # não esquecer de descomentar a linha 106
    def run_automation(self):
        if self.aut_name_selected == '':
            self.error_txt = 'Nenhuma automação selecionada'
            self.error_modal_screen()
        else:
            self.connect_database()
            aut_id = self.cursor.execute(f"SELECT id FROM automacao WHERE name='{self.aut_name_selected}'").fetchone()[0]
            commands = self.cursor.execute(f"SELECT * FROM comando WHERE automacao_id='{aut_id}'").fetchall()
            pyautogui.hotkey('win', 'd')
            for command in commands:
                type = command[2]
                subtype = command[3]
                cmd = command[4]
                cmd_str_split = cmd.split('-')
                if type == 'keyboard':
                    if subtype == 'press':
                        if len(cmd.split('.')) == 1:
                            pyautogui.press(cmd)
                        else:
                            special_cmd = cmd.split('.')[1]
                            if special_cmd == 'cmd':
                                special_cmd = 'win'
                            pyautogui.press(special_cmd)
                else:
                    mouse_parameters = cmd_str_split[1].split(',')
                    print('mouse_parameters: ', mouse_parameters)
                    pos_x = int(mouse_parameters[0].split(':')[1])
                    pos_y = int(mouse_parameters[1].split(':')[1])
                    if cmd_str_split[0] == 'click':
                        btn_click = mouse_parameters[2].split(':')[1].split('.')[1]
                        print(f'click : x={pos_x}, y={pos_y}, button={btn_click}, clicks=1')
                        pyautogui.click(x=pos_x, y=pos_y, button=btn_click, clicks=1)
                    else:
                        dx = mouse_parameters[2].split(':')[1]
                        dy = mouse_parameters[3].split(':')[1]
                        print(f'scroll: x={pos_x}, y={pos_y}, dx={dx}, dy={dy}')
                        if dx == '0':
                            if dy == 'up':
                                pyautogui.scroll(10, x=pos_x, y=pos_y)
                            else:
                                pyautogui.scroll(-10, x=pos_x, y=pos_y)
                        else:
                            # scroll horizontal
                            if dx == 'right':
                                pyautogui.hscroll(10, x=pos_x, y=pos_y)
                            else:
                                pyautogui.hscroll(-10, x=pos_x, y=pos_y)
            self.disconnect_database()
    def save_keyboard_cmd(self):
        input_len = len(self.edit_input.get())
        if input_len == 0:
            messagebox.showerror(title='Erro', message='Entrada vazia')
        elif input_len > self.entry_limit:
            messagebox.showwarning(title='Atenção!', message='Número de characters é maior que o permitido.')
        else:
            cmdOrder = 0
            print('self.add_cmd_dir: ',self.add_cmd_dir)
            if self.add_cmd_dir == 'above':
                cmdOrder = self.cmd_order_selected - 1
            else:
                cmdOrder = self.cmd_order_selected + 1
            self.connect_database()
            insert_query = f"INSERT INTO comando (automacao_id, type, subtype, command, cmdOrder) VALUES ({self.aut_id_selected}, 'keyboard', '{self.subtype_cmd}', '{self.edit_input.get()}', {cmdOrder})"
            self.cursor.execute(insert_query)
            self.conn.commit()
            self.disconnect_database()
            self.update_all_cmd_order()
            self.root_add_cmd.destroy()
            self.command_selected = ''
            self.cmd_seleted.config(text=self.command_selected)
            self.update_edit_tree()
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
        self.conf9irm_cmd_del = False
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
    def config_constants(self):
        self.app_version = '1.0'
        self.title = f'Bot Collie - v_{self.app_version}'
        self.root_bg_color = '#babdc2'
        self.frame_bg_color = '#edeff2'
        self.edit_btn_color = '#dae1eb'
    def screen(self):
        self.root.title(self.title)
        self.root.configure(background=self.root_bg_color)
        self.root.geometry("900x800")
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
        self.del_cmd_msg = Label(self.error_modal_frame, text='Deseja excluir o comando?', bg=self.frame_bg_color, font=('Arial', 14))
        self.del_cmd_msg.place(relx=0, rely=0.1, relwidth=1, relheight=0.3)
        self.Ndel_cmd_confirm_btn = Button(self.error_modal_frame, text='Cancelar', command=self.reset_confirm_cmd_del, bd=2, bg='#c93045', fg='white')
        self.Ndel_cmd_confirm_btn.place(relx= 0.15, rely=0.5, relwidth=0.3, relheight=0.15)
        self.del_cmd_confirm_btn = Button(self.error_modal_frame, text='Excluir', command=self.delete_command, bd=2, bg='#00A86B', fg='white')
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
        self.logo_img = PhotoImage(file='assets/bot_collie_logo90X70.png')
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

        self.auto_selected = Label(self.frame_2, text='Selecione a automação', bg=self.edit_btn_color, font=('Arial', 15))
        self.auto_selected.place(relx=0.62, rely=0.03, relwidth=0.36, relheight=0.09)

        self.btn_run_aut = Button(self.frame_2, text='Rodar automação', command=self.run_automation, bd=2, bg='#00A86B', fg='white')
        self.btn_run_aut.place(relx=0.62, rely=0.25, relwidth=0.36, relheight=0.09)

        self.btn_edit_aut = Button(self.frame_2, text='Editar automação', command=self.edit_screen, bd=2, bg='#5a4aed', fg='white')
        self.btn_edit_aut.place(relx=0.62, rely=0.45, relwidth=0.36, relheight=0.09)

        self.btn_del_aut = Button(self.frame_2, text='Excluir automação', command=self.delete_aut_confirmation, bd=2, bg='#c93045', fg='white')
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

        self.add_above_lbl = Label(self.edit_frame, text='Adicionar comando acima', bg=self.frame_bg_color, font=('Arial', 13))
        self.add_above_lbl.place(relx=0.62, rely=0.03, relwidth=0.36, relheight=0.09)
        self.add_above_btn = Button(self.edit_frame, text='+', command=self.set_add_cmd_above, bd=2, bg=self.edit_btn_color)
        self.add_above_btn.place(relx=0.62, rely=0.1, relwidth=0.36, relheight=0.05)

        self.cmd_seleted = Label(self.edit_frame, text='Selecione o comando', bg=self.edit_btn_color, font=('Arial', 15))
        self.cmd_seleted.place(relx=0.62, rely=0.3, relwidth=0.36, relheight=0.09)
        self.btn_edt_cmd = Button(self.edit_frame, text='Editar comando', command=self.add_command_widgets, bd=2, bg='#5a4aed', fg='white')
        self.btn_edt_cmd.place(relx=0.62, rely=0.40, relwidth=0.36, relheight=0.07)
        self.btn_del_cmd = Button(self.edit_frame, text='Excluir comando', command=self.confirm_del_cmd, bd=2, bg='#c93045', fg='white')
        self.btn_del_cmd.place(relx=0.62, rely=0.50, relwidth=0.36, relheight=0.06)

        self.add_below_lbl = Label(self.edit_frame, text='Adicionar comando abaixo', bg=self.frame_bg_color, font=('Arial', 13))
        self.add_below_lbl.place(relx=0.62, rely=0.8, relwidth=0.36, relheight=0.09)
        self.add_below_btn = Button(self.edit_frame, text='+', command=self.set_add_cmd_below, bd=2, bg=self.edit_btn_color)
        self.add_below_btn.place(relx=0.62, rely=0.77, relwidth=0.36, relheight=0.05)
    def confirm_del_cmd(self):
        if self.command_selected == '':
            self.error_txt = 'Nenhum comando selecionado'
        else:
            self.confirm_cmd_del = True
        self.error_modal_screen()
    def reset_confirm_cmd_del(self):
        self.confirm_cmd_del = False
        self.root_error_modal.destroy()
    def show_keyboard_opt(self):
        pass
    def show_mouse_opt(self):
        pass
    def clean_del_confirm(self):
        self.aut_name_selected = ''
        self.auto_selected.config(text=self.aut_name_selected)
        self.update_tree()
        self.del_confirmation_msg.destroy()
        self.del_cancel_btn.destroy()
        self.del_confirm_btn.destroy()
        self.widgets_frame_1()
    def delete_aut_confirmation(self):
        if self.aut_name_selected == '':
            self.error_txt = 'Nenhuma automação selecionada'
            self.error_modal_screen()
        else:
            self.btn_add_aut.destroy()
            self.del_confirmation_msg = Label(self.frame_1, text='Deseja excluir a automação?', bg=self.frame_bg_color, font=('Arial', 13))
            self.del_confirmation_msg.place(relx=0.2, rely=0.1, relwidth=0.6, relheight=0.1)
            self.del_cancel_btn = Button(self.frame_1, text='Cancelar', command=self.clean_del_confirm, bd=2, bg='#c93045', fg='white')
            self.del_cancel_btn.place(relx=0.25, rely=0.5, relwidth=0.23, relheight=0.30)
            self.del_confirm_btn = Button(self.frame_1, text='Excluir', command=self.delete_automation, bd=2, bg='#00A86B', fg='white')
            self.del_confirm_btn.place(relx=0.55, rely=0.5, relwidth=0.23, relheight=0.30)
    def set_add_cmd_above(self):
        if self.command_selected == '':
            self.error_txt = 'Nenhum comando selecionado'
            self.error_modal_screen()
        else:
            self.add_cmd_dir = 'above'
            self.add_cmd()
    def set_add_cmd_below(self):
        if self.command_selected == '':
            self.error_txt = 'Nenhum comando selecionado'
            self.error_modal_screen()
        else:
            self.add_cmd_dir = 'below'
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
            self.add_cmd_wiget_frame()
    def add_cmd_wiget_frame(self):
        self.btn_keyboard_opt = Button(self.add_cmd_frame, text='Comandos teclado', command=self.open_keyboard_cmds, bd=2, bg=self.edit_btn_color)
        self.btn_keyboard_opt.place(relx=0.05, rely=0.02, relwidth=0.4, relheight=0.07)
        self.btn_mouse_opt = Button(self.add_cmd_frame, text='Comandos mouse', bd=2, bg=self.edit_btn_color)
        self.btn_mouse_opt.place(relx=0.55, rely=0.02, relwidth=0.4, relheight=0.07)
    def open_keyboard_cmds(self):
        self.btn_keyboard_opt.destroy()
        self.btn_mouse_opt.destroy()
        self.add_cmd_keyboard_title = Label(self.add_cmd_frame, text='Selecione o tipo de comando', bg=self.frame_bg_color, font=('Arial', 15))
        self.add_cmd_keyboard_title.place(relx=0, rely=0, relwidth=1, relheight=0.2)

        self.btn_press = Button(self.add_cmd_frame, text='Pressionar', command=self.keyboard_press, bd=2, bg=self.edit_btn_color)
        self.btn_press.place(relx=0.1667, rely=0.25, relwidth=0.25, relheight=0.1)

        self.btn_write= Button(self.add_cmd_frame, text='Escrever', bd=2, bg=self.edit_btn_color)
        self.btn_write.place(relx=0.5834, rely=0.25, relwidth=0.25, relheight=0.1)

        self.btn_hold = Button(self.add_cmd_frame, text='Segurar', bd=2, bg=self.edit_btn_color)
        self.btn_hold.place(relx=0.1667, rely=0.4, relwidth=0.25, relheight=0.1)

        self.btn_key_up= Button(self.add_cmd_frame, text='Soltar', bd=2, bg=self.edit_btn_color)
        self.btn_key_up.place(relx=0.5834, rely=0.4, relwidth=0.25, relheight=0.1)

        self.btn_hotkey = Button(self.add_cmd_frame, text='Atalho', bd=2, bg=self.edit_btn_color)
        self.btn_hotkey.place(relx=0.375, rely=0.55, relwidth=0.25, relheight=0.1)
    def clean_open_keyboard_cmds(self):
        self.add_cmd_keyboard_title.destroy()
        self.btn_press.destroy()
        self.btn_write.destroy()
        self.btn_hold.destroy()
        self.btn_key_up.destroy()
        self.btn_hotkey.destroy()
    def keyboard_press(self):
        self.subtype_cmd = 'press'
        self.clean_open_keyboard_cmds()
        self.press_label = Label(self.add_cmd_frame, text='Pressionar', bg=self.frame_bg_color, font=('Arial', 15))
        self.press_label.place(relx=0, rely=0, relwidth=1, relheight=0.2)
        self.edit_input = Entry(self.add_cmd_frame, bg=self.edit_btn_color)
        self.edit_input.place(relx=0.375, rely=0.2, relwidth=0.25, relheight=0.1)
        self.entry_limit = 1
        self.btn_save = Button(self.add_cmd_frame, text='Salvar', command=self.save_keyboard_cmd, bd=2, bg=self.edit_btn_color)
        self.btn_save.place(relx=0.375, rely=0.35, relwidth=0.25, relheight=0.1)
    def add_command_widgets(self):
        if self.command_selected == '':
            self.error_txt = 'Nenhum comando selecionado'
            self.error_modal_screen()
        else:
            self.tree_command.destroy()
            self.ed_scroll.destroy()
            self.add_above_lbl.destroy()
            self.add_above_btn.destroy()
            self.cmd_seleted.destroy()
            self.btn_edt_cmd.destroy()
            self.btn_del_cmd.destroy()
            self.add_below_lbl.destroy()
            self.add_below_btn.destroy()

            self.btn_keyboard_opt = Button(self.edit_frame, text='Comandos teclado', bd=2, bg=self.edit_btn_color)
            self.btn_keyboard_opt.place(relx=0.05, rely=0.02, relwidth=0.4, relheight=0.07)
            self.btn_mouse_opt = Button(self.edit_frame, text='Comandos mouse', bd=2, bg=self.edit_btn_color)
            self.btn_mouse_opt.place(relx=0.55, rely=0.02, relwidth=0.4, relheight=0.07)


Application()
