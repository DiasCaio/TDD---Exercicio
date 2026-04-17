import os
import sys
import random
import keyboard
import time

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "Etapa6"))
from snake import Jogo


class io_handler:

    x_size: int
    y_size: int
    game_speed = float
    last_input: str
    matrix = []

    def __init__(self, dim, speed):
        self.x_size = dim[0]
        self.y_size = dim[1]

        self.game_speed = speed
        self.last_input = 'w'
        self.input_queue = []

        for i in range (self.y_size):
            self.matrix.append([0]*self.x_size)

    def _registrar(self, tecla):
        if tecla in ('w', 'a', 's', 'd'):
            self.input_queue.append(tecla)
        self.last_input = tecla

    def record_inputs(self):
        keyboard.on_press_key('w', lambda e: self._registrar('w'))
        keyboard.on_press_key('a', lambda e: self._registrar('a'))
        keyboard.on_press_key('s', lambda e: self._registrar('s'))
        keyboard.on_press_key('d', lambda e: self._registrar('d'))
        keyboard.on_press_key('r', lambda e: self._registrar('r'))
        keyboard.on_press_key('esc', lambda e: self._registrar('end'))

    def proximo_movimento(self):
        if self.input_queue:
            return self.input_queue.pop(0)
        return None

    def display(self):
        def display_h_line(self):
            print ('+', end='')
            print ('--'* len(self.matrix[0]), end='')
            print ('+')
        
        def display_content_line(line):
            print ('|', end='')
            for item in line: 
                if item == 1:
                    print ('[]', end='')
                elif item == 2:
                    print ('<>', end='')
                elif item == 3:
                    print ('()', end='')
                else:
                    print ('  ', end='')

            print ('|')

        os.system('cls' if os.name == 'nt' else 'clear')
        display_h_line(self)
        for line in self.matrix:
            display_content_line(line)
        display_h_line(self)

instance = io_handler((20, 10), 0.15)

def spawner_aleatorio(ocupadas, dim):
    livres = [(x, y) for y in range(dim[1]) for x in range(dim[0]) if (x, y) not in ocupadas]
    return random.choice(livres)

jogo = Jogo(dim=(20, 10), inicio=(5, 5), direcao_inicial='d', spawner=spawner_aleatorio)

def desenhar():
    for y in range(len(instance.matrix)):
        for x in range(len(instance.matrix[0])):
            instance.matrix[y][x] = 0
    for fx, fy in jogo.frutas:
        if 0 <= fy < len(instance.matrix) and 0 <= fx < len(instance.matrix[0]):
            instance.matrix[fy][fx] = 3
    for i, (x, y) in enumerate(jogo.snake.corpo):
        if 0 <= y < len(instance.matrix) and 0 <= x < len(instance.matrix[0]):
            instance.matrix[y][x] = 2 if i == 0 else 1

def desenhar_game_over():
    for y in range(len(instance.matrix)):
        for x in range(len(instance.matrix[0])):
            instance.matrix[y][x] = 1

def tela_jogando():
    desenhar()
    instance.display()
    print("mova com WASD, saia com esc. Tamanho:", jogo.snake.tamanho,
          " Direcao:", jogo.direcao)

def tela_game_over():
    desenhar_game_over()
    instance.display()
    print()
    print("  ======================================")
    print("            G A M E   O V E R           ")
    print(f"            Tamanho final: {jogo.snake.tamanho}")
    print("         R: reiniciar  |  ESC: sair     ")
    print("  ======================================")

def game_loop():
    instance.record_inputs()
    while True:
        if jogo.vivo:
            tela_jogando()
            jogo.passo(instance.proximo_movimento())
        else:
            tela_game_over()
            if instance.last_input == 'r':
                jogo.reiniciar()
                instance.input_queue.clear()
                instance.last_input = jogo.direcao

        if instance.last_input == 'end':
            return
        time.sleep(instance.game_speed)

game_loop()