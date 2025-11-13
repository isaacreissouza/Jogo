from sprite_object import *
from collections import deque
import pygame as pg


class Weapon(AnimatedSprite): #é uma sprite animada que representa a arma do jogador
    # funcao de inicialização da arma, determinando a posiçao, escala e tempo de animação
    def __init__(self, game, path='sprites/sprites_animated/shotgun/0.png', scale=0.4, animation_time=90):
        super().__init__(game=game, path=path, scale=scale, animation_time=animation_time)
        self.images=deque(
            [pg.transform.smoothscale(img, (self.image.get_width()*scale, self.image.get_height()*scale)) #redimensiona cada imagem da animação
            for img in self.images])
        self.weapon_pos = (HALF_WIDHT - self.images[0].get_width() // 2, HEIGHT - self.images[0].get_height())
        self.reloading = False
        self.num_images = len(self.images) # número de imagens na animação da arma
        self.frame_counter = 0  
        self.damage = 50  # dano causado pela arma

    def animate_shot(self): # anima a arma quando o jogador atira ou seja clicar no mouse
        if self.reloading:
            self.game.player.shot = False #reseta o estado de tiro do jogador, para não ocorrer múltiplos tiros
            if self.animation_trigger:# verifica se é hora de atualizar a animação
                self.images.rotate(-1) # rotaciona as imagens para a próxima na animação, depois do tiro a arma volta para a posição inicial, ja que assume rotaçao para carregamento
                self.image = self.images[0]
                self.frame_counter += 1
                if self.frame_counter == self.num_images:
                    self.reloading = False # termina a animação de recarregamento
                    self.frame_counter = 0 # reseta o contador para o proximo tiro

    def draw(self):
        self.game.screen.blit(self.images[0], self.weapon_pos) #Desenha a imagem atual da arma na tela

    def update(self): #atualiza a animação da arma
        self.check_animation_time()
        self.animate_shot()