from snake import Snake


def test_mover_direita_incrementa_x():
    s = Snake((5, 5))
    s.mover('d')
    assert s.cabeca == (6, 5)


def test_mover_esquerda_decrementa_x():
    s = Snake((5, 5))
    s.mover('a')
    assert s.cabeca == (4, 5)


def test_mover_cima_decrementa_y():
    s = Snake((5, 5))
    s.mover('w')
    assert s.cabeca == (5, 4)


def test_mover_baixo_incrementa_y():
    s = Snake((5, 5))
    s.mover('s')
    assert s.cabeca == (5, 6)


def test_mover_mantem_tamanho():
    s = Snake((5, 5))
    s.mover('d')
    assert s.tamanho == 1
