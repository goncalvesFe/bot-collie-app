from tkinter import *

from pynput import keyboard, mouse
from save_automation import save_automation


def add_automation():
    commands = []
    stop_mouse_watcher = False

    def on_press(key):
        commands.append(key)
        try:
            print('alphanumeric key {0} pressed'.format(key.char))
        except AttributeError:
            print('special key {0} pressed'.format(key))

    def on_release(key):
        if key == keyboard.Key.esc:
            print('stop listener')
            for command in commands:
                print(command)
            # save_automation(commands)
            # Stop listener
            return False

    def on_move(x, y):
        print('Pointer moved to {0}'.format((x, y)))

    def on_click(x, y, button, pressed):
        print('{0} at {1}'.format('Pressed' if pressed else 'Released', (x, y)))
        if not pressed:
            print('not pressed')
            # Stop listener
            # return False

    def on_scroll(x, y, dx, dy):
        print('Scrolled {0} at {1}'.format('down' if dy < 0 else 'up', (x, y)))

    def init_watchers():
        keyboard_listener = keyboard.Listener(on_press=on_press, on_release=on_release)
        keyboard_listener.start()
        mouse_listener = mouse.Listener(on_move=on_move, on_click=on_click, on_scroll=on_scroll)
        mouse_listener.start()
        print('AQUI')
        print(keyboard_listener.is_alive())

    main_bg_color = '#babdc2'
    margin = 0.02

    modalConfirmation = Tk()
    modalConfirmation.title('Teste modal')
    modalConfirmation.configure(background=main_bg_color)
    modalConfirmation.geometry("400x200")
    modalConfirmation.resizable(True, True)
    modalConfirmation.maxsize(width=700, height=500)
    # modalConfirmation.minsize(width=300, height=200)

    btn_rel_size_w = 0.4
    btn_rel_size_h = 0.15
    btn_rel_pos_y = 0.5
    main_text = Label(modalConfirmation, text="Para criar uma nova automação clique em começar", bg=main_bg_color)
    main_text.place(relx=0, rely=0, relwidth=1, relheight=0.3)
    back_btn = Button(modalConfirmation, text="voltar", command=modalConfirmation.destroy)
    back_btn.place(relx=margin, rely=btn_rel_pos_y, relwidth=btn_rel_size_w, relheight=btn_rel_size_h)
    begin_btn = Button(modalConfirmation, text="começar", command=init_watchers)
    begin_btn.place(relx=1 - (margin + btn_rel_size_w), rely=btn_rel_pos_y, relwidth=btn_rel_size_w, relheight=btn_rel_size_h)
