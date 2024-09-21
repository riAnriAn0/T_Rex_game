import pygame
import os 
import random
from pygame.locals import *
from sys import exit

pygame.init()
pygame.font.init()

IMAGEM_OVER = pygame.image.load(os.path.join('img','game_over.png'))
IMAGEM_RETURN = pygame.transform.scale2x(pygame.image.load(os.path.join('img','return.png')))
IMAGEM_DINO = pygame.image.load(os.path.join('img','dino.png'))
IMAGEM_CHAO = pygame.image.load(os.path.join('img','chao.png'))
IMAGEM_NUVEM =  pygame.image.load(os.path.join('img','nuvem.png'))
FONTE_PONTOS = pygame.font.SysFont(os.path.join('fonts','PressStart2P-Regular.ttf') , 20)
IMAGEMS_CACTOS = [
    pygame.image.load(os.path.join('img','cactos1.png')),
    pygame.image.load(os.path.join('img','cactos2.png')),
    pygame.image.load(os.path.join('img','cactos3.png')),
    pygame.image.load(os.path.join('img','cactos4.png'))
]

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

class Return:

    IMAGEM = IMAGEM_RETURN

    def __init__(self):
        self.x = 600 - (self.IMAGEM.get_width() / 2)
        self.y = 225
        self.imagem = self.IMAGEM
        self.sprite_width = self.IMAGEM.get_width()
        self.sprite_height = self.IMAGEM.get_height()

    def desenhar(self, tela):
        tela.blit(self.imagem, (self.x,self.y))

class Chao:

    IMAGEM = IMAGEM_CHAO
    VELOCIDADE = 30
    FRAME_X = 0
    FRAME_Y = 0

    def __init__(self):
        self.imagem = self.IMAGEM
        self.x = 0
        self.y = 300
        self.x_2 = 1200
        self.y_2 = 300
        self.velocidade = self.VELOCIDADE
        self.sprite_width = self.IMAGEM.get_width()
        self.sprite_height = self.IMAGEM.get_height()

    def animacao(self):
        self.x -= self.velocidade
        self.x_2 -= self.velocidade

        if self.x == -1200:
            self.x = 1200

        if self.x_2 == -1200:
            self.x_2 = 1200
    
    def desenhar(self, tela):
        tela.blit( self.imagem,(self.x, self.y))
        tela.blit( self.imagem,(self.x_2, self.y_2))

class Nuvem:

    IMAGEM = IMAGEM_NUVEM
    VELOCIDADE = 5
    FRAME_X = 0
    FRAME_Y = 0

    def __init__(self):
        self.imagem = self.IMAGEM
        self.x = 500
        self.y = 250
        self.velocidade = self.VELOCIDADE
        self.sprite_width = self.IMAGEM.get_width()
        self.sprite_height = self.IMAGEM.get_height()

    def animacao(self):
        self.x -= self.velocidade

        if self.x == -50:
            self.x = 1000 #????????
    def desenhar(self, tela):
        tela.blit( self.imagem,(self.x, self.y))


class Cactos:

    IMAGEMS = IMAGEMS_CACTOS
    VELOCIDADE = 40
    SPRITE_WIDTH = 25
    SPRITE_HEIGHT = 47
    FRAME_X = 0
    FRAME_Y = 0

    def __init__(self):
        self.x = 1250
        self.y = 265  
        self.imagem = self.random_image()
        self.velocidade = self.VELOCIDADE
        self.sprite_width = self.imagem.get_width()
        self.sprite_height = self.imagem.get_height()
        self.passou = False

    def random_image(self):
        num = random.randrange(1,10)

        if num <= 4:
            return self.IMAGEMS[0]
        elif num >= 5 and num <=7:
            return self.IMAGEMS[1]
        elif num == 8 or num == 9:
            return self.IMAGEMS[2]
        else:
            return self.IMAGEMS[3]

    def animacao(self):

        self.x -= self.velocidade
        if self.x < 0:
            self.x = 1200
    
    def mask(self):
        return pygame.mask.from_surface(self.imagem)

    def desenhar(self, tela):    
        tela.blit( self.imagem,(self.x, self.y))

class Dino:

    IMAGEM = IMAGEM_DINO
    FRAME_X = 44
    FRAME_Y = 47

    def __init__(self):
        self.x = 250
        self.y = 265
        self.imagem = self.IMAGEM
        self.sprite_atual = 1
        self.sprite_width = 44
        self.sprite_height = 47
        self.velocidade = 0
        self.gravidade = 5
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
            self.velocidade = -25
            self.pulando = True
        
        if self.pulando:
            self.y += self.velocidade
            self.velocidade += self.gravidade

            if self.y >= 265:
                self.y = 265
                self.velocidade = 0
                self.pulando = False
    
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
    DISPLAY_WIDTH = 1200
    DIPLAY_HEIGHT = 500

    display = pygame.display.set_mode((DISPLAY_WIDTH,DIPLAY_HEIGHT))
    clock = pygame.time.Clock()
    rodando = True
    pontos = 0
    game_over = Over()
    retornar = Return()
    chao = Chao()
    nuvem = Nuvem()
    cactos = [Cactos()]
    dino = Dino()
    primeiro_cacto = True

    while rodando:
    
        clock.tick(15) 

        for event in pygame.event.get():
            if event.type == QUIT:
                rodando = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:    
                    dino.pular()

        if dino.pulando:
            dino.pular()
        
        display.fill((247,247,247))

        texto = FONTE_PONTOS.render(f"SCORE {pontos}", 0,(83,83,83))
        display.blit(texto,(1000 , 100))
        

        if primeiro_cacto:
            cactos.append(Cactos())
            primeiro_cacto = False

        if cactos[0].x < 800 and len(cactos) < 2:
            cactos.append(Cactos())
           
        for cacto in cactos:
            dino.colisao(cacto)          
        if not dino.colidir:
            for cacto in cactos:
                chao.animacao()
                nuvem.animacao()
                cacto.animacao()

        for cacto in cactos:
            if cacto.x < 100:
                cacto.passou = True

        chao.desenhar(display)
        nuvem.desenhar(display)
        dino.desenhar(display)
        for cacto in cactos:
            cacto.desenhar(display)
        
        for i,cacto in enumerate(cactos):
            if cacto.passou:
                cactos.pop(i)

        if not dino.colidir:
            pontos += 1
            if pontos % 100 == 0:
                chao.VELOCIDADE += 5
                for cacto in cactos:
                    cacto.velocidade += 5
        if dino.colidir:
            game_over.desenhar(display)
            retornar.desenhar(display)
        
        pygame.display.flip()

    pygame.quit()
    exit()

if __name__ == "__main__":
    main()


