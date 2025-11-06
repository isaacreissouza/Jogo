import pygame as pg
from settings import *
from math import *

# Cria a classe do jogador:
class Player:
    def __init__(self, game):
        self.game = game
        self.x, self.y = P_POS
        self.angle = P_ANGLE
    # Função que vai definir o movimento do jogador a partir da velocidade e ângulo:
    def movement(self):
        sin_a = sin(self.angle)
        cos_a = cos(self.angle)
        dx, dy = 0, 0
        speed = P_SPEED * self.game.delta_time
        speed_sin = speed * sin_a
        speed_cos = speed * cos_a

        # Adiciona teclas pra ditar a direção e sentido da variação do movimento:
        keys = pg.key.get_pressed()
        if keys[pg.K_w]:
            dx += speed_cos
            dy += speed_sin
        if keys[pg.K_s]:
            dx += - speed_cos
            dy += - speed_sin
        if keys[pg.K_a]:
            dx += speed_sin
            dy += - speed_cos
        if keys[pg.K_d]:
            dx += - speed_sin
            dy += speed_cos

    #função para analisar a colisão com as paredes do jogo
        self.check_wall_collision(dx, dy)


        # Aplica a variação e atualiza a posição:
        """self.x += dx
        self.y += dy"""
        # Adiciona teclas pra ditar a variação do ângulo:
        """if keys[pg.K_LEFT]:
            self.angle -= P_ROT_SPEED * self.game.delta_time
        if keys[pg.K_RIGHT]:
            self.angle += P_ROT_SPEED * self.game.delta_time"""
        
        self.angle %= tau



        #checagem da localização do jogador no mapa
    def check_wall(self, x, y):
        return (x,y) not in self.game.map.world_map
    
    #definição da colisão do jogador com as paredes
    def check_wall_collision(self, dx, dy): #posição do jogador no x e y
        scale= PLAYER_SIZE_SCALE/self.game.delta_time
        if self.check_wall(int(self.x + dx*scale), int(self.y)): #chega colisão no eixo x
            self.x+= dx
        if self.check_wall(int(self.x), int(self.y + dy*scale)):#chega colisão no eixo y
            self.y+= dy

    # Função que desenha o jogador no plano e que desenha sua direção de movimento com uma linha:
    def draw(self):
        
        pg.draw.line(self.game.screen, 'yellow', (self.x * 100, self.y * 100),
                     (self.x * 100 + WIDTH * cos(self.angle),
                      self.y * 100 + WIDTH * sin(self.angle)), 2)
                      
        pg.draw.circle(self.game.screen, 'green', (self.x * 100, self.y * 100), 15)

    def mouse_control(self):#função de controle do mouse
            mx, my = pg.mouse.get_pos()#pega a posição do mouse
            if mx < MOUSE_BOURDER_LEFT or mx > MOUSE_BOURDER_RIGHT:
                pg.mouse.set_pos([HALF_WIDHT, HALF_HEIGHT])
            self.rel = pg.mouse.get_rel()[0]
            self.rel = max(-MOUSE_MAX_REL, min(MOUSE_MAX_REL, self.rel))
            self.angle += self.rel * MOUSE_SENSITIVITY * self.game.delta_time

    # Função que vai atualizar a posição do jogador a partir do movimento:
    def update(self):
        self.movement()
        self.mouse_control()
    # Função que retorna a posição em x e y:
    def pos(self):
        #posição atual do jogador 
        return self.x, self.y
    # Função que retorna a posição em x e y no mapa:
    def map_pos(self):
        #converte para inteiro
        return int(self.x), int(self.y)
    

     