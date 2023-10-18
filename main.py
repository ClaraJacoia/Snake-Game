import pygame
import random
from time import sleep

pygame.init()
pygame.display.set_caption("Jogo da cobrinha")
largura, altura = 1000, 700
tela = pygame.display.set_mode((largura, altura))
relogio = pygame.time.Clock()
fonte = pygame.font.Font(None, 36)

# cores
azul = (0,191,255)
branca = (255, 255, 255)
vermelho = (255, 0, 0)
verde = (0, 255, 0)
rosa = (255, 105, 180)
preta = (0, 0, 0)

# carregamento das imagens
cabeca_cobra = pygame.image.load("C:\\Snake-Game\\imagens\\cabeca_cobra.png")
corpo_cobra = pygame.image.load("C:\\Snake-Game\\imagens\\corpo_cobra.png")
cauda_cobra = pygame.image.load("C:\\Snake-Game\\imagens\\cauda_cobra.png")
comida = pygame.image.load("C:\\Snake-Game\\imagens\\nemo.png")
boost = pygame.transform.scale(pygame.image.load("C:\\Snake-Game\\imagens\\raio.png"), (30, 30))
anzol = pygame.transform.scale(pygame.image.load("C:\\Snake-Game\\imagens\\anzol.png"), (25, 25))

# parametros do jogo
velocidade_jogo = 10
tamanho_quadrado = 25

def tela_inicial():
    texto_titulo = fonte.render("Jogo da Cobrinha", True, rosa)
    tela.blit(texto_titulo, (largura // 2 - texto_titulo.get_width() // 2, 100))
    # Instruções
    texto_titulo = fonte.render("Use WASD para mover a Cobrinha", True, azul)
    tela.blit(texto_titulo, (largura // 2 - texto_titulo.get_width() // 2, 150))
    texto_titulo = fonte.render("Coma os nemos e fuja das paredes e de você mesmo", True, azul)
    tela.blit(texto_titulo, (largura // 2 - texto_titulo.get_width() // 2, 200))
    texto_titulo = fonte.render("O raio te deixa mais rápido mas te dá o dobro de pontos", True, azul)
    tela.blit(texto_titulo, (largura // 2 - texto_titulo.get_width() // 2, 250))
    texto_titulo = fonte.render("Use com cautela!", True, azul)
    tela.blit(texto_titulo, (largura // 2 - texto_titulo.get_width() // 2, 300))
    texto_instrucoes = fonte.render("Pressione ESPAÇO para começar", True, branca)
    tela.blit(texto_instrucoes, (largura // 2 - texto_instrucoes.get_width() // 2, 500))

    pygame.display.update()

    aguardando_inicio = True
    while aguardando_inicio:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                quit()
            if evento.type == pygame.KEYDOWN and evento.key == pygame.K_SPACE:
                aguardando_inicio = False


def tela_final(pontuacao):  
    tela.fill(preta)
    texto_titulo = fonte.render("Game Over", True, rosa)
    tela.blit(texto_titulo, (largura // 2 - texto_titulo.get_width() // 2, 100))
    texto_titulo = fonte.render(f"Pontos: {pontuacao}", True, azul)
    tela.blit(texto_titulo, (largura // 2 - texto_titulo.get_width() // 2, 150))
    # Novo jogo
    jogar_de_novo = fonte.render("Pressione ESPAÇO para jogar novamente", True, branca)
    tela.blit(jogar_de_novo, (largura // 3 - texto_titulo.get_width() // 1.6, 450))
    # Sair do jogo
    sair_jogo = fonte.render("Pressione ESC para sair do jogo", True, branca)
    tela.blit(sair_jogo, (largura // 3 - texto_titulo.get_width() // 6, 500))

    pygame.display.update()

    aguardando_escolha = True
    while aguardando_escolha:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                quit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_SPACE:
                    aguardando_escolha = False
                    # O jogador escolheu jogar novamente
                    pontuacao = rodar_jogo()
                    tela_final(pontuacao)

                elif evento.key == pygame.K_ESCAPE:
                    pygame.quit()
                    quit()

def gerar_comida():
    posicao_x_comida = round(random.randrange(40, largura - tamanho_quadrado + 15) / float(tamanho_quadrado)) * float(
        tamanho_quadrado)
    posicao_y_comida = round(random.randrange(40, altura - tamanho_quadrado + 15) / float(tamanho_quadrado)) * float(
        tamanho_quadrado)
    return posicao_x_comida, posicao_y_comida

def gerar_boost():
    posicao_x_boost = round(random.randrange(40, largura - tamanho_quadrado + 15) / float(tamanho_quadrado)) * float(
        tamanho_quadrado)
    posicao_y_boost = round(random.randrange(40, altura - tamanho_quadrado + 15) / float(tamanho_quadrado)) * float(
        tamanho_quadrado)
    return posicao_x_boost, posicao_y_boost

def gerar_anzol():
    posicao_x_anzol = 300
    posicao_y_anzol = 400
    return posicao_x_anzol, posicao_y_anzol

def desenhar_cobra(pixels, corpo_cobra):
    tela.blit(cauda_cobra, [pixels[0][0], pixels[0][1]])
    pixels_invertidos = pixels[::-1]
    # desenha o corpo da cobra
    for pixel in pixels_invertidos[1:]:
        tela.blit(corpo_cobra, [pixel[0], pixel[1]])
    # desenha a cabeça da cobra por último
    tela.blit(cabeca_cobra, [pixels_invertidos[0][0], pixels_invertidos[0][1]])

def desenhar_comida(comida, posicao_x_comida, posicao_y_comida):
    tela.blit(comida, [posicao_x_comida, posicao_y_comida])

def desenhar_boost(boost, posicao_x_boost, posicao_y_boost):
    tela.blit(boost, [posicao_x_boost, posicao_y_boost])

def desenhar_anzol(anzol, posicao_x_anzol, posicao_y_anzol):
    tela.blit(anzol, [posicao_x_anzol, posicao_y_anzol])

def selecionar_velocidade(tecla):
    velocidade_x = 0
    velocidade_y = 0

    if tecla == pygame.K_s:
        posicao_atual = "Baixo"
        velocidade_x = 0
        velocidade_y = tamanho_quadrado
    if tecla == pygame.K_w:
        posicao_atual = "Alto"
        velocidade_x = 0
        velocidade_y = -tamanho_quadrado
    if tecla == pygame.K_d:
        posicao_atual = "Direita"
        velocidade_x = tamanho_quadrado
        velocidade_y = 0
    if tecla == pygame.K_a:
        velocidade_x = -tamanho_quadrado
        velocidade_y = 0

    return velocidade_x, velocidade_y

def desenhar_pontuacao(pontuacao):
    fonte = pygame.font.SysFont("Consolas", 35, 1)
    texto = fonte.render(f"Pontos: {pontuacao}", True, (25,25,112))
    tela.blit(texto, [1, 1])

def mostra_temporizador(tempo_boost):
    fonte = pygame.font.SysFont("Consolas", 35, 1)
    texto = fonte.render(f"Boost: {tempo_boost + 1}", True, (25,25,112))
    tela.blit(texto, (0, 40))

def rodar_jogo():
    fim_jogo = False
    global velocidade_jogo
    global pontuacao
    global tamanho_cobra
    pontuacao = 0
    x = largura / 2
    y = altura / 2

    velocidade_x = 0
    velocidade_y = 0


    tamanho_cobra = 1
    fase = 1
    
    # variaveis para o controle do boost
    count_boost = 1
    boost_ativo = 0
    duracao_boost = 3000

    pixels = [[largura / 2, altura / 2], [largura / 2 - tamanho_quadrado, altura / 2]]

    posicao_x_comida, posicao_y_comida = gerar_comida()
    posicao_x_boost, posicao_y_boost = gerar_boost()
    posicao_x_anzol, posicao_y_anzol = gerar_anzol()

    if x == posicao_x_comida and y == posicao_y_comida:
        # adicione a posição da comida ao corpo da cobra
        pixels.append([posicao_x_comida, posicao_y_comida])
        # gere uma nova posição para a comida
        posicao_x_comida, posicao_y_comida = gerar_comida()
        # não aumente o tamanho_cobra, pois apenas o corpo deve crescer
    else:
        # se não comeu comida, remova o último segmento do corpo para manter o tamanho constante
        pixels.pop(0)

    while not fim_jogo:
        tela.fill(azul)

        tempo_atual = pygame.time.get_ticks()

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                fim_jogo = True
            elif evento.type == pygame.KEYDOWN:
                velocidade_x_nova, velocidade_y_nova = selecionar_velocidade(evento.key)
                if velocidade_x_nova != 0 or velocidade_y_nova != 0:
                    # Atualiza a direção apenas se a nova direção for válida
                    velocidade_x, velocidade_y = velocidade_x_nova, velocidade_y_nova

        # sistema de obstáculos - fase-1, nivel-1
        if (tamanho_cobra == 1 and fase == 1):
            desenhar_anzol(anzol, posicao_x_anzol, posicao_y_anzol)
            desenhar_anzol(anzol, posicao_x_anzol - 100, posicao_y_anzol - 100)
            desenhar_anzol(anzol, posicao_x_anzol + 300, posicao_y_anzol - 200)
            desenhar_anzol(anzol, posicao_x_anzol - 200, posicao_y_anzol + 50)
            desenhar_anzol(anzol, posicao_x_anzol + 100, posicao_y_anzol + 25)
            # colisões com o anzol
            if ((x == posicao_x_anzol and y == posicao_y_anzol) or (x == posicao_x_anzol-100 and y == posicao_y_anzol-100) or
            (x == posicao_x_anzol+300 and y == posicao_y_anzol-200) or (x == posicao_x_anzol-200 and y == posicao_y_anzol+50) or
            (x == posicao_x_anzol+100 and y == posicao_y_anzol+25)):
                fim_jogo = True

        # sistema de obstáculos - fase-1, nivel-2
        if tamanho_cobra == 2 and fase == 1:
             desenhar_anzol(anzol, posicao_x_anzol, posicao_y_anzol)
             desenhar_anzol(anzol, posicao_x_anzol + 150, posicao_y_anzol - 100)
             desenhar_anzol(anzol, posicao_x_anzol + 250, posicao_y_anzol + 200)
             desenhar_anzol(anzol, posicao_x_anzol - 125, posicao_y_anzol + 175)
             desenhar_anzol(anzol, posicao_x_anzol + 125, posicao_y_anzol + 250)
             # colisões com o anzol
             if ((x == posicao_x_anzol and y == posicao_y_anzol) or (x == posicao_x_anzol+150 and y == posicao_y_anzol-100) or
                (x == posicao_x_anzol+250 and y == posicao_y_anzol+200) or (x == posicao_x_anzol-125 and y == posicao_y_anzol+175) or
                (x == posicao_x_anzol+125 and y == posicao_y_anzol+250)):
                    fim_jogo = True

        # sistema de obstáculos - fase-1, nivel-3
        if tamanho_cobra == 3 and fase == 1:
            desenhar_anzol(anzol, posicao_x_anzol, posicao_y_anzol)
            desenhar_anzol(anzol, posicao_x_anzol + 175, posicao_y_anzol - 100)
            desenhar_anzol(anzol, posicao_x_anzol - 250, posicao_y_anzol + 200)
            desenhar_anzol(anzol, posicao_x_anzol - 125, posicao_y_anzol + 250)
            desenhar_anzol(anzol, posicao_x_anzol + 175, posicao_y_anzol + 250)
            # colisões com o anzol
            if ((x == posicao_x_anzol and y == posicao_y_anzol) or
                (x == posicao_x_anzol+175 and y == posicao_y_anzol-100) or (x == posicao_x_anzol-250 and y == posicao_y_anzol+200) or
                (x == posicao_x_anzol-125 and y == posicao_y_anzol+250) or (x == posicao_x_anzol+175 and y == posicao_y_anzol+250)):
                fim_jogo = True

        # sistema de obstáculos - fase-2, nivel-4
        if tamanho_cobra == 4 and fase == 2:
            desenhar_anzol(anzol, posicao_x_anzol, posicao_y_anzol)
            desenhar_anzol(anzol, posicao_x_anzol + 175, posicao_y_anzol - 100)
            desenhar_anzol(anzol, posicao_x_anzol - 250, posicao_y_anzol + 200)
            desenhar_anzol(anzol, posicao_x_anzol - 125, posicao_y_anzol + 250)
            desenhar_anzol(anzol, posicao_x_anzol + 175, posicao_y_anzol + 250)
            desenhar_anzol(anzol, posicao_x_anzol - 100, posicao_y_anzol - 100)
            desenhar_anzol(anzol, posicao_x_anzol + 300, posicao_y_anzol - 200)
            desenhar_anzol(anzol, posicao_x_anzol - 200, posicao_y_anzol + 50)
            desenhar_anzol(anzol, posicao_x_anzol + 100, posicao_y_anzol + 25)
            # colisões com o anzol
            if ((x == posicao_x_anzol + 175 and y == posicao_y_anzol - 100) or (
            x == posicao_x_anzol - 250 and y == posicao_y_anzol + 200) or
            (x == posicao_x_anzol - 125 and y == posicao_y_anzol + 250) or (
            x == posicao_x_anzol + 175 and y == posicao_y_anzol + 250)):
                fim_jogo = True
            if ((x == posicao_x_anzol and y == posicao_y_anzol) or (x == posicao_x_anzol-100 and y == posicao_y_anzol-100) or
            (x == posicao_x_anzol+300 and y == posicao_y_anzol-200) or (x == posicao_x_anzol-200 and y == posicao_y_anzol+50) or
            (x == posicao_x_anzol+100 and y == posicao_y_anzol+25)):
                fim_jogo = True

        # sistema de obstáculos - fase-2, nivel-5
        if tamanho_cobra == 5 and fase == 2:
            desenhar_anzol(anzol, posicao_x_anzol, posicao_y_anzol)
            desenhar_anzol(anzol, posicao_x_anzol + 150, posicao_y_anzol - 100)
            desenhar_anzol(anzol, posicao_x_anzol + 250, posicao_y_anzol + 200)
            desenhar_anzol(anzol, posicao_x_anzol - 125, posicao_y_anzol + 175)
            desenhar_anzol(anzol, posicao_x_anzol + 125, posicao_y_anzol + 250)
            desenhar_anzol(anzol, posicao_x_anzol - 100, posicao_y_anzol - 100)
            desenhar_anzol(anzol, posicao_x_anzol + 300, posicao_y_anzol - 200)
            desenhar_anzol(anzol, posicao_x_anzol - 200, posicao_y_anzol + 50)
            desenhar_anzol(anzol, posicao_x_anzol + 100, posicao_y_anzol + 25)
            # colisões com o anzol
            if ((x == posicao_x_anzol - 100 and y == posicao_y_anzol - 100) or
            (x == posicao_x_anzol + 300 and y == posicao_y_anzol - 200) or (
            x == posicao_x_anzol - 200 and y == posicao_y_anzol + 50) or
            (x == posicao_x_anzol + 100 and y == posicao_y_anzol + 25)):
                fim_jogo = True
            if ((x == posicao_x_anzol and y == posicao_y_anzol) or (
                    x == posicao_x_anzol + 150 and y == posicao_y_anzol - 100) or
                    (x == posicao_x_anzol + 250 and y == posicao_y_anzol + 200) or (
                            x == posicao_x_anzol - 125 and y == posicao_y_anzol + 175) or
                    (x == posicao_x_anzol + 125 and y == posicao_y_anzol + 250)):
                fim_jogo = True

        # sistema de obstáculos - fase-2, nivel-6
        if tamanho_cobra == 6 and fase == 2:
            desenhar_anzol(anzol, posicao_x_anzol, posicao_y_anzol)
            desenhar_anzol(anzol, posicao_x_anzol + 150, posicao_y_anzol - 100)
            desenhar_anzol(anzol, posicao_x_anzol + 250, posicao_y_anzol + 200)
            desenhar_anzol(anzol, posicao_x_anzol - 125, posicao_y_anzol + 175)
            desenhar_anzol(anzol, posicao_x_anzol + 125, posicao_y_anzol + 250)
            desenhar_anzol(anzol, posicao_x_anzol + 175, posicao_y_anzol - 100)
            desenhar_anzol(anzol, posicao_x_anzol - 250, posicao_y_anzol + 200)
            desenhar_anzol(anzol, posicao_x_anzol - 125, posicao_y_anzol + 250)
            desenhar_anzol(anzol, posicao_x_anzol + 175, posicao_y_anzol + 250)
            # colisões com o anzol
            if ((x == posicao_x_anzol and y == posicao_y_anzol) or
            (x == posicao_x_anzol + 175 and y == posicao_y_anzol - 100) or (
            x == posicao_x_anzol - 250 and y == posicao_y_anzol + 200) or
            (x == posicao_x_anzol - 125 and y == posicao_y_anzol + 250) or (
            x == posicao_x_anzol + 175 and y == posicao_y_anzol + 250)):
                fim_jogo = True
            if ((x == posicao_x_anzol + 150 and y == posicao_y_anzol - 100) or
            (x == posicao_x_anzol + 250 and y == posicao_y_anzol + 200) or (
            x == posicao_x_anzol - 125 and y == posicao_y_anzol + 175) or
            (x == posicao_x_anzol + 125 and y == posicao_y_anzol + 250)):
                fim_jogo = True

        # sistema de obstáculos - fase-3, nivel-7
        if tamanho_cobra == 7 and fase == 3:
            desenhar_anzol(anzol, posicao_x_anzol, posicao_y_anzol)
            desenhar_anzol(anzol, posicao_x_anzol - 175, posicao_y_anzol - 100)
            desenhar_anzol(anzol, posicao_x_anzol + 350, posicao_y_anzol - 300)
            desenhar_anzol(anzol, posicao_x_anzol + 125, posicao_y_anzol + 250)
            desenhar_anzol(anzol, posicao_x_anzol - 175, posicao_y_anzol + 250)
            desenhar_anzol(anzol, posicao_x_anzol + 500, posicao_y_anzol - 200)
            desenhar_anzol(anzol, posicao_x_anzol - 300, posicao_y_anzol - 200)
            desenhar_anzol(anzol, posicao_x_anzol + 200, posicao_y_anzol + 50)
            desenhar_anzol(anzol, posicao_x_anzol + 400, posicao_y_anzol - 125)
            desenhar_anzol(anzol, posicao_x_anzol - 250, posicao_y_anzol + 200)
            desenhar_anzol(anzol, posicao_x_anzol - 125, posicao_y_anzol + 250)
            desenhar_anzol(anzol, posicao_x_anzol + 175, posicao_y_anzol + 250)
            # colisões com o anzol
            if ((x == posicao_x_anzol - 175 and y == posicao_y_anzol - 100) or (
                    x == posicao_x_anzol + 350 and y == posicao_y_anzol - 300) or
                    (x == posicao_x_anzol + 125 and y == posicao_y_anzol + 250) or (
                            x == posicao_x_anzol - 175 and y == posicao_y_anzol + 250)):
                fim_jogo = True
            if ((x == posicao_x_anzol and y == posicao_y_anzol) or (
                x == posicao_x_anzol + 500 and y == posicao_y_anzol - 200) or
                (x == posicao_x_anzol - 300 and y == posicao_y_anzol - 200) or (
                x == posicao_x_anzol + 200 and y == posicao_y_anzol + 50) or
                (x == posicao_x_anzol + 400 and y == posicao_y_anzol - 125)):
                fim_jogo = True
            if ((x == posicao_x_anzol - 250 and y == posicao_y_anzol + 200) or
            (x == posicao_x_anzol - 125 and y == posicao_y_anzol + 250) or (
            x == posicao_x_anzol + 175 and y == posicao_y_anzol + 250)):
                fim_jogo = True

        # sistema de obstáculos - fase-3, nivel-8
        if tamanho_cobra == 8 and fase == 3:
            desenhar_anzol(anzol, posicao_x_anzol, posicao_y_anzol)
            desenhar_anzol(anzol, posicao_x_anzol + 275, posicao_y_anzol - 100)
            desenhar_anzol(anzol, posicao_x_anzol + 350, posicao_y_anzol - 300)
            desenhar_anzol(anzol, posicao_x_anzol + 125, posicao_y_anzol + 250)
            desenhar_anzol(anzol, posicao_x_anzol + 175, posicao_y_anzol - 250)
            desenhar_anzol(anzol, posicao_x_anzol + 500, posicao_y_anzol - 200)
            desenhar_anzol(anzol, posicao_x_anzol - 300, posicao_y_anzol - 200)
            desenhar_anzol(anzol, posicao_x_anzol + 200, posicao_y_anzol + 50)
            desenhar_anzol(anzol, posicao_x_anzol + 400, posicao_y_anzol - 125)
            desenhar_anzol(anzol, posicao_x_anzol - 250, posicao_y_anzol + 200)
            desenhar_anzol(anzol, posicao_x_anzol + 325, posicao_y_anzol + 350)
            desenhar_anzol(anzol, posicao_x_anzol + 175, posicao_y_anzol + 250)
            # colisões com o anzol
            if ((x == posicao_x_anzol + 275 and y == posicao_y_anzol - 100) or (
                    x == posicao_x_anzol + 350 and y == posicao_y_anzol - 300) or
                    (x == posicao_x_anzol + 125 and y == posicao_y_anzol + 250) or (
                            x == posicao_x_anzol + 175 and y == posicao_y_anzol - 250)):
                fim_jogo = True
            if ((x == posicao_x_anzol and y == posicao_y_anzol) or (
                    x == posicao_x_anzol + 500 and y == posicao_y_anzol - 200) or
                    (x == posicao_x_anzol - 300 and y == posicao_y_anzol - 200) or (
                            x == posicao_x_anzol + 200 and y == posicao_y_anzol + 50) or
                    (x == posicao_x_anzol + 400 and y == posicao_y_anzol - 125)):
                fim_jogo = True
            if ((x == posicao_x_anzol - 250 and y == posicao_y_anzol + 200) or
                    (x == posicao_x_anzol + 325 and y == posicao_y_anzol + 350) or (
                            x == posicao_x_anzol + 175 and y == posicao_y_anzol + 250)):
                fim_jogo = True

        # desenhar comida
        desenhar_comida(comida, posicao_x_comida, posicao_y_comida)

        if count_boost % 3 == 0:
            desenhar_boost(boost, posicao_x_boost, posicao_y_boost)

        # atualizar a posição da cobra
        if x < 0 or x >= largura or y < 0 or y >= altura:
            fim_jogo = True
        x += velocidade_x
        y += velocidade_y

        # desenhar cobra
        pixels.append([x, y])
        if len(pixels) > tamanho_cobra:
            del pixels[0]

        for pixel in pixels[:-1]:
            if pixel == [x, y]:
                fim_jogo = True
        desenhar_cobra(pixels, corpo_cobra)

        # desenhar pontuação
        desenhar_pontuacao(pontuacao)

        tempo_atual = pygame.time.get_ticks()


        # atualização da tela
        pygame.display.update()

        # criar uma nova comida e aumentar fase
        if x == posicao_x_comida and y == posicao_y_comida:
            tamanho_cobra += 1
            if tamanho_cobra == 4 or tamanho_cobra == 7 or tamanho_cobra == 9:
                fase+=1
            if boost_ativo:
                pontuacao += 2
            else:
                pontuacao += 1

            count_boost += 1
            posicao_x_comida, posicao_y_comida = gerar_comida()

        if x == posicao_x_boost and y == posicao_y_boost:
            count_boost += 1
            boost_ativo = 1
            tempo_inicial = pygame.time.get_ticks()

        if boost_ativo and tempo_atual - tempo_inicial <= duracao_boost:
            velocidade_jogo = 30
            tempo_decorrido = pygame.time.get_ticks() - tempo_inicial
            tempo_restante = max(0, duracao_boost - tempo_decorrido)
            mostra_temporizador(tempo_restante // 1000)
        
            # atualiza o retangulo no qual o temporizador esta inserido para que seja possivel a contagem regressiva do tempo do boost

            pygame.display.update([0, 0, 100, 100])
        else:
            velocidade_jogo = 10
            boost_ativo = 0

        
        # tempo de jogo
        relogio.tick(velocidade_jogo)
    return pontuacao 
tela_inicial()
while True:  # Loop principal do jogo
    pontuacao = rodar_jogo()
    tela_final(pontuacao) 

tela_final()
