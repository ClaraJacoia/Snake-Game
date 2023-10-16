import pygame
import random

pygame.init()
pygame.display.set_caption("Jogo da cobrinha")
largura, altura = 1000, 700
tela = pygame.display.set_mode((largura, altura))
relogio = pygame.time.Clock()
fonte = pygame.font.Font(None, 36)

#cores
azul = (0, 0, 255)
branca = (255, 255, 255)
vermelho = (255, 0, 0)
verde = (0, 255, 0)
rosa = (255, 105, 180)

#parametros da cobrinha
cabeca_cobra = pygame.image.load("C:\\Snake-Game\\imagens\\pixil-frame-0.png")
corpo_cobra = pygame.image.load("C:\\Snake-Game\\imagens\\pixil-frame-0 (1).png")
cauda_cobra = pygame.image.load("C:\\Snake-Game\\imagens\\pixil-frame-0 (3).png")
comida = pygame.image.load("C:\\Snake-Game\\imagens\\pixil-frame-0 (2).png")
velocidade_inicial = 22
velocidade_atual = 5
tamanho_quadrado = 25

def tela_inicial():
    texto_titulo = fonte.render("Jogo da Cobrinha", True, rosa)
    # Instruções
    tela.blit(texto_titulo, (largura // 2 - texto_titulo.get_width() // 2, 100))
    texto_titulo = fonte.render("Use WASD para mover a Cobrinha", True, azul)
    tela.blit(texto_titulo, (largura // 2 - texto_titulo.get_width() // 2, 150))
    texto_titulo = fonte.render("Coma as frutinhas e fuja das paredes e de você mesmo", True, azul)
    tela.blit(texto_titulo, (largura // 2 - texto_titulo.get_width() // 2, 200))
    texto_titulo = fonte.render("Lembrando que o raio te deixa mais rápido. Use com cautela!", True, azul)
    tela.blit(texto_titulo, (largura // 2 - texto_titulo.get_width() // 2, 250))
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

def gerar_comida():
    posicao_x_comida = round(random.randrange(40, largura-tamanho_quadrado+15) / float(tamanho_quadrado)) * float(tamanho_quadrado)
    posicao_y_comida = round(random.randrange(40, altura-tamanho_quadrado+15) / float(tamanho_quadrado)) * float(tamanho_quadrado)
    return posicao_x_comida, posicao_y_comida
def desenhar_cobra(pixels, corpo_cobra):
    tela.blit(cauda_cobra, [pixels[0][0], pixels[0][1]])
    pixels_invertidos = pixels[::-1]
    #desenha o corpo da cobra
    for pixel in pixels_invertidos[1:]:
        tela.blit(corpo_cobra, [pixel[0], pixel[1]])
    #desenha a cabeça da cobra por último
    tela.blit(cabeca_cobra, [pixels_invertidos[0][0], pixels_invertidos[0][1]])
def desenhar_comida(comida,posicao_x_comida,posicao_y_comida):
        tela.blit(comida, [posicao_x_comida, posicao_y_comida])
def selecionar_velocidade(tecla):
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
    fonte = pygame.font.SysFont("Helvetica", 35)
    texto = fonte.render(f"Pontos: {pontuacao}", True, vermelho)
    tela.blit(texto, [1,1])
def rodar_jogo():
    fim_jogo = False
    global velocidade_atual

    x = largura/2
    y = altura/2

    velocidade_x = 0
    velocidade_y = 0

    tamanho_cobra = 1

    pixels = [[largura / 2, altura / 2], [largura / 2 - tamanho_quadrado, altura / 2]]

    posicao_x_comida,posicao_y_comida = gerar_comida()

    if x == posicao_x_comida and y == posicao_y_comida:
        #adicione a posição da comida ao corpo da cobra
        pixels.append([posicao_x_comida, posicao_y_comida])
        #gere uma nova posição para a comida
        posicao_x_comida, posicao_y_comida = gerar_comida()
        #não aumente o tamanho_cobra, pois apenas o corpo deve crescer
    else:
        #se não comeu comida, remova o último segmento do corpo para manter o tamanho constante
        pixels.pop(0)

    while not fim_jogo:
        tela.fill(azul)

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                fim_jogo = True
            elif evento.type == pygame.KEYDOWN:
                velocidade_x, velocidade_y = selecionar_velocidade(evento.key)

        #desenhar comida
        desenhar_comida(comida, posicao_x_comida, posicao_y_comida)

        #atualizar a posição da cobra
        if x < 0 or x >= largura or y < 0 or y >= altura:
            fim_jogo = True
        x += velocidade_x
        y += velocidade_y

        #desenhar cobra
        pixels.append([x, y])
        if len(pixels) > tamanho_cobra:
            del pixels[0]

        for pixel in pixels[:-1]:
            if pixel == [x,y]:
                fim_jogo = True
        desenhar_cobra(pixels, corpo_cobra)

        #desenhar pontuação
        desenhar_pontuacao(tamanho_cobra - 1)

        #atualização da tela
        pygame.display.update()

        #criar uma nova comida
        if x == posicao_x_comida and y == posicao_y_comida:
            tamanho_cobra += 1
            velocidade_atual += 5
            posicao_x_comida, posicao_y_comida = gerar_comida()

        #tempo de jogo
        relogio.tick(velocidade_atual)
        
tela_inicial()
rodar_jogo()
