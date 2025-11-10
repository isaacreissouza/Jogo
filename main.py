import pygame as pg
from settings import *
from map import *
from player import *
from raycasting import *
from object_render import *
import sys
from sprite_object import *
from object_handler import *

class Game:
    # Inicia o jogo e define parâmetros base (Resolução e FPS):
    def __init__(self):
        pg.init() # Começa a operação do jogo
        pg.mouse.set_visible(False) # Esconde o cursor do mouse
        self.screen = pg.display.set_mode(RES) # Define uma variável pra tela
        self.clock = pg.time.Clock() # Define uma variável pro clock
        self.delta_time = 1 # Define o tempo que passa entre frames 
        self.new_game()
    # Cria novo jogo:
    def new_game(self):
        self.map = Map(self) # Adiciona o mapa
        self.player = Player(self) # Adiciona o jogador
        self.object_renderer = ObjectRenderer(self) #classe de renderização de objetos
        #classe de raycasting
        self.raycasting= RayCasting(self)
        self.object_handler = ObjectHandler(self)
    # Atualiza as informações da tela:
    def update(self):
        self.player.update() # Atualiza o jogador
        self.raycasting.update() #atualiza o raycasting
        self.object_handler.update()
        pg.display.flip()
        self.delta_time = self.clock.tick(FPS) # Torna a velocidade independente do FPS
        pg.display.set_caption(f'{self.clock.get_fps() :.1f}') # Mostra FPS na tela
    # Função que desenha coisas na tela:
    def draw(self):
        #self.screen.fill('black') # Pinta a tela de vermelho (mudar dps)
        # self.map.draw() # Desenha o mapa na tela para debug
        # self.player.draw() # Desenha o jogador na tela para debug
        self.object_renderer.draw() # Desenha os objetos na tela
        pg.display.flip()
#TALVEZ EU TIRE ESSA LINHA DEPOIS
    # Função que verifica interações do usuário:
    def check_events(self):
        for event in pg.event.get():
            # fechar janela ou pressionar ESC
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
           
    # Função com o loop que roda o jogo:
    def run(self):
        while True:
            self.check_events() # Checa os eventos
            self.update() # Atualiza
            self.draw() # Desenha

# Cria instância do jogo:
if __name__ == '__main__':
    game = Game()
    game.run() # Roda o jogo