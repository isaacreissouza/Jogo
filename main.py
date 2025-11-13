import pygame as pg
from settings import *
from map import *
from player import *
from raycasting import *
from object_render import *
import sys
from sprite_object import *
from object_handler import *
from weapon import *
from audio import Sound
from pathfinding import *

class Game:
    # Inicia o jogo e define parâmetros base (Resolução e FPS):
    def __init__(self):
        pg.init() # Começa a operação do jogo
        pg.mouse.set_visible(False) # Esconde o cursor do mouse
        self.screen = pg.display.set_mode(RES) # Define uma variável pra tela
        self.clock = pg.time.Clock() # Define uma variável pro clock
        self.delta_time = 1 # Define o tempo que passa entre frames 
        self.global_trigger = False # Variável usada na padronização de funções de eventos e animações
        self.global_event = pg.USEREVENT + 0 # Variável usada na padronização de funções de eventos e animações
        pg.time.set_timer(self.global_event, 40) # Adiciona um timer padronizado pra animação
        self.new_game()

    # Cria novo jogo:
    def new_game(self):
        self.map = Map(self) # Adiciona o mapa
        self.player = Player(self) # Adiciona o jogador
        self.object_renderer = ObjectRenderer(self) # Classe de renderização de objetos
        self.raycasting= RayCasting(self) # Classe de raycasting
        self.object_handler = ObjectHandler(self) # Classe que adiciona sprites e npcs
        self.weapon = Weapon(self) # Adiciona a arma
        self.sound = Sound(self) # Adiciona o som
        self.pathfinding = PathFinding(self) # Adiciona pathfinding
        pg.mixer.music.play(-1) # Toca a música

    # Atualiza as informações da tela:
    def update(self):
        self.player.update() # Atualiza o jogador
        self.raycasting.update() # Atualiza o raycasting
        self.object_handler.update() # Atualiza os sprites e texturas
        self.weapon.update() # Atualiza a arma
        pg.display.flip() # Atualiza a tela toda
        self.delta_time = self.clock.tick(FPS) # Torna a velocidade independente do FPS
        pg.display.set_caption(f'{self.clock.get_fps() :.1f}') # Mostra FPS na tela

    # Função que desenha coisas na tela:
    def draw(self):
        self.object_renderer.draw() # Desenha os objetos na tela
        self.weapon.draw() # Desenha a arma na tela
        pg.display.flip()
        
    # Função que verifica interações do usuário:
    def check_events(self):
        self.global_trigger = False
        for event in pg.event.get():
            if event.type == pg.QUIT: # Permite fechar o jogo
                pg.quit()
                sys.exit()
            elif event.type == self.global_event: # Marca a ocorrência de eventos
                self.global_trigger = True
            self.player.single_fire_event(event) # Tiro do jogador
           
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