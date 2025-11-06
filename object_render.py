import pygame as pg
from settings import *


#O que será renderizado na tela
class ObjectRenderer:
    def __init__(self, game):
        self.game= game
        self.screen= game.screen
        self.wall_textures=self.load_wall_textures() #texturas das paredes

        self.sky_image= self.get_texture('textures/sky.png', (WIDTH, HALF_HEIGHT))#.convert()
        self.sky_offset=0


        #Desenhae na tela
    def draw(self):
        self.draw_background()
        self.render_game_objects()


        #Desenho do fundo 
    def draw_background(self):
        self.sky_offset=(self.sky_offset + 4.0 * self.game.player.rel) % WIDTH
        self.screen.blit(self.sky_image, (-self.sky_offset, 0)) #desenha o ceu
        self.screen.blit(self.sky_image, (-self.sky_offset + WIDTH, 0)) 
        pg.draw.rect(self.screen, FLOOR_COLOR, (0, HALF_HEIGHT, WIDTH, HALF_HEIGHT)) 


    def render_game_objects(self):
            list_objects=self.game.raycasting.objects_to_render
            for depth, image, pos in list_objects:
                self.screen.blit(image, pos) #adiciona imagem na posição

    def get_texture(self,path, res=(TEXTURE_SIZE, TEXTURE_SIZE)):
        #Carrega a imagem e converte para efeito alpha
        texture= pg.image.load(path).convert_alpha()
        #converte a resolução da imagem
        return pg.transform.scale(texture, res)
    

    def load_wall_textures(self):
        return {
            1: self.get_texture('textures/1.png'),
            2: self.get_texture('textures/2.png'),
            3: self.get_texture('textures/3.png'),
            4: self.get_texture('textures/4.png'),
            5: self.get_texture('textures/5.png'),
        }


