from snake import Jogo


def spawner_fixo(posicoes):
    it = iter(posicoes)

    def _spawn(ocupadas, dim):
        return next(it)
    return _spawn


def test_jogo_novo_esta_vivo():
    jogo = Jogo(dim=(20, 10), inicio=(5, 5), spawner=spawner_fixo([(9, 9)]))
    assert jogo.vivo is True


def test_cobra_tamanho_1_nao_morre_sozinha():
    jogo = Jogo(dim=(20, 10), inicio=(5, 5), direcao_inicial='d',
                spawner=spawner_fixo([(9, 9)]))
    for _ in range(3):
        jogo.passo(None)
    assert jogo.vivo is True


def test_colidir_com_proprio_corpo_mata():
    # cobra cresce ate tamanho 5 indo pra direita, depois faz um U
    # posicoes 1..4: frutas em linha reta
    frutas_iniciais = [(6, 5), (7, 5), (8, 5), (9, 5), (99, 99)]
    jogo = Jogo(dim=(20, 10), inicio=(5, 5), direcao_inicial='d',
                spawner=spawner_fixo(frutas_iniciais))
    for _ in range(4):
        jogo.passo(None)  # come 4 frutas, tamanho=5, cabeca em (9,5)
    # corpo: [(9,5), (8,5), (7,5), (6,5), (5,5)]
    jogo.passo('s')  # (9, 6)
    jogo.passo('a')  # (8, 6)
    jogo.passo('w')  # (8, 5) <- colide com corpo
    assert jogo.vivo is False


def test_passo_apos_game_over_nao_altera_estado():
    frutas_iniciais = [(6, 5), (7, 5), (8, 5), (9, 5), (99, 99)]
    jogo = Jogo(dim=(20, 10), inicio=(5, 5), direcao_inicial='d',
                spawner=spawner_fixo(frutas_iniciais))
    for _ in range(4):
        jogo.passo(None)
    jogo.passo('s')
    jogo.passo('a')
    jogo.passo('w')
    corpo_congelado = list(jogo.snake.corpo)
    jogo.passo('d')
    jogo.passo('s')
    assert jogo.snake.corpo == corpo_congelado
    assert jogo.vivo is False


def test_cobra_retilinea_com_tamanho_igual_a_dimensao_nao_morre_no_wrap():
    # grid 3x3; cobra cresce verticalmente ate ocupar a coluna 0 inteira (tamanho 3)
    jogo = Jogo(dim=(3, 3), inicio=(0, 2), direcao_inicial='w',
                spawner=spawner_fixo([(0, 1), (0, 0), (2, 2)]))
    jogo.passo(None)  # come (0,1)
    jogo.passo(None)  # come (0,0); corpo=[(0,0),(0,1),(0,2)], tamanho=3=altura
    jogo.passo(None)  # wrap: alvo=(0,2); era a cauda, escapa no mesmo tick
    assert jogo.vivo is True


def test_cobra_dobrada_com_tamanho_dim_mais_1_morre_no_wrap():
    # grid 3x3; cobra em L com tamanho 4 = largura+1, bate no corpo ao dar wrap
    jogo = Jogo(dim=(3, 3), inicio=(0, 1), direcao_inicial='w',
                spawner=spawner_fixo([(0, 0), (1, 0), (2, 0), (2, 2)]))
    jogo.passo(None)  # come (0,0); corpo=[(0,0),(0,1)]
    jogo.passo('d')   # come (1,0); corpo=[(1,0),(0,0),(0,1)]
    jogo.passo(None)  # come (2,0); corpo=[(2,0),(1,0),(0,0),(0,1)], tamanho=4=dim_x+1
    jogo.passo(None)  # alvo=(3,0)%3=(0,0); (0,0) esta no meio do corpo (nao e cauda)
    assert jogo.vivo is False


def test_cabeca_entrando_na_antiga_cauda_nao_morre():
    # com tamanho 2+, a cauda sai da celula no mesmo tick em que a cabeca entra.
    # montamos cobra de tamanho 2 e fazemos a cabeca cair onde estava a cauda.
    # cobra come 1 fruta indo 'd': corpo = [(6,5),(5,5)], tamanho=2
    # depois giramos: 's' -> (6,6), 'a' -> (5,6), 'w' -> (5,5) == antiga cauda => nao morre
    jogo = Jogo(dim=(20, 10), inicio=(5, 5), direcao_inicial='d',
                spawner=spawner_fixo([(6, 5), (99, 99)]))
    jogo.passo(None)  # come (6,5), corpo=[(6,5),(5,5)]
    jogo.passo('s')
    jogo.passo('a')
    jogo.passo('w')
    assert jogo.vivo is True
