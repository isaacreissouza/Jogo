import pygame as pg
from settings import *


#O que será renderizado na tela
#desenhar todos os elementos gráficos
class ObjectRenderer:
    def __init__(self, game):
        self.game= game
        self.screen= game.screen
        self.wall_textures=self.load_wall_textures() #texturas das paredes

        self.sky_image= self.get_texture('textures/sky.png', (WIDTH, HALF_HEIGHT))#Carrega o fundo do céu (que se move conforme o jogador gira).sky_offset é usado para o efeito de rolagem (scroll lateral do céu).
        self.sky_offset=0
        self.blood_screen = self.get_texture('textures/blood_screen.png', RES) #imagem que aparece quando o jogador leva dano
        self.digit_size = 90
        self.digit_images = [self.get_texture(f'textures/digits/{i}.png', [self.digit_size] * 2) # carrega as imagens dos dígitos de 0 a 10
                             for i in range(11)]
        self.digits = dict(zip(map(str, range(11)), self.digit_images)) #dicionário que mapeia os dígitos para suas imagens correspondentes
        self.game_over_image = self.get_texture('textures/game_over.png', RES) #imagem de game over
        self.win_image = self.get_texture('textures/win.png') #imagem de vitória
        #Desenhae na tela
    def draw(self):
        self.draw_background()#desenha o fundo do céu e o chão
        self.render_game_objects()#desenha os objetos do jogo (paredes, sprites, etc.)
        self.draw_player_health()#desenha a "saúde" do jogador na tela

    def win(self): # tela de vitória
         self.screen.blit(self.win_image, (0,0))

    def game_over(self): #tela de game over
         self.screen.blit(self.game_over_image, (0,0))

    def draw_player_health(self): #desenha a "saúde" do jogador na tela
        health = str(self.game.player.health)
        for i, char in enumerate(health): #itera sobre cada caractere na string de saúde
              self.screen.blit(self.digits[char], (i * self.digit_size, 0))
        self.screen.blit(self.digits['10'], ((i + 1) * self.digit_size, 0))

    def player_damage(self): # efeito de dano na tela
         self.screen.blit(self.blood_screen, (0,0))
        #Desenho do fundo 
    def draw_background(self):
        self.sky_offset=(self.sky_offset + 4.0 * self.game.player.rel) % WIDTH# movimentação do céu conforme o jogador gira
        self.screen.blit(self.sky_image, (-self.sky_offset, 0)) #desenha o ceu
        self.screen.blit(self.sky_image, (-self.sky_offset + WIDTH, 0)) 
        pg.draw.rect(self.screen, FLOOR_COLOR, (0, HALF_HEIGHT, WIDTH, HALF_HEIGHT)) 


    def render_game_objects(self): #desenha os objetos do jogo (paredes, sprites, etc.)
            list_objects = sorted(self.game.raycasting.objects_to_render,key=lambda t: t[0], reverse=True) #ordena os objetos pela distância do jogador (do mais distante para o mais próximo)
            for depth, image, pos in list_objects:
                self.screen.blit(image, pos) #adiciona imagem na posição

    def get_texture(self,path, res=(TEXTURE_SIZE, TEXTURE_SIZE)): #carrega a textura da parede
        #Carrega a imagem e converte para efeito alpha
        texture= pg.image.load(path).convert_alpha()
        #converte a resolução da imagem
        return pg.transform.scale(texture, res) #redimensiona a textura para a resolução especificada
    

    def load_wall_textures(self): #carrega as texturas das paredes do jogo
        return {
            1: self.get_texture('textures/1.png'),
            2: self.get_texture('textures/2.png'),
            3: self.get_texture('textures/3.png'),
            4: self.get_texture('textures/4.png'),
            5: self.get_texture('textures/5.png'),
        }


