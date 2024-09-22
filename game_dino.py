import pygame
import os 
import random
from pygame.locals import *
from sys import exit

pygame.init()
pygame.font.init()

MELHOR_PONTUACAO = 0
IMAGEM_OVER = pygame.image.load(os.path.join('img','game_over.png'))
IMAGEM_DINO = pygame.image.load(os.path.join('img','dino.png'))
IMAGEM_DINO_REBAIXADO = pygame.image.load(os.path.join('img','dino_rebaixado.png'))
IMAGEM_CHAO = pygame.image.load(os.path.join('img','chao.png'))
IMAGEM_NUVEM =  pygame.image.load(os.path.join('img','nuvem.png'))
IMAGEM_CACTO = pygame.image.load(os.path.join('img','cacto.png'))
IMAGEM_AVES = pygame.image.load(os.path.join('img','aves.png'))
FONTE_PONTOS = pygame.font.SysFont(os.path.join('fonts','PressStart2P-Regular.ttf') , 30)

class Over:

    IMAGEM = IMAGEM_OVER

    def __init__(self):
        self.x = 600 - (self.IMAGEM.get_width() / 2)
        self.y = 200
        self.imagem = self.IMAGEM
        self.sprite_width = self.IMAGEM.get_width()
        self.sprite_height = self.IMAGEM.get_height()

    def desenhar(self, tela):
        tela.blit(self.imagem, (self.x,self.y))

class Chao:

    IMAGEM = IMAGEM_CHAO
    FRAME_X = 0
    FRAME_Y = 0

    def __init__(self):
        self.imagem = self.IMAGEM
        self.x = 0
        self.y = 340
        self.x_2 = 1200
        self.y_2 = 340
        self.velocidade = 30
        self.sprite_width = self.IMAGEM.get_width()
        self.sprite_height = self.IMAGEM.get_height()

    def animacao(self):
        self.x -= self.velocidade
        self.x_2 -= self.velocidade

        if self.x < -1200:
            self.x = 1200

        if self.x_2 < -1200:
            self.x_2 = 1200
    
    def desenhar(self, tela):
        tela.blit( self.imagem,(self.x, self.y))
        tela.blit( self.imagem,(self.x_2, self.y_2))

class Nuvem:

    IMAGEM = IMAGEM_NUVEM
    FRAME_X = 0
    FRAME_Y = 0

    def __init__(self,x, y):
        self.imagem = self.IMAGEM
        self.x = x
        self.y = y
        self.velocidade = 3
        self.sprite_width = self.IMAGEM.get_width()
        self.sprite_height = self.IMAGEM.get_height()
        self.passou = False

    def animacao(self):
        self.x -= self.velocidade
        if self.x < -50:
            self.passou = True

    def desenhar(self, tela):
        tela.blit( self.imagem,(self.x, self.y))


class Cactos:

    IMAGEM = IMAGEM_CACTO
    SPRITE_WIDTH = 25
    SPRITE_HEIGHT = 47
    FRAME_X = 0
    FRAME_Y = 0

    def __init__(self, x):
        self.x = x
        self.y = 275  
        self.imagem = self.IMAGEM
        self.velocidade = 35
        self.sprite_width = self.IMAGEM.get_width()
        self.sprite_height = self.IMAGEM.get_height()
        self.passou = False

    def animacao(self):

        self.x -= self.velocidade
        if self.x < -100:
            self.passou = True
    
    def mask(self):
        return pygame.mask.from_surface(self.imagem)

    def desenhar(self, tela):    
        tela.blit( self.imagem,(self.x, self.y))

class Aves:

    IMAGEM = IMAGEM_AVES
    SPRITE_WIDTH = 184
    SPRITE_HEIGHT = 79
    FRAME_X = 92
    FRAME_Y = 79

    def __init__(self, x):
        self.x = x
        self.y = 200
        self.imagem = self.IMAGEM
        self.velocidade = 35
        self.sprite_width = self.IMAGEM.get_width()
        self.sprite_height = self.IMAGEM.get_height()
        self.sprite_atual = 1
        self.passou = False

    def animacao(self):
        self.x -= self.velocidade
        if self.x < -100:
            self.passou = True
    
    def mask(self):
        return pygame.mask.from_surface(self.imagem)

    def desenhar(self, tela): 
        self.sprite_atual += 1
        if self.sprite_atual > 1:
            self.sprite_atual = 0

        tela.blit(self.imagem,(self.x, self.y), (self.sprite_atual * self.FRAME_X, 0, self.FRAME_X, self.FRAME_Y))

class Dino:

    IMAGEM = IMAGEM_DINO
    IMAGEM_REBAIXADO = IMAGEM_DINO_REBAIXADO

    def __init__(self):
        self.x = 150
        self.y = 265
        self.imagem = self.IMAGEM
        self.sprite_atual = 1
        self.sprite_width = self.IMAGEM.get_width()
        self.sprite_height = self.IMAGEM.get_height()
        self.velocidade = 2
        self.gravidade = 3.5
        self.pulando = False
        self.colidir = False
        self.abaixar = False

    def desenhar(self, tela):
        
        if self.abaixar:
            self.sprite_atual += 1
            if self.sprite_atual > 1:
                self.sprite_atual = 0
        elif self.colidir:
            self.sprite_atual = 3
        elif not self.pulando:
            self.sprite_atual += 1
            if self.sprite_atual > 2:
                self.sprite_atual = 1
        elif self.pulando:
            self.sprite_atual = 0

        if self.abaixar:   
            self.imagem = self.IMAGEM_REBAIXADO
            tela.blit( self.imagem,(self.x, 300), (self.sprite_atual * 118.5, 0, 118.5, 59))
        else:
            self.imagem = self.IMAGEM
            tela.blit( self.imagem,(self.x, self.y), (self.sprite_atual * 87.5, 0, 87.5, 94))

    def pular(self):

        if not self.pulando:
            self.y -= 160 
            self.pulando = True

        if self.y < 270:
                self.y += self.velocidade
                self.velocidade += self.gravidade
                if self.y > 265:
                    self.y = 265
                    self.pulando = False
                    self.velocidade = 0

    def mask(self):
        if self.abaixar:
            dino_frame_surface = self.imagem.subsurface((self.sprite_atual * 118.5, 0, 118.5, 59))
        else:
            dino_frame_surface = self.imagem.subsurface((self.sprite_atual * 87.5, 0, 87.5, 94))
        
        return pygame.mask.from_surface(dino_frame_surface)
    
    def colisao(self, obstaculo):

        offset_x = obstaculo.x - self.x
        offset_y = obstaculo.y - (self.y if not self.abaixar else 300)
        mask_dino = self.mask()

        if mask_dino.overlap(obstaculo.mask(),(offset_x, offset_y)):
            obstaculo.velocidade = 0
            self.colidir = True

def desenhar(tela, chao, nuvens, cactos, aves, dino, pontos):
    texto = FONTE_PONTOS.render(f"SCORE: {pontos}", 0,(83,83,83))
    texto_mpv = FONTE_PONTOS.render(f"MVP: {MELHOR_PONTUACAO}", 0,(166,166,166))

    tela.blit(texto,(1000 , 100))
    tela.blit(texto_mpv,(900 , 100))
    
    if not dino.colidir:
        for cacto in cactos:
            cacto.animacao()
        for ave in aves:
            ave.animacao()
        for nuvem in nuvens:
            nuvem.animacao()
        chao.animacao()

    chao.desenhar(tela)
    dino.desenhar(tela)

    for nuvem in nuvens:
        nuvem.desenhar(tela)

    for cacto in cactos:
        cacto.desenhar(tela)
    
    for ave in aves:
        ave.desenhar(tela)

def retornar(display, game_over, dino, pontos):
    global MELHOR_PONTUACAO

    retorne = FONTE_PONTOS.render(f"Precione R para reiniciar", 0,(64,64,64))

    if dino.colidir:
        game_over.desenhar(display)
        display.blit(retorne,( 500 ,240))
        if pontos > MELHOR_PONTUACAO:
            MELHOR_PONTUACAO = pontos

def main():
    global MELHOR_PONTUACAO

    DISPLAY_WIDTH = 1200
    DIPLAY_HEIGHT = 500

    display = pygame.display.set_mode((DISPLAY_WIDTH,DIPLAY_HEIGHT))
    clock = pygame.time.Clock()
    rodando = True
    game_over = Over()
    chao = Chao()
    nuvens = [Nuvem(1100,100)]
    cactos = [Cactos(1400)]
    aves = [Aves(3000)]
    dino = Dino()
    pontos = 0

    while rodando:
    
        clock.tick(18) 
        display.fill((247,247,247))

        for event in pygame.event.get():
            if event.type == QUIT:
                rodando = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:    
                    dino.pular()
                if event.key == pygame.K_r and dino.colidir:
                    main() 
        
        keys = pygame.key.get_pressed()

        if keys[pygame.K_DOWN]:
            dino.abaixar = True
        else:
            dino.abaixar = False


        if dino.pulando:
            dino.pular()

        if nuvens[0].x < 700 and len(nuvens) < 2:
            x = random.randrange(1100,1300,100)
            y = random.randrange(190,270,20)
            nuvens.append(Nuvem(x, y - 10))

        num = random.randrange(0,10,1)

        if num <= 7 :
            if len(cactos) > 0:
                if cactos[0].x < 600:
                    if len(aves) > 0 :
                        dist_a = aves[0].x
                        cactos.append(Cactos(dist_a + 600))
                    else:    
                        x_c = random.choice((50,100))
                        cactos.append(Cactos(1100 + x_c))
        else:
            if  len(aves) > 0: 
                if aves[0].x < 500:
                    if len(cactos) > 0:
                        dist_c = cactos[0].x
                        aves.append(Aves( dist_c + 600 ))
                    else:
                        x_a = random.choice((0,100,200))
                        aves.append(Aves(x_a + 1400))
        

        desenhar(display,chao, nuvens, cactos, aves, dino, pontos)
           
        for cacto in cactos:
            dino.colisao(cacto) 
        
        for ave in aves:
            dino.colisao(ave)

        for i,cacto in enumerate(cactos):
            if cacto.passou:
                cactos.pop(i)

        for i,ave in enumerate(aves):
            if ave.passou:
                aves.pop(i)
        
        for i,nuven in enumerate(nuvens):
            if nuven.passou:
                nuvens.pop(i)

        if not dino.colidir:
            pontos += 1
        if pontos % 100 == 0:
            chao.velocidade += 5
            for cacto in cactos:
                cacto.velocidade  += 5 

        retornar(display, game_over, dino, pontos)
        
        pygame.display.flip()

    pygame.quit()
    exit()

if __name__ == "__main__":
    main()


