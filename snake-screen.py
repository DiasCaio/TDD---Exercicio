import os
import sys
import random
import pygame

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "Etapa7"))
from snake import Jogo

TILE = 40
GRID = (20, 15)
LARGURA = TILE * GRID[0]
ALTURA = TILE * GRID[1]
COR_FUNDO = (175, 215, 70)
COR_FUNDO_ESCURA = (167, 209, 61)
COR_GAME_OVER = (40, 40, 40)
GAME_SPEED_MS = 150

GRAPHICS = os.path.join(os.path.dirname(__file__), "Graphics")


def carregar_sprite(nome):
    return pygame.image.load(os.path.join(GRAPHICS, nome)).convert_alpha()


def spawner_aleatorio(ocupadas, dim):
    livres = [(x, y) for y in range(dim[1]) for x in range(dim[0]) if (x, y) not in ocupadas]
    return random.choice(livres)


def desenhar_fundo(tela):
    for y in range(GRID[1]):
        for x in range(GRID[0]):
            cor = COR_FUNDO if (x + y) % 2 == 0 else COR_FUNDO_ESCURA
            pygame.draw.rect(tela, cor, (x * TILE, y * TILE, TILE, TILE))


def desenhar_jogo(tela, jogo, sprites):
    desenhar_fundo(tela)
    for fx, fy in jogo.frutas:
        tela.blit(sprites['apple'], (fx * TILE, fy * TILE))
    for (x, y), nome in jogo.segmentos():
        tela.blit(sprites[nome], (x * TILE, y * TILE))


def desenhar_game_over(tela, jogo, fonte):
    tela.fill(COR_GAME_OVER)
    titulo = fonte.render("GAME OVER", True, (240, 240, 240))
    info = fonte.render(f"Tamanho final: {jogo.snake.tamanho}", True, (200, 200, 200))
    rodape = fonte.render("R: reiniciar    ESC: sair", True, (200, 200, 200))
    tela.blit(titulo, titulo.get_rect(center=(LARGURA // 2, ALTURA // 2 - 60)))
    tela.blit(info, info.get_rect(center=(LARGURA // 2, ALTURA // 2)))
    tela.blit(rodape, rodape.get_rect(center=(LARGURA // 2, ALTURA // 2 + 60)))


TECLAS_DIRECAO = {
    pygame.K_w: 'w', pygame.K_UP: 'w',
    pygame.K_s: 's', pygame.K_DOWN: 's',
    pygame.K_a: 'a', pygame.K_LEFT: 'a',
    pygame.K_d: 'd', pygame.K_RIGHT: 'd',
}


def main():
    pygame.init()
    tela = pygame.display.set_mode((LARGURA, ALTURA))
    pygame.display.set_caption("Snake")
    clock = pygame.time.Clock()
    fonte = pygame.font.SysFont("consolas", 36, bold=True)

    nomes_sprites = [
        'apple',
        'head_up', 'head_down', 'head_left', 'head_right',
        'tail_up', 'tail_down', 'tail_left', 'tail_right',
        'body_horizontal', 'body_vertical',
        'body_topleft', 'body_topright', 'body_bottomleft', 'body_bottomright',
    ]
    sprites = {nome: carregar_sprite(nome + '.png') for nome in nomes_sprites}

    jogo = Jogo(dim=GRID, inicio=(GRID[0] // 2, GRID[1] // 2),
                direcao_inicial='d', spawner=spawner_aleatorio)

    fila_inputs = []
    proximo_tick = pygame.time.get_ticks() + GAME_SPEED_MS

    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                return
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    pygame.quit()
                    return
                if not jogo.vivo and evento.key == pygame.K_r:
                    jogo.reiniciar()
                    fila_inputs.clear()
                elif jogo.vivo and evento.key in TECLAS_DIRECAO:
                    fila_inputs.append(TECLAS_DIRECAO[evento.key])

        agora = pygame.time.get_ticks()
        if agora >= proximo_tick:
            if jogo.vivo:
                entrada = fila_inputs.pop(0) if fila_inputs else None
                jogo.passo(entrada)
            proximo_tick = agora + GAME_SPEED_MS

        if jogo.vivo:
            desenhar_jogo(tela, jogo, sprites)
        else:
            desenhar_game_over(tela, jogo, fonte)
        pygame.display.flip()
        clock.tick(60)


if __name__ == "__main__":
    main()
