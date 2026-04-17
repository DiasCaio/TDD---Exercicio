from snake import Snake


def test_snake_inicial_tem_corpo_na_posicao_dada():
    snake = Snake(inicio=(5, 5))
    assert snake.corpo == [(5, 5)]


def test_snake_comeca_com_tamanho_1():
    snake = Snake(inicio=(3, 2))
    assert len(snake.corpo) == 1


def test_snake_cabeca_e_primeira_posicao_do_corpo():
    snake = Snake(inicio=(7, 4))
    assert snake.cabeca == (7, 4)
