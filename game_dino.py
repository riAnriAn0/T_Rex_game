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

    def __init__(self, y):
        self.imagem = self.IMAGEM
        self.x = 1100
        self.y = y
        self.velocidade = 1
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
        self.velocidade = 40
        self.sprite_width = self.IMAGEM.get_width()
        self.sprite_height = self.IMAGEM.get_height()
        self.passou = False

    def animacao(self):

        self.x -= self.velocidade
        if self.x < 10:
            self.passou = True
    
    def mask(self):
        return pygame.mask.from_surface(self.imagem)

    def desenhar(self, tela):    
        tela.blit( self.imagem,(self.x, self.y))

class Dino:

    IMAGEM = IMAGEM_DINO
    IMAGEM_REBAIXADO = IMAGEM_DINO_REBAIXADO
    FRAME_X = 87.5
    FRAME_Y = 94

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

    def desenhar(self, tela):
        if self.colidir:
            self.sprite_atual = 3
        elif not self.pulando:
            self.sprite_atual += 1
            if self.sprite_atual > 2:
                self.sprite_atual = 1
        elif self.pulando:
            self.sprite_atual = 0
        
        tela.blit( self.imagem,(self.x, self.y), (self.sprite_atual * self.FRAME_X, 0, self.FRAME_X, self.FRAME_Y))

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
        frame_x = self.sprite_atual * self.FRAME_X  
        dino_frame_surface = self.imagem.subsurface((frame_x, 0, self.FRAME_X, self.FRAME_Y))
        return pygame.mask.from_surface(dino_frame_surface)
    
    def colisao(self, objeto):

        offset_x = objeto.x - self.x
        offset_y = objeto.y - self.y

        mask_dino = self.mask()
    
        if mask_dino.overlap(objeto.mask(),(offset_x, offset_y)):
            objeto.velocidade = 0
            self.colidir = True


def main():
    global MELHOR_PONTUACAO

    DISPLAY_WIDTH = 1200
    DIPLAY_HEIGHT = 500

    display = pygame.display.set_mode((DISPLAY_WIDTH,DIPLAY_HEIGHT))
    clock = pygame.time.Clock()
    rodando = True
    pontos = 0
    game_over = Over()
    chao = Chao()
    nuvens = [Nuvem(0)]
    cactos = [Cactos(0)]
    dino = Dino()
    primeiro_cacto = True

    while rodando:
    
        clock.tick(18) 

        for event in pygame.event.get():
            if event.type == QUIT:
                rodando = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:    
                    dino.pular()
                if event.key == pygame.K_r and dino.colidir:
                    main() 

        if dino.pulando:
            dino.pular()
        
        display.fill((247,247,247))

        texto = FONTE_PONTOS.render(f"SCORE: {pontos}", 0,(83,83,83))
        texto_mpv = FONTE_PONTOS.render(f"MVP: {MELHOR_PONTUACAO}", 0,(166,166,166))
        display.blit(texto,(1000 , 100))
        display.blit(texto_mpv,(900 , 100))
        
        if len(nuvens) == 0 or len(nuvens) < 2:
            y = random.randrange(50,200,10)
            nuvens.append(Nuvem(y - 10))

        if primeiro_cacto:
            cactos.append(Cactos(1400))
            primeiro_cacto = False

        if cactos[0].x < 500 and len(cactos) < 3:
            x = random.randrange(1400,1600,100)
            cactos.append(Cactos(x))
           
        for cacto in cactos:
            dino.colisao(cacto) 

        if not dino.colidir:
            for cacto in cactos:
                cacto.animacao()
            for nuvem in nuvens:
                nuvem.animacao()
            chao.animacao()

        chao.desenhar(display)
        dino.desenhar(display)

        for nuvem in nuvens:
            nuvem.desenhar(display)

        for cacto in cactos:
            cacto.desenhar(display)
        
        for i,cacto in enumerate(cactos):
            if cacto.passou:
                cactos.pop(i)
        
        for i,nuven in enumerate(nuvens):
            if nuven.passou:
                nuvens.pop(i)

        if not dino.colidir:
            pontos += 1
            if pontos % 100 == 0:
                chao.velocidade += 5
                for cacto in cactos:
                    cacto.velocidade += 5

        retornar = FONTE_PONTOS.render(f"Precione r para reiniciar", 0,(64,64,64))

        if dino.colidir:
            if pontos > MELHOR_PONTUACAO:
                MELHOR_PONTUACAO = pontos
            game_over.desenhar(display)
            display.blit(retornar,( 500 ,240))

        
        pygame.display.flip()

    pygame.quit()
    exit()

if __name__ == "__main__":
    main()


