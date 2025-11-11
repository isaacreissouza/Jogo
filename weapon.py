from sprite_object import *
from collections import deque
import pygame as pg


class Weapon (AnimatedSprite):
    def ___init___(self, game, path='sprites/sprites_animated/shotgun/0.png', scale=0.4, animation_time=90):
        super()._init_(game=game, path=path, scale=scale, animation_time=animation_time)
        self.images=deque(
            [pg.transform.smoothscale(img, (self.image.get_width()*scale,
                                                self.image.get_height()*scale)) 
                 for img in self.images])
        
        self.weapon_pos = (HALF_HEIGHT - self.images[0].get_width() // 2, HEIGHT - self.images[0].get_height())
        self.reloading = False
        self.num_images=len(self.images) # número de imagens na animação da arma
        self.frame_counter = 0  
        self.damage = 50  # dano causado pela arma



    def animate_shot(self):
        if self.reloading:
            self.game.player.shot= False
            if self.animation_trigger:
                self.images.rotate(-1)
                self.image = self.images[0]
                self.frame_counter += 1
                if self.frame_counter == self.num_images:
                
                    self.reloading = False
                    self.frame_counter = 0

        
            
    def draw(self):
        self.game.screen.blit(self.images[0], self.weapon_pos)

    def update(self):
        self.check_animation_time()
        self.animate_shot()
        