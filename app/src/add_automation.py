import sqlite3
import sys
from tkinter import *
from tkinter import ttk

from pynput import keyboard

database = sqlite3.connect('db-bot-collie.db')

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
    frm = ttk.Frame(modalConfirmation, padding=10)
    frm.grid()

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
    
    ttk.Label(frm, text="Para adicionar uma nova automação clique em começar").grid(column=0, row=0, padx=10, pady=10, columnspan=2)
    ttk.Button(frm, text="voltar", command=modalConfirmation.destroy).grid(column=0, row=1, padx=10, pady=10)
    ttk.Button(frm, text="começar", command=watch_keyboard).grid(column=1, row=1, padx=10, pady=10)

sys.modules[__name__] = add_automation
