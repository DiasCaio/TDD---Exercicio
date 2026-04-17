DELTAS = {
    'w': (0, -1),
    's': (0, 1),
    'a': (-1, 0),
    'd': (1, 0),
}


class Snake:
    def __init__(self, inicio):
        self.corpo = [inicio]

    @property
    def cabeca(self):
        return self.corpo[0]

    @property
    def tamanho(self):
        return len(self.corpo)

    def mover(self, direcao):
        dx, dy = DELTAS[direcao]
        x, y = self.cabeca
        self.corpo.insert(0, (x + dx, y + dy))
        self.corpo.pop()


class Jogo:
    def __init__(self, dim, inicio, direcao_inicial='w', spawner=None):
        self.dim = dim
        self.snake = Snake(inicio)
        self.direcao = direcao_inicial
        self.spawner = spawner
        self.frutas = []
        self._garantir_frutas()

    def _qtd_frutas_alvo(self):
        return 1 + self.snake.tamanho // 10

    def _ocupadas(self):
        return set(self.snake.corpo) | set(self.frutas)

    def _garantir_frutas(self):
        while len(self.frutas) < self._qtd_frutas_alvo():
            self.frutas.append(self.spawner(self._ocupadas(), self.dim))

    def passo(self, input_jogador):
        if input_jogador in DELTAS:
            self.direcao = input_jogador
        dx, dy = DELTAS[self.direcao]
        x, y = self.snake.cabeca
        nova_cabeca = (x + dx, y + dy)
        self.snake.corpo.insert(0, nova_cabeca)
        if nova_cabeca in self.frutas:
            self.frutas.remove(nova_cabeca)
            self._garantir_frutas()
        else:
            self.snake.corpo.pop()
