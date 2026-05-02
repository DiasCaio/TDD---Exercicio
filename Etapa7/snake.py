DELTAS = {
    'w': (0, -1),
    's': (0, 1),
    'a': (-1, 0),
    'd': (1, 0),
}

OPOSTOS = {'w': 's', 's': 'w', 'a': 'd', 'd': 'a'}

DIR_PARA_NOME = {'w': 'up', 's': 'down', 'a': 'left', 'd': 'right'}


class Snake:
    def __init__(self, inicio):
        self.corpo = [inicio]

    @property
    def cabeca(self):
        return self.corpo[0]

    @property
    def tamanho(self):
        return len(self.corpo)

    def proxima_cabeca(self, direcao):
        dx, dy = DELTAS[direcao]
        x, y = self.cabeca
        return (x + dx, y + dy)

    def colidiria_em(self, pos):
        return pos in self.corpo[:-1]

    def mover_para(self, pos):
        self.corpo.insert(0, pos)
        self.corpo.pop()

    def crescer_para(self, pos):
        self.corpo.insert(0, pos)


class Jogo:
    def __init__(self, dim, inicio, direcao_inicial='w', spawner=None):
        self.dim = dim
        self.inicio = inicio
        self.direcao_inicial = direcao_inicial
        self.spawner = spawner
        self.reiniciar()

    def reiniciar(self):
        self.snake = Snake(self.inicio)
        self.direcao = self.direcao_inicial
        self.frutas = []
        self.vivo = True
        self._repor_frutas()

    def segmentos(self):
        corpo = self.snake.corpo
        out = []
        out.append((corpo[0], 'head_' + DIR_PARA_NOME[self.direcao]))
        for i in range(1, len(corpo) - 1):
            anterior = corpo[i - 1]
            seguinte = corpo[i + 1]
            out.append((corpo[i], self._sprite_meio(corpo[i], anterior, seguinte)))
        if len(corpo) >= 2:
            cauda, vizinho = corpo[-1], corpo[-2]
            out.append((cauda, self._sprite_cauda(cauda, vizinho)))
        return out

    def _delta(self, origem, destino):
        dx = destino[0] - origem[0]
        dy = destino[1] - origem[1]
        if dx > self.dim[0] / 2: dx -= self.dim[0]
        elif dx < -self.dim[0] / 2: dx += self.dim[0]
        if dy > self.dim[1] / 2: dy -= self.dim[1]
        elif dy < -self.dim[1] / 2: dy += self.dim[1]
        return (dx, dy)

    def _sprite_cauda(self, cauda, vizinho):
        dx, dy = self._delta(cauda, vizinho)
        if dx > 0: return 'tail_left'
        if dx < 0: return 'tail_right'
        if dy > 0: return 'tail_up'
        return 'tail_down'

    def _sprite_meio(self, atual, anterior, seguinte):
        ax, ay = self._delta(atual, anterior)
        sx, sy = self._delta(atual, seguinte)
        if ay == 0 and sy == 0:
            return 'body_horizontal'
        if ax == 0 and sx == 0:
            return 'body_vertical'
        tem_cima = ay < 0 or sy < 0
        tem_esquerda = ax < 0 or sx < 0
        if tem_cima and tem_esquerda: return 'body_topleft'
        if tem_cima: return 'body_topright'
        if tem_esquerda: return 'body_bottomleft'
        return 'body_bottomright'

    def passo(self, input_jogador):
        if not self.vivo:
            return
        self._atualizar_direcao(input_jogador)
        alvo = self._com_wrap(self.snake.proxima_cabeca(self.direcao))
        if alvo in self.frutas:
            self._consumir_fruta(alvo)
        elif self.snake.colidiria_em(alvo):
            self.vivo = False
        else:
            self.snake.mover_para(alvo)

    def _qtd_alvo(self):
        return 1 + self.snake.tamanho // 10

    def _ocupadas(self):
        return set(self.snake.corpo) | set(self.frutas)

    def _repor_frutas(self):
        while len(self.frutas) < self._qtd_alvo():
            self.frutas.append(self.spawner(self._ocupadas(), self.dim))

    def _atualizar_direcao(self, entrada):
        if entrada in DELTAS and entrada != OPOSTOS[self.direcao]:
            self.direcao = entrada

    def _com_wrap(self, pos):
        x, y = pos
        return (x % self.dim[0], y % self.dim[1])

    def _consumir_fruta(self, alvo):
        self.frutas.remove(alvo)
        self.snake.crescer_para(alvo)
        self._repor_frutas()
