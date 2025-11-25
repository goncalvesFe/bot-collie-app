from typing import Optional, List, Dict
from pynput import keyboard, mouse
import pyautogui
import time
from database.repositories import AutomationRepository, CommandRepository
from database.models import Automation, Command
import subprocess
import threading


class AutomationService:
    @staticmethod
    def init_listeners():
        # estrutura dos comandos adicionados sempre será:
        # commands = [['type', 'subtype', 'cmd'], ['type', 'subtype', 'cmd'], ...]
        commands = []
        pyautogui.hotkey('win', 'd')

        def on_press(key):
            if key != keyboard.Key.esc:
                commands.append(['keyboard', 'Pressionar', key])
        
        def on_release(key):
            if key == keyboard.Key.esc:
                mouse_listener.stop()
                
                # Criar nova automação
                from datetime import datetime
                automation_name = f"Nova Automação {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
                automation = Automation(name=automation_name, description="Automação criada via gravação")
                automation_id = AutomationRepository.create(automation)
                
                if automation_id:
                    print(f"Automação '{automation_name}' criada com ID: {automation_id}")
                    # Salvar comandos
                    for index, cmd in enumerate(commands):
                        # cmd structure: ['type', 'subtype', 'cmd']
                        new_command = Command(
                            automation_id=automation_id,
                            type=cmd[0],
                            subtype=cmd[1],
                            command=str(cmd[2]),
                            cmdOrder=index
                        )
                        CommandRepository.create(new_command)
                    print(f'{len(commands)} comandos salvos com sucesso!')
                
                return False

        def on_move(x, y):
            # print('Pointer moved to {0}'.format((x, y)))
            pass

        def on_click(x, y, button, pressed):
            btn = 'Esquerdo' if button.name == 'left' else 'Direito'
            if pressed:
                # command: ‘x,y,button,num’ 
                mouse_click = f'{x},{y},{btn},1'
                commands.append(['mouse', 'click', mouse_click])

        def on_scroll(x, y, dx, dy):
            hscroll_map = {0: 0, -1: 'para direita', 1: 'para esquerda'}
            vscroll_map = {0: 0, -1: 'para baixo', 1: 'para cima'}

            hscroll = hscroll_map.get(dx, dx)
            vscroll = vscroll_map.get(dy, dy)
            
            # command: ‘x,y,dx,dy’
            mouse_scroll = f'{x},{y},{hscroll},{vscroll}' # type: ignore
            commands.append(['mouse', 'scroll', mouse_scroll])

        keyboard_listener = keyboard.Listener(on_press=on_press, on_release=on_release) # type: ignore
        mouse_listener = mouse.Listener(on_move=on_move, on_click=on_click, on_scroll=on_scroll)

        keyboard_listener.start()
        mouse_listener.start()

        # Aguarda o teclado terminar (quando esc for pressionado)
        #keyboard_listener.join()
        # Para o mouse também
        #mouse_listener.stop()
        return True

    @staticmethod
    def create_automation(name: str, description: str = "") -> Optional[int]:
        """Cria nova automação"""
        try:
            automation = Automation(
                name=name,
                description=description,
            )
            return AutomationRepository.create(automation)
        except Exception as e:
            print(f"Erro ao criar automação: {e}")
            return None

    @staticmethod
    def execute_automation(automation_id: int) -> bool:
        """Executar a automação"""
        return True

    @staticmethod
    def update_automation(automation_id: int, **kwargs) -> bool:
        """Atualiza automação"""
        return True

    @staticmethod
    def delete_automation(automation_id: int) -> bool:
        """Deleta automação"""
        return AutomationRepository.delete(automation_id)