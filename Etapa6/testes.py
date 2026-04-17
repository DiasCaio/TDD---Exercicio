from snake import Jogo


def spawner_fixo(posicoes):
    it = iter(posicoes)

    def _spawn(ocupadas, dim):
        return next(it)
    return _spawn


def test_reiniciar_restaura_vivo():
    frutas = [(6, 5), (7, 5), (8, 5), (9, 5), (9, 9), (1, 1)]
    jogo = Jogo(dim=(20, 10), inicio=(5, 5), direcao_inicial='d',
                spawner=spawner_fixo(frutas))
    for _ in range(4):
        jogo.passo(None)
    jogo.passo('s'); jogo.passo('a'); jogo.passo('w')
    assert jogo.vivo is False
    jogo.reiniciar()
    assert jogo.vivo is True


def test_reiniciar_volta_cobra_ao_estado_inicial():
    frutas = [(6, 5), (7, 5), (8, 5), (9, 5), (9, 9), (1, 1)]
    jogo = Jogo(dim=(20, 10), inicio=(5, 5), direcao_inicial='d',
                spawner=spawner_fixo(frutas))
    for _ in range(4):
        jogo.passo(None)
    jogo.reiniciar()
    assert jogo.snake.corpo == [(5, 5)]
    assert jogo.snake.tamanho == 1


def test_reiniciar_restaura_direcao_inicial():
    jogo = Jogo(dim=(20, 10), inicio=(5, 5), direcao_inicial='d',
                spawner=spawner_fixo([(9, 9), (2, 2)]))
    jogo.passo('s')
    assert jogo.direcao == 's'
    jogo.reiniciar()
    assert jogo.direcao == 'd'


def test_reiniciar_respawna_apenas_uma_fruta():
    jogo = Jogo(dim=(20, 10), inicio=(5, 5), direcao_inicial='d',
                spawner=spawner_fixo([(1, 1), (2, 2)]))
    jogo.reiniciar()
    assert len(jogo.frutas) == 1


def test_passo_funciona_apos_reiniciar():
    frutas = [(6, 5), (7, 5), (8, 5), (9, 5), (9, 9), (1, 1)]
    jogo = Jogo(dim=(20, 10), inicio=(5, 5), direcao_inicial='d',
                spawner=spawner_fixo(frutas))
    for _ in range(4):
        jogo.passo(None)
    jogo.passo('s'); jogo.passo('a'); jogo.passo('w')
    jogo.reiniciar()
    jogo.passo(None)
    assert jogo.snake.cabeca == (6, 5)
    assert jogo.vivo is True
