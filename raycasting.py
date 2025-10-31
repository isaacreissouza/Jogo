import pygame as pg
import math
from settings import *


#mapeando a percepção do jogador no mapa
class RayCasting:
    def __init__(self, game):
        self.game = game


    def ray_cast(self):
        ox, oy= self.game.player.map_pos #pega a posição x e y do jogador
        x_map, y_map= self.game.player.map_pos #mapeia essas posições onde o jogador se deslocar

        ray_angle= self.game.player.angle - HALF_FOV + 0.0001 #angulo que o jogador se deslocar
        for ray in range(NUM_RAYS):#loop de rios na deslocação do jogador, no caso vamos necessitar do seno e cosseno
            sin_a= math.sin(ray_angle)
            cos_a= math.cos(ray_angle)

            #mapear o jogador na horizontal
            y_hor, dy= (y_map +1, 1) if sin_a>0 else (y_map - 1e-6, -1)
            depth_hor= (y_hor - oy)/ sin_a
            x_hor= ox + depth_hor * cos_a
            delta_depth= dy/ sin_a
            dx= delta_depth * cos_a

            for i in range(MAX_DEPTH): #loop da distancia maxima do jogador pode enxergar na horizontal
                tile_hor= int(x_hor), int(y_hor)
                if tile_hor in self.game.map.world_map: 
                    break
                x_hor += dx
                y_hor += dy
                depth_hor += delta_depth

            #mapear o jogador na vertical
            x_vert, dx= (x_map +1, 1) if cos_a>0 else (x_map - 1e-6, -1)
            depth_vert= (x_vert - ox)/ cos_a
            y_vert= oy + depth_vert * sin_a
            delta_depth= dx/ cos_a
            dy= delta_depth * sin_a

            for i in range(MAX_DEPTH): #loop da distancia maxima do jogador pode enxergar na vertical
                tile_vert= int(x_vert), int(y_vert)
                if tile_vert in self.game.map.world_map:
                    break
                x_vert += dx
                y_vert += dy
                depth_vert += delta_depth

            #definindo a menor distância entre as duas direções
            if depth_vert < depth_hor:
                depth= depth_vert
            else:
                depth= depth_hor

            # desenho para a indicação do jogador no mapa 
            pg.draw.line(self.game.screen, 'yellow', (100 * ox, 100 * oy),
                         (100 * (ox + depth * cos_a), 100 * (oy + depth * sin_a)), 2)

            #proximo ângulo do raio
            ray_angle += DELTA_ANGLE

    def update(self):
        self.ray_cast()# chama a função ray cast
        