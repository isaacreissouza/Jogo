import pygame as pg
from settings import *
from math import *

# Cria a classe do jogador:
class Player:
    def __init__(self, game):
        self.game = game
        self.x, self.y = P_POS # Posição do jogador em x e y
        self.angle = P_ANGLE # Ângulo do jogador
        self.shot = False # Se for True, significa que o jogador atirou
        self.health = PLAYER_MAX_HEALTH # Vida inicial do jogador:
    
    # Verifica se o jogador morreu:
    def check_game_over(self):
        if self.health < 1: # Se a vida for 0 
            self.game.object_renderer.game_over() # Desenhar tela de game over
            pg.display.flip() # Atualizar a tela pra mostrar o game over
            pg.time.delay(1500)
            self.game.new_game() # Fechar o jogo após delay de 1,5s

    # Faz jogador tomar dano:
    def get_damage(self, damage):
        self.health -= damage # Retira dano da vida
        self.game.object_renderer.player_damage() # Mostra indicador de dano
        self.game.sound.player_pain.play() # Toca som de dor
        self.check_game_over() # Vê se jogador morreu
    
    # Clicar no botão do mouse para atirar:
    def single_fire_event(self,event):
        if event.type == pg.MOUSEBUTTONDOWN: # Se apertar botão do mouse
            if event.button == 1 and not self.shot and not self.game.weapon.reloading:
                self.game.sound.shotgun.play() # Executa o som do tiro quando atira
                self.shot = True # Torna tiro verdadeiro
                self.game.weapon.reloading = True # Torna recarregamento verdadeiro

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
        if keys[pg.K_w]: # W pra ir pra frente
            dx += speed_cos
            dy += speed_sin
        if keys[pg.K_s]: # S para ir pra trás
            dx += - speed_cos
            dy += - speed_sin
        if keys[pg.K_a]: # A para ir pra esquerda
            dx += speed_sin
            dy += - speed_cos
        if keys[pg.K_d]: # D para ir pra direita
            dx += - speed_sin
            dy += speed_cos

        self.check_wall_collision(dx, dy) # Analisar a colisão com as paredes do jogo


        # Aplica a variação e atualiza a posição:
        """self.x += dx
        self.y += dy"""
        # Adiciona teclas pra ditar a variação do ângulo:
        """if keys[pg.K_LEFT]:
            self.angle -= P_ROT_SPEED * self.game.delta_time
        if keys[pg.K_RIGHT]:
            self.angle += P_ROT_SPEED * self.game.delta_time"""
        
        self.angle %= tau # Ajusta ângulo de acordo com movimentação



    # Checagem se é parede:
    def check_wall(self, x, y):
        return (x,y) not in self.game.map.world_map
    
    # Definição da colisão do jogador com as paredes:
    def check_wall_collision(self, dx, dy): # Posição do jogador no x e y
        scale= PLAYER_SIZE_SCALE/self.game.delta_time # Define escala
        if self.check_wall(int(self.x + dx*scale), int(self.y)): # Checa colisão no eixo x
            self.x+= dx
        if self.check_wall(int(self.x), int(self.y + dy*scale)): # Checa colisão no eixo y
            self.y+= dy

    # Função de controle do mouse:
    def mouse_control(self):
            mx, my = pg.mouse.get_pos() # Pega a posição do mouse
            if mx < MOUSE_BOURDER_LEFT or mx > MOUSE_BOURDER_RIGHT:
                pg.mouse.set_pos([HALF_WIDHT, HALF_HEIGHT]) # Coloca mouse no centro da tela
            self.rel = pg.mouse.get_rel()[0] # Adquire movimento do mouse
            self.rel = max(-MOUSE_MAX_REL, min(MOUSE_MAX_REL, self.rel)) # Transforma movimento em dado pra ser processado
            self.angle += self.rel * MOUSE_SENSITIVITY * self.game.delta_time # Adquire o ângulo do movimento

    # Função que vai atualizar a posição do jogador a partir do movimento:
    def update(self):
        self.movement()
        self.mouse_control()

    # Função que retorna a posição em x e y:
    def pos(self):
        return self.x, self.y
    
    # Função que retorna a posição em x e y no mapa:
    def map_pos(self):
        return int(self.x), int(self.y) # Converte para inteiro