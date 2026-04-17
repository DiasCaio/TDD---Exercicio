from snake import Jogo


def spawner_fixo(posicoes):
    it = iter(posicoes)

    def _spawn(ocupadas, dim):
        return next(it)
    return _spawn


def test_jogo_inicia_com_uma_fruta():
    jogo = Jogo(dim=(10, 10), inicio=(5, 5), spawner=spawner_fixo([(1, 1)]))
    assert len(jogo.frutas) == 1


def test_fruta_inicial_na_posicao_do_spawner():
    jogo = Jogo(dim=(10, 10), inicio=(5, 5), spawner=spawner_fixo([(3, 4)]))
    assert jogo.frutas == [(3, 4)]


def test_passo_sem_comer_mantem_tamanho_1():
    jogo = Jogo(dim=(10, 10), inicio=(5, 5),
                direcao_inicial='d', spawner=spawner_fixo([(1, 1), (2, 2)]))
    jogo.passo(None)
    assert jogo.snake.tamanho == 1


def test_snake_cresce_ao_comer_fruta():
    jogo = Jogo(dim=(10, 10), inicio=(5, 5),
                direcao_inicial='d', spawner=spawner_fixo([(6, 5), (9, 9)]))
    jogo.passo(None)
    assert jogo.snake.tamanho == 2


def test_fruta_comida_eh_substituida():
    jogo = Jogo(dim=(10, 10), inicio=(5, 5),
                direcao_inicial='d', spawner=spawner_fixo([(6, 5), (8, 8)]))
    jogo.passo(None)
    assert jogo.frutas == [(8, 8)]


def test_tamanho_10_gera_duas_frutas():
    posicoes = [(6 + i, 5) for i in range(11)]
    jogo = Jogo(dim=(50, 10), inicio=(5, 5),
                direcao_inicial='d', spawner=spawner_fixo(posicoes))
    for _ in range(9):
        jogo.passo(None)
    assert jogo.snake.tamanho == 10
    assert len(jogo.frutas) == 2


def test_tamanho_20_gera_tres_frutas():
    posicoes = [(6 + i, 5) for i in range(22)]
    jogo = Jogo(dim=(50, 10), inicio=(5, 5),
                direcao_inicial='d', spawner=spawner_fixo(posicoes))
    for _ in range(19):
        jogo.passo(None)
    assert jogo.snake.tamanho == 20
    assert len(jogo.frutas) == 3
