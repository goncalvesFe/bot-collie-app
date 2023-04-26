import sqlite3
import sys
from tkinter import *

from pynput import keyboard

database = sqlite3.connect('db-bot-collie.db')

main_bg_color = '#babdc2'
margin = 0.02

def on_press(key):
    try:
        print('alphanumeric key {0} pressed'.format(
            key.char))
    except AttributeError:
        print('special key {0} pressed'.format(
            key))

def on_release(key):
    print('{0} released'.format(
        key))
    if key == keyboard.Key.esc:
        # Stop listener
        return False

def add_automation():
    modalConfirmation = Tk()
    modalConfirmation.title('Teste modal')
    modalConfirmation.configure(background=main_bg_color)
    modalConfirmation.geometry("400x200")
    modalConfirmation.resizable(True, True)
    modalConfirmation.maxsize(width=700, height=500)
    # modalConfirmation.minsize(width=300, height=200)

    def watch_keyboard():
        modalConfirmation.destroy
        # Collect events until released
        # with keyboard.Listener(
        #         on_press=on_press,
        #         on_release=on_release) as listener:
        #     listener.join()

        # ...or, in a non-blocking fashion:
        listener = keyboard.Listener(
            on_press=on_press,
            on_release=on_release)
        listener.start()
        # listener.stop()

    btn_rel_size_w = 0.4
    btn_rel_size_h = 0.15
    btn_rel_pos_y = 0.5
    main_text = Label(modalConfirmation, text="Para criar uma nova automação clique em começar", bg=main_bg_color)
    main_text.place(relx=0, rely=0, relwidth=1, relheight=0.3)
    back_btn = Button(modalConfirmation, text="voltar", command=modalConfirmation.destroy)
    back_btn.place(relx=margin, rely=btn_rel_pos_y, relwidth=btn_rel_size_w, relheight=btn_rel_size_h)
    begin_btn = Button(modalConfirmation, text="começar", command=watch_keyboard)
    begin_btn.place(relx=1 - (margin + btn_rel_size_w), rely=btn_rel_pos_y, relwidth=btn_rel_size_w, relheight=btn_rel_size_h)

sys.modules[__name__] = add_automation
