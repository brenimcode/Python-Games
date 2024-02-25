import pygame
import sys
import random

# Inicializar o Pygame
pygame.init()

# Definir as dimensões da janela
largura, altura = 1200, 800
tela = pygame.display.set_mode((largura, altura))
pygame.display.set_caption("Jogo do Cavalinho")

# Carregar a imagem PNG e redimensioná-la
imagem_cavalo_original = pygame.image.load("cavalo2.png")  
largura_cavalo, altura_cavalo = 100, 100  
imagem_cavalo = pygame.transform.scale(imagem_cavalo_original, (largura_cavalo, altura_cavalo))

# Coordenadas iniciais do cavalo
x, y = largura/2, 0

# Definir a velocidade de movimento do CAVALO
velocidade = 15

# Coordenadas e dimensões do OBSTACULO 1 e 2
obstaculo_x, obstaculo_y = 1100, (altura/2)-100
obstaculo_largura, obstaculo_altura = 100, 150

obstaculo2_x, obstaculo2_y = 5, 200
obstaculo2_largura, obstaculo2_altura = 100, 150

def gerar_coordenadas_aleatorias():
    novo_x = random.randint(0, largura - largura_cavalo)
    novo_y = random.randint(0, altura - altura_cavalo)
    return novo_x, novo_y
                    
# Coordenadas e dimensões dos obstáculos CIRCULOS de VELOCIDADE
obstaculo_aumenta_velocidade_x, obstaculo_aumenta_velocidade_y = gerar_coordenadas_aleatorias()
obstaculo_diminui_velocidade_x, obstaculo_diminui_velocidade_y = gerar_coordenadas_aleatorias()
obstaculo_velocidade_largura, obstaculo_velocidade_altura = 100, 100

# Definir fonte para a mensagem
fonte = pygame.font.SysFont('JetBrains Mono', 20)


# Função para exibir mensagem de perda e perguntar se o jogador quer jogar novamente
def exibir_mensagem_perda():
    # Criar uma nova janela para a mensagem de perda
    tela_perda = pygame.display.set_mode((largura, altura))
    pygame.display.set_caption("Você perdeu!")
    
    mensagem = fonte.render("Você perdeu! Deseja jogar novamente?  (S para SIM e N para NAO)", True, (255, 0, 0))
    tela_perda.blit(mensagem, (200, 350))
    pygame.display.flip()

    # Aguardar resposta do jogador
    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_s:  # S para sim
                    return True
                elif evento.key == pygame.K_n:  # N para não
                    pygame.quit()
                    sys.exit()

def exibir_mensagem_ganho():
    # Criar uma nova janela para a mensagem de perda
    tela_ganho = pygame.display.set_mode((largura, altura))
    pygame.display.set_caption("Você VENCEU!!!")

    
    mensagem = fonte.render("Você VENCEU! Deseja jogar novamente?  (S para SIM e N para NAO)", True, (0, 255, 110))
    tela_ganho.blit(mensagem, (200, 350))
    pygame.display.flip()

    # Aguardar resposta do jogador
    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_s:  # S para sim
                    return True
                elif evento.key == pygame.K_n:  # N para não
                    pygame.quit()
                    sys.exit()

# SONS
                    
som_colisao_perda = pygame.mixer.Sound("triste.mp3")
som_colisao_ganho = pygame.mixer.Sound("nossa.mp3")  
som_colisao_velocidade = pygame.mixer.Sound("mario.mp3")  
som_colisao_velocidade.set_volume(0.09)

pygame.mixer.music.set_volume(0.25)
som_fundo = pygame.mixer.music.load("fundo.mp3")
pygame.mixer.music.play(-1)

#textos
pontos = 5


# Loop principal

rodando = True

while rodando:
    # Verificar eventos
    texto_do_jogo = f'Pontos: {pontos}'
    texto_formatado = fonte.render(texto_do_jogo, True, (0,0,0))
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False
    
    # Movimento contínuo do cavalo
    teclas_press = pygame.key.get_pressed()
    if teclas_press[pygame.K_LEFT] or teclas_press[pygame.K_a]:
        if x > 0:  # Verificar se não atingiu o limite esquerdo da tela
            x -= velocidade
    if teclas_press[pygame.K_RIGHT] or teclas_press[pygame.K_d]:
        if x < largura - largura_cavalo:  # Verificar se não atingiu o limite direito da tela
            x += velocidade
    if teclas_press[pygame.K_UP] or teclas_press[pygame.K_w]:
        if y > 0:  # Verificar se não atingiu o limite superior da tela
            y -= velocidade
    if teclas_press[pygame.K_DOWN] or teclas_press[pygame.K_s]:
        if y < altura - altura_cavalo:  # Verificar se não atingiu o limite inferior da tela
            y += velocidade
    
    # Verificar colisão com o obstáculo
    if x < obstaculo_x + obstaculo_largura and x + largura_cavalo > obstaculo_x and \
       y < obstaculo_y + obstaculo_altura and y + altura_cavalo > obstaculo_y:
        som_colisao_perda.play()
        if exibir_mensagem_perda():
            x, y = 0, 0
            continue  # Reiniciar o jogo após o jogador escolher jogar novamente
    # Verificar colisão com o obstáculo 2 (o obstáculo da vitória)
    if x < obstaculo2_x + obstaculo2_largura and x + largura_cavalo > obstaculo2_x and \
       y < obstaculo2_y + obstaculo2_altura and y + altura_cavalo > obstaculo2_y:
        som_colisao_ganho.play()
        if exibir_mensagem_ganho():
            x, y = 0, 0
            continue  # Reiniciar o jogo após o jogador escolher jogar novamente

    # Verifica colisao com o obstaculo que diminui velocidade
    if x < obstaculo_aumenta_velocidade_x + obstaculo_velocidade_largura and x + largura_cavalo > obstaculo_aumenta_velocidade_x and \
       y < obstaculo_aumenta_velocidade_y + obstaculo_velocidade_altura and y + altura_cavalo > obstaculo_aumenta_velocidade_y:
        som_colisao_velocidade.play()
        if(pontos>0): pontos-=1
        if(velocidade > 5): velocidade -= 5  # Diminuir a velocidade do cavalo
        obstaculo_aumenta_velocidade_x, obstaculo_aumenta_velocidade_y = gerar_coordenadas_aleatorias()  # Mover o obstáculo que diminui a velocidade para fora da tela

    # Verifica colisao com o obstaculo que aumenta velocidade
    if x < obstaculo_diminui_velocidade_x + obstaculo_velocidade_largura and x + largura_cavalo > obstaculo_diminui_velocidade_x and \
       y < obstaculo_diminui_velocidade_y + obstaculo_velocidade_altura and y + altura_cavalo > obstaculo_diminui_velocidade_y:
        som_colisao_velocidade.play()
        pontos+=1
        if(velocidade < 80): velocidade += 5  # Diminuir a velocidade do cavalo
        obstaculo_diminui_velocidade_x, obstaculo_diminui_velocidade_y = gerar_coordenadas_aleatorias() # Mover o obstáculo que diminui a velocidade para fora da tela

    # Limpar a tela
    tela.fill((255, 255, 255))  # Cor de fundo branca

    # Desenhar a imagem do cavalo na tela
    tela.blit(imagem_cavalo, (x, y))
    #Desenha Texto
    tela.blit(texto_formatado,(largura/2-100,(altura/2)+350))

    # Desenhar o obstáculo na tela
    pygame.draw.rect(tela, (255, 0, 0), (obstaculo_x, obstaculo_y, obstaculo_largura, obstaculo_altura))

    #Fazendo com que mude a posição do bloco RED
    obstaculo_y+=3
    if obstaculo_y >= altura:
        obstaculo_y=0

    # Desenhar o obstáculo2 na tela
    pygame.draw.rect(tela, (0, 250, 10), (obstaculo2_x, obstaculo2_y, obstaculo2_largura, obstaculo2_altura))

  #Fazendo com que mude a posição do bloco RED
    obstaculo2_y+=5
    if obstaculo2_y >= altura:
        obstaculo2_y=0


    # Desenhar o obstáculo que diminui velocidade na tela
    pygame.draw.circle(tela, (147,0 , 211), (obstaculo_aumenta_velocidade_x, obstaculo_aumenta_velocidade_y),15)

    # Desenhar o obstáculo que aumenta velocidade na tela
    pygame.draw.circle(tela, (0, 0, 0), (obstaculo_diminui_velocidade_x, obstaculo_diminui_velocidade_y), 20)

    # Atualizar a tela
    pygame.display.flip()

    # Controlar a taxa de quadros por segundo
    pygame.time.Clock().tick(100)

# Sair do Pygame
pygame.quit()
sys.exit()
