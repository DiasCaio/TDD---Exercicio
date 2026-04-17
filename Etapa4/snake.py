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

    def mover(self, direcao):
        self.corpo.insert(0, self.proxima_cabeca(direcao))
        self.corpo.pop()

    def crescer(self, direcao):
        self.corpo.insert(0, self.proxima_cabeca(direcao))


class Jogo:
    def __init__(self, dim, inicio, direcao_inicial='w', spawner=None):
        self.dim = dim
        self.snake = Snake(inicio)
        self.direcao = direcao_inicial
        self.spawner = spawner
        self.frutas = []
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

    def _alvo(self):
        dx, dy = DELTAS[self.direcao]
        x, y = self.snake.cabeca
        return ((x + dx) % self.dim[0], (y + dy) % self.dim[1])

    def passo(self, input_jogador):
        self._atualizar_direcao(input_jogador)
        alvo = self._alvo()
        self.snake.corpo.insert(0, alvo)
        if alvo in self.frutas:
            self.frutas.remove(alvo)
            self._repor_frutas()
        else:
            self.snake.corpo.pop()
