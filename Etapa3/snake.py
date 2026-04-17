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

    def passo(self, input_jogador):
        pass
