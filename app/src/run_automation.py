import sqlite3

import pyautogui
from pynput.keyboard import Controller, Key


def run_automation(aut_id):
    print(f'running automation {aut_id}')

    pyautogui.PAUSE = 1
    keyboard = Controller()

    database = sqlite3.connect('db-bot-collie.db', check_same_thread=False)
    cursor = database.cursor()

    # buscar no banco os comandos referentes a id da automacao
    commands = cursor.execute(
        f'SELECT * FROM comando WHERE automacao_id = {aut_id}').fetchall()
    for command in commands:
        # id do comando command[0]
        # id da automacao command[1]
        # o comando
        cmd = command[2]
        if len(cmd.split('.')) == 1:
            print('tecla normal')
            print(cmd)
            # keyboard.press(cmd)
            # keyboard.release(cmd)
            pyautogui.press(cmd)
        else:
            print('tecla especial')
            special_cmd = cmd.split('.')[1]
            print(special_cmd)
            if special_cmd == 'cmd':
                special_cmd = 'win'
            pyautogui.press(special_cmd)
            # keyboard.press(Key[special_cmd])
            # keyboard.release(Key[special_cmd])
