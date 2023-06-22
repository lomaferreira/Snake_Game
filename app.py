import pygame  # importa a biblioteca
# importa do sub modulo locals todas as funções e constantes
from pygame.locals import *
# importa do modulo sys a função exit(fecha a janela do jogo)
from sys import exit
from random import randint  # importa a funçao randint(sortea valores)

pygame.init()  # inicializa todas as funções e variaveis


largura = 640
altura = 480
# controlam o movimento dos objetos(ta no centro(n exatamente))
x_cobra = int(largura/2)
y_cobra = int(altura/2)

velocidade = 7
x_controle = velocidade
y_controle = 0

# posições de escolha pra x, desconsiderando a altura do retangulo pra n sair da tela
x_maca = randint(40, 600)
y_maca = randint(50, 430)


pontos = 0
# pygame.font.get_fonts() ver as fontes disponiveis
fonte = pygame.font.SysFont('arial', 40, True, True)


relogio = pygame.time.Clock()  # velocidade do movimento

# cria um objeto que vai ser a tela largura=640 e h=480
tela = pygame.display.set_mode((largura, altura))
pygame.display.set_caption("Game")  # muda o nome da janela


# Guarda as posições anteriores da cobra que estão na lista_cabeca
lista_cobra = []
comprimento_inicial = 5

morreu = False


def aumenta_cobra(lista_cobra):
    # para cada posição x e y anterior desenha um retangulo
    for XeY in lista_cobra:
        # XeY = [x,y]
        # XeY[0]= x
        # XeY[1]=Y
        pygame.draw.rect(tela, (0, 255, 0), (XeY[0], XeY[1], 20, 20))


def reiniciar_jogo():
    # as variaveis se tornam globais
    global pontos, comprimento_inicial, x_cobra, y_cobra, lista_cobra, lista_cabeca, x_maca, y_maca, morreu
    pontos = 0
    comprimento_inicial = 5
    x_cobra = int(largura/2)
    y_cobra = int(altura/2)
    lista_cobra = []
    lista_cabeca = []
    x_maca = randint(40, 600)
    y_maca = randint(50, 430)
    morreu = False


while True:
    # preenche a tela da cor preta a cada interação(n ver a prolongação do movimento )
    tela.fill((255, 255, 255))
    relogio.tick(30)

    mensagem = f"Pontos:{pontos}"

    # uni a msg e a fonte(mensagem, false=maisPixelado)
    texto_formatado = fonte.render(mensagem, True, (0, 0, 0))

    # detecta se algum evento ocorreu
    for event in pygame.event.get():
        # testa se o evento fechar a janela do jogo ocorreu
        if event.type == QUIT:
            pygame.quit()
            exit()
        # testa os  eventos do teclado para cada tecla
        if event.type == KEYDOWN:
            # Faz a cobra andar e bloquear a tecla K_d quando a K_a for pressionada
            if event.key == K_a and x_controle != velocidade:
                x_controle = -velocidade
                y_controle = 0
            if event.key == K_d and x_controle != -velocidade:
                x_controle = velocidade
                y_controle = 0
            if event.key == K_w and y_controle != velocidade:
                y_controle = -velocidade
                x_controle = 0
            if event.key == K_s and y_controle != -velocidade:
                y_controle = velocidade
                x_controle = 0

    # Add a posição inicial da cobra mais o key do teclado
    x_cobra += x_controle
    y_cobra += y_controle

    cobra = pygame.draw.rect(tela, (0, 240, 0), (x_cobra, y_cobra, 20, 20))
    maca = pygame.draw.rect(tela, (255, 0, 0), (x_maca, y_maca, 20, 20))

    # Colisão da cobra com a maçã
    if cobra.colliderect(maca):
        x_maca = randint(40, 600)
        y_maca = randint(50, 430)
        pontos += 1
       # cobra cresce
        comprimento_inicial += 1

    # posição atual da cobra, muda a cada interação
    lista_cabeca = []
    lista_cabeca.append(x_cobra)
    lista_cabeca.append(y_cobra)

    lista_cobra.append(lista_cabeca)

    # Condição pra cobra morrer(quando lista_cabeca ocupa um lugar  ja existente em lista_cobra)
    if lista_cobra.count(lista_cabeca) > 1:
        fonte2 = pygame.font.SysFont('arial', 20, True, True,)
        mensagem = 'Game over! Pressione a tecla R para jogar novamente'
        texto_formatado = fonte2.render(mensagem, True, (0, 0, 0))
        # colocar o texto n meio da tela
        ret_texto = texto_formatado.get_rect()
        morreu = True
        while morreu:
            tela.fill((255, 255, 255))

            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    exit()
                if event.type == KEYDOWN:
                    if event.key == K_r:
                        reiniciar_jogo()
            ret_texto.center = (largura//2, altura//2)
            tela.blit(texto_formatado, ret_texto)
            pygame.display.update()
    # Quando a cobra sair da tela voltar pelo outro lado
    if x_cobra > largura:
        x_cobra = 0
    if x_cobra < 0:
        x_cobra == largura
    if y_cobra < 0:
        y_cobra = altura
    if y_cobra > altura:
        y_cobra = 0
    # Deleta a cauda da cobra(primeiro elemento da matriz) quando ele for maior que 5
    if len(lista_cobra) > comprimento_inicial:
        del lista_cobra[0]

    aumenta_cobra(lista_cobra)

    tela.blit(texto_formatado, (450, 440))
    pygame.display.update()
