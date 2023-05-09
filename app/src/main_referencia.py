from tkinter import *
from tkinter import ttk

# import pyautogui
from add_automation_ref import add_automation
from get_automations import get_automations
from run_automation import run_automation

root = Tk()

main_bg_color = '#babdc2'

root.title('Bot Collie')
root.configure(background=main_bg_color)
root.geometry("700x500")
root.resizable(True, True)
# se clicar em ampliar ele permite aumentar a tela acima desse limite
root.maxsize(width=900, height=700)
root.minsize(width=400, height=300)

# frame = Frame(bd=4, bg='#edeff2', highlightbackground='blue', highlightthickness=3)
# frame.place(relx=0.02, rely=0.02, relwidth=0.96, relheight=0.46)

margin = 0.02

logo = Label(root, text="Logo aqui",bg='#edeff2')
logo_rel_size = 0.1
logo.place(relx=margin, rely=margin, relwidth=logo_rel_size, relheight=logo_rel_size)

automation_button_rel_size = 0.07
button_text_relx = 0.5
button_text_rely = 0.3
button_text = Label(root, text='Criar nova automação', bg=main_bg_color)
button_text.place(relx=button_text_relx, rely=margin, relwidth=button_text_rely, relheight=automation_button_rel_size)
add_automation_button = Button(root, text='+', command=add_automation)
add_automation_button.place(relx=button_text_relx + button_text_rely, rely=margin, relwidth=automation_button_rel_size, relheight=automation_button_rel_size)

# VALIDAR SE DÁ PRA FAZER A AUTOMAÇÃO RODAR MESMO
# colocar apenas a ultima automação criada
automations = get_automations()
if (len(automations) != 0):
    aut_id = automations[len(automations)-1][0]
    aut_name = automations[len(automations)-1][1]
    def aut_btn_pressed():
        # pyautogui.hotkey('cmd', 'd')
        run_automation(aut_id)
    botao_teste = Button(root, text=aut_name, command=aut_btn_pressed)
    botao_teste.place(relx=0, rely=0.4, relwidth=1, relheight=0.1)
# depois pensar em como fazer a lista atualizar sozinha
# a unica solução é colocar todo o codigo num arquivo só e usar classe como no curbutton_text_relxso

# frame2 = Frame(bd=4, bg='#edeff2', highlightbackground='blue', highlightthickness=3)
# frame2.place(relx=0.02, rely=0.5, relwidth=0.96, relheight=0.46)

# abordagem com grid -> excluir se não for usar
# frm = ttk.Frame(root, padding=10)
# frm.grid()
# ttk.Label(frm, text="Logo aqui").grid(column=0, row=0)
# ttk.Label(frm, text="Adicionar automação").grid(column=1, row=1, padx=10)
# ttk.Button(frm, text="+", command=add_automation).grid(column=2, row=1)

root.mainloop()
