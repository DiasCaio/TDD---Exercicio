from snake import Jogo


def spawner_fixo(posicoes):
    it = iter(posicoes)

    def _spawn(ocupadas, dim):
        return next(it)
    return _spawn


def test_cobra_tamanho_1_so_tem_cabeca_na_direcao_atual():
    jogo = Jogo(dim=(20, 10), inicio=(5, 5), direcao_inicial='d',
                spawner=spawner_fixo([(9, 9)]))
    assert jogo.segmentos() == [((5, 5), 'head_right')]


def test_cabeca_acompanha_direcao_atual():
    casos = {'d': 'head_right', 'a': 'head_left', 'w': 'head_up', 's': 'head_down'}
    for direcao, sprite in casos.items():
        jogo = Jogo(dim=(20, 10), inicio=(5, 5), direcao_inicial=direcao,
                    spawner=spawner_fixo([(9, 9)]))
        assert jogo.segmentos()[0] == ((5, 5), sprite)


def test_cobra_horizontal_indo_direita():
    # corpo: cabeca em (7,5), corpos em (6,5) e (5,5), cauda em (4,5)
    frutas = [(6, 5), (7, 5), (9, 9)]
    jogo = Jogo(dim=(20, 10), inicio=(5, 5), direcao_inicial='d',
                spawner=spawner_fixo(frutas))
    jogo.passo(None)  # come (6,5); corpo=[(6,5),(5,5)]
    jogo.passo(None)  # come (7,5); corpo=[(7,5),(6,5),(5,5)]
    segs = jogo.segmentos()
    assert segs[0] == ((7, 5), 'head_right')
    assert segs[1] == ((6, 5), 'body_horizontal')
    assert segs[2] == ((5, 5), 'tail_left')


def test_cobra_vertical_indo_baixo():
    frutas = [(5, 6), (5, 7), (9, 9)]
    jogo = Jogo(dim=(20, 10), inicio=(5, 5), direcao_inicial='s',
                spawner=spawner_fixo(frutas))
    jogo.passo(None)
    jogo.passo(None)
    segs = jogo.segmentos()
    assert segs[0] == ((5, 7), 'head_down')
    assert segs[1] == ((5, 6), 'body_vertical')
    assert segs[2] == ((5, 5), 'tail_up')


def test_curva_topleft_segmento_com_vizinhos_acima_e_esquerda():
    # cobra cresce: (5,5) -> (6,5) -> (6,4); curva no (6,5) com vizinhos acima e esquerda
    frutas = [(6, 5), (6, 4), (9, 9)]
    jogo = Jogo(dim=(20, 10), inicio=(5, 5), direcao_inicial='d',
                spawner=spawner_fixo(frutas))
    jogo.passo(None)        # come (6,5); corpo=[(6,5),(5,5)]
    jogo.passo('w')         # come (6,4); corpo=[(6,4),(6,5),(5,5)]
    segs = jogo.segmentos()
    assert segs[0] == ((6, 4), 'head_up')
    assert segs[1] == ((6, 5), 'body_topleft')
    assert segs[2] == ((5, 5), 'tail_left')


def test_curva_bottomright_segmento_com_vizinhos_abaixo_e_direita():
    # (5,5) -> (4,5) -> (4,6); no (4,5) vizinhos sao a direita (5,5) e abaixo (4,6)
    frutas = [(4, 5), (4, 6), (9, 9)]
    jogo = Jogo(dim=(20, 10), inicio=(5, 5), direcao_inicial='a',
                spawner=spawner_fixo(frutas))
    jogo.passo(None)
    jogo.passo('s')
    segs = jogo.segmentos()
    assert segs[0] == ((4, 6), 'head_down')
    assert segs[1] == ((4, 5), 'body_bottomright')
    assert segs[2] == ((5, 5), 'tail_right')


def test_segmentos_lida_com_wrap():
    # cobra grande o suficiente pra cruzar a borda direita-esquerda
    frutas = [(0, 0), (1, 0), (9, 9)]
    jogo = Jogo(dim=(3, 3), inicio=(2, 0), direcao_inicial='d',
                spawner=spawner_fixo(frutas))
    jogo.passo(None)        # come (0,0); corpo=[(0,0),(2,0)]
    jogo.passo(None)        # come (1,0); corpo=[(1,0),(0,0),(2,0)]
    segs = jogo.segmentos()
    # cobra horizontal indo 'd', mesmo com wrap entre (2,0) e (0,0)
    assert segs[0] == ((1, 0), 'head_right')
    assert segs[1] == ((0, 0), 'body_horizontal')
    assert segs[2] == ((2, 0), 'tail_left')
