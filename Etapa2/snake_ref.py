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
