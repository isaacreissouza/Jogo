import pygame as pg
from settings import *


# Classe que define o que será renderizado na tela e que vai desenhar todos os elementos gráficos:
class ObjectRenderer:
    def __init__(self, game):
        self.game= game
        self.screen= game.screen
        self.wall_textures=self.load_wall_textures() # Carrega as texturas das paredes

        self.sky_image= self.get_texture('textures/sky.png', (WIDTH, HALF_HEIGHT)) # Carrega o fundo do céu (que se move conforme o jogador gira) 
        self.sky_offset = 0 # Adiciona o efeito de rolagem (scroll lateral do céu)
        self.blood_screen = self.get_texture('textures/blood_screen.png', RES) # Imagem que aparece quando o jogador leva dano
        self.digit_size = 90 # Tamanho dos dígitos da vida no canto superior esquerdo
        self.digit_images = [self.get_texture(f'textures/digits/{i}.png', [self.digit_size] * 2) # Carrega as imagens dos dígitos de 0 a 9 e % 
                             for i in range(11)]
        self.digits = dict(zip(map(str, range(11)), self.digit_images)) # Dicionário que mapeia os dígitos para suas imagens correspondentes
        self.game_over_image = self.get_texture('textures/game_over.png', RES) # Tela de game over
        self.win_image = self.get_texture('textures/win.png') # Tela de vitória

    # Desenhae na tela:
    def draw(self):
        self.draw_background() # Desenha o fundo do céu e o chão
        self.render_game_objects() # Desenha os objetos do jogo (paredes, sprites, etc.)
        self.draw_player_health() # Desenha a "saúde" do jogador na tela

    # Tela de vitória:
    def win(self): 
         self.screen.blit(self.win_image, (0,0))

    # Tela de game over:
    def game_over(self): 
         self.screen.blit(self.game_over_image, (0,0))

    # Desenha a "saúde" do jogador na tela:
    def draw_player_health(self): 
        health = str(self.game.player.health)
        for i, char in enumerate(health): # Itera sobre cada caractere na string de saúde
              self.screen.blit(self.digits[char], (i * self.digit_size, 0))
        self.screen.blit(self.digits['10'], ((i + 1) * self.digit_size, 0))

    # Efeito de dano na tela:
    def player_damage(self): 
         self.screen.blit(self.blood_screen, (0,0))
        
    # Desenho do fundo: 
    def draw_background(self):
        self.sky_offset=(self.sky_offset + 4.0 * self.game.player.rel) % WIDTH # Movimentação do céu conforme o jogador gira
        self.screen.blit(self.sky_image, (-self.sky_offset, 0)) # Desenha o ceu
        self.screen.blit(self.sky_image, (-self.sky_offset + WIDTH, 0)) 
        pg.draw.rect(self.screen, FLOOR_COLOR, (0, HALF_HEIGHT, WIDTH, HALF_HEIGHT)) 


    # Desenha os objetos do jogo (paredes, sprites, etc.):
    def render_game_objects(self): 
            list_objects = sorted(self.game.raycasting.objects_to_render,key=lambda t: t[0], reverse=True) # Ordena os objetos pela distância do jogador (do mais distante para o mais próximo)
            for depth, image, pos in list_objects:
                self.screen.blit(image, pos) # Adiciona imagem na posição

    # Carrega a textura da parede:
    def get_texture(self,path, res=(TEXTURE_SIZE, TEXTURE_SIZE)): 
        texture= pg.image.load(path).convert_alpha() # Carrega a imagem e converte para efeito alpha
        return pg.transform.scale(texture, res) # Redimensiona a textura para a resolução especificada
    
    # Carrega as texturas das paredes do jogo:
    def load_wall_textures(self): 
        return {
            1: self.get_texture('textures/1.png'),
            2: self.get_texture('textures/2.png'),
            3: self.get_texture('textures/3.png'),
            4: self.get_texture('textures/4.png'),
            5: self.get_texture('textures/5.png'),
        }


