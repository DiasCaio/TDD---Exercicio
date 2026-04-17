DELTAS = {
    'w': (0, -1),
    's': (0, 1),
    'a': (-1, 0),
    'd': (1, 0),
}

OPOSTOS = {'w': 's', 's': 'w', 'a': 'd', 'd': 'a'}


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
        self.snake = Snake(inicio)
        self.direcao = direcao_inicial
        self.spawner = spawner
        self.frutas = []
        self.vivo = True
        self._repor_frutas()

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
