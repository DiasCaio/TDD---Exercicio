from snake import Jogo


def spawner_fixo(posicoes):
    it = iter(posicoes)

    def _spawn(ocupadas, dim):
        return next(it)
    return _spawn


# --- bloqueio 180 graus ---
def test_ignora_input_oposto_a_direcao_atual():
    jogo = Jogo(dim=(20, 10), inicio=(5, 5), direcao_inicial='d',
                spawner=spawner_fixo([(9, 9)]))
    jogo.passo('a')
    assert jogo.direcao == 'd'
    assert jogo.snake.cabeca == (6, 5)


def test_ignora_180_em_cada_eixo():
    casos = [('w', 's'), ('s', 'w'), ('a', 'd'), ('d', 'a')]
    for direcao, oposta in casos:
        jogo = Jogo(dim=(20, 10), inicio=(5, 5), direcao_inicial=direcao,
                    spawner=spawner_fixo([(9, 9)]))
        jogo.passo(oposta)
        assert jogo.direcao == direcao


# --- wrap-around ---
def test_wrap_pela_direita():
    jogo = Jogo(dim=(10, 10), inicio=(9, 5), direcao_inicial='d',
                spawner=spawner_fixo([(1, 1)]))
    jogo.passo(None)
    assert jogo.snake.cabeca == (0, 5)


def test_wrap_pela_esquerda():
    jogo = Jogo(dim=(10, 10), inicio=(0, 5), direcao_inicial='a',
                spawner=spawner_fixo([(1, 1)]))
    jogo.passo(None)
    assert jogo.snake.cabeca == (9, 5)


def test_wrap_pelo_topo():
    jogo = Jogo(dim=(10, 8), inicio=(4, 0), direcao_inicial='w',
                spawner=spawner_fixo([(1, 1)]))
    jogo.passo(None)
    assert jogo.snake.cabeca == (4, 7)


def test_wrap_pelo_fundo():
    jogo = Jogo(dim=(10, 8), inicio=(4, 7), direcao_inicial='s',
                spawner=spawner_fixo([(1, 1)]))
    jogo.passo(None)
    assert jogo.snake.cabeca == (4, 0)
