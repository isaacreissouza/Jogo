import pygame as pg
from settings import *
import os
from collections import deque

# Adiciona sprites:
class SpriteObject:
    def __init__(self, game, path='sprites/sprites_rigid/candlebra.png', # Define caminho, escala, posição e shift em y 
                 pos=(10.5,3.5), scale=0.7, shift=0.27):
        self.game = game
        self.player = game.player
        self.x, self.y = pos
        self.image = pg.image.load(path).convert_alpha()
        self.IMAGE_WIDTH = self.image.get_width() # Pega largura da imagem
        self.IMAGE_HALF_WIDTH = self.image.get_width() // 2 # Pega metade de tal
        self.IMAGE_RATIO = self.IMAGE_WIDTH / self.image.get_height() # Pega a razão da imagem
        self.dx, self.dy, self.theta, self.screen_x, self.dist, self.norm_dist = 0, 0, 0, 0, 1, 1 # Define ângulos e distâncias
        self.sprite_half_width = 0 # Define meia largura como 0
        self.SPRITE_SCALE = scale # Define escala
        self.SPRITE_HEIGHT_SHIFT = shift # Define movimentação no eixo y

    # Função que adquire a projeção do sprite no ambiente 3D:
    def get_sprite_projection(self):
        proj = SCREEN_DIST / self.norm_dist * self.SPRITE_SCALE # Define a projeção
        proj_width, proj_height = proj * self.IMAGE_RATIO, proj # Define largura e altura

        image = pg.transform.scale(self.image, (proj_width, proj_height)) # Deixa a imagem em escala

        self.sprite_half_width = proj_width // 2
        height_shift = proj_height * self.SPRITE_HEIGHT_SHIFT # Adquire mudança em altura
        pos = self.screen_x - self.sprite_half_width, HALF_HEIGHT - proj_height // 2 + height_shift # Adquire a posição do sprite

        self.game.raycasting.objects_to_render.append((self.norm_dist, image, pos)) # Projeta com o raycast em ambiente 3D

    # Adquire o sprite:
    def get_sprite(self):
        dx = self.x - self.player.x # Define x do sprite
        dy = self.y - self.player.y # Define y do sprite
        self.dx, self.dy = dx, dy # Defina a dx e a dy
        self.theta = math.atan2(dy, dx) # Usa dx e dy pra adquirir o ângulo entre eles

        delta = self.theta - self.player.angle # Com o ângulo, adquire o delta
        if (dx > 0 and self.player.angle > math.pi) or (dx < 0 and dy < 0):
            delta += math.tau # Soma tau a delta se o ângulo for maior que pi se dx for maior que 0 ou dx e dy forem negativos
        
        delta_rays = delta / DELTA_ANGLE # Projeção dos raios do raycast
        self.screen_x = (HALF_NUM_RAYS + delta_rays) * SCALE # X da tela calculado pelos rays

        self.dist = math.hypot(dx,dy) # Adquire distância
        self.norm_dist = self.dist * math.cos(delta) # Adquire distância normal
        if -self.IMAGE_HALF_WIDTH < self.screen_x < (WIDTH + self.IMAGE_HALF_WIDTH) and self.norm_dist > 0.5:
            self.get_sprite_projection() 

    # Atualiza os sprites de acordo com a projeção do raycast:
    def update(self):
        self.get_sprite()

# Classe para sprites animados, herdando a classe anterior:
class AnimatedSprite(SpriteObject):
    def __init__(self, game, path='sprites/sprites_animated/green_light/0.png', # Define caminho, escala, posição e shift em y e tempo da animação
                 pos=(11.5, 3.5), scale=0.8, shift=0.15, animation_time=120):
        super().__init__(game, path, pos, scale, shift)
        self.animation_time = animation_time # Tempo de animação
        self.path = path.rsplit('/', 1)[0] # Separador pra gerar animação
        self.images = self.get_images(self.path) # Define imagens
        self.animation_time_prev = pg.time.get_ticks() # Tempo de animação
        self.animation_trigger = False # Começa a animação se for True

    # Atualiza o sprite:
    def update(self):
        super().update()
        self.check_animation_time() # Checa tempo de animação
        self.animate(self.images) # Anima
    
    # Função que irá animar:
    def animate(self, images):
        if self.animation_trigger:
            images.rotate(-1) # Rotaciona entre as imagens da pasta, gerando movimento
            self.image = images[0]
    
    # Checa tempo de animação:
    def check_animation_time(self):
        self.animation_trigger = False
        time_now = pg.time.get_ticks()
        if time_now - self.animation_time_prev > self.animation_time: # Se tempo estiver aceitável
            self.animation_time_prev = time_now # Usa os ticks atuais (pois estão corretos)
            self.animation_trigger = True # Anima
    
    # Adquire as imagens da pasta
    def get_images(self, path):
        images = deque()
        for file_name in os.listdir(path):
            if os.path.isfile(os.path.join(path, file_name)): # Adquire as imagens da pasta
                img = pg.image.load(path + '/' + file_name).convert_alpha()
                images.append(img)
        return images # Retornas as imagens pra serem animadas
