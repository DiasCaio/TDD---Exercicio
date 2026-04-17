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
        x, y = self.cabeca
        if direcao == 'd':
            nova = (x + 1, y)
        elif direcao == 'a':
            nova = (x - 1, y)
        elif direcao == 'w':
            nova = (x, y - 1)
        elif direcao == 's':
            nova = (x, y + 1)
        self.corpo.insert(0, nova)
        self.corpo.pop()
