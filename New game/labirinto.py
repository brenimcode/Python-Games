import pygame
from pygame.locals import *
from sys import exit
from random import randint

pygame.init()

pygame.mixer.music.set_volume(0.1)
musica_de_fundo = pygame.mixer.music.load('fundo.mp3')
barulho_colisao = pygame.mixer.Sound('mario.mp3')
pygame.mixer.music.play(-1)

largura = 640
altura = 480

x = int(largura/2) 
y = int(altura/2)

x_azul = randint(40, 600)
y_azul = randint(50, 430)

pontos = 0
fonte = pygame.font.SysFont('arial', 40, bold=True, italic=True)

tela = pygame.display.set_mode((largura, altura))
pygame.display.set_caption('Jogo')
relogio = pygame.time.Clock()

while True:
    relogio.tick(30)
    tela.fill((255,255,255))
    
    mensagem = f'Pontos: {pontos}'
    texto_formatado = fonte.render(mensagem, True, (15,15,15))
    
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            exit()
        '''
        if event.type == KEYDOWN:
            if event.key == K_a:
                x = x - 20
            if event.key == K_d:
                x = x + 20
            if event.key == K_w:
                y = y - 20
            if event.key == K_s:
                y = y + 20'''
                        
    if pygame.key.get_pressed()[K_a]:
        x = x - 20
    if pygame.key.get_pressed()[K_d]:
        x = x + 20 
    if pygame.key.get_pressed()[K_w]:
        y = y - 20
    if pygame.key.get_pressed()[K_s]:
        y = y + 20
        
    cobra = pygame.draw.rect(tela, (0,210,120), (x,y,20,20))
    maca = pygame.draw.rect(tela, (255,0,0), (x_azul,y_azul,20,20))
    
    if cobra.colliderect(maca):
        x_azul = randint(40, 600)
        y_azul = randint(50, 430)
        pontos += 1
        barulho_colisao.play()
        
    tela.blit(texto_formatado, (450,40))

    
    pygame.display.update()