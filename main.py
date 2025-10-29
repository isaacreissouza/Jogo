import pygame as pg
from settings import *
class Game:
    # Inicia o jogo e define parâmetros base (Resolução e FPS):
    def __init__(self):
        pg.init() # Começa a operação do jogo
        self.screen = pg.display.set_mode(RES) # Define uma variável pra tela
        self.clock = pg.time.Clock() # Define uma variável pro clock
    # Cria novo jogo :
    def new_game(self):
        pass # Depois adiciona coisas
    # Atualiza as informações da tela:
    def update(self):
        pg.display.flip()
        self.clock.tick(FPS)
        pg.display.set_caption(f'{self.clock.get_fps() :.1f}') # Mostra FPS na tela
    # Função que desenha coisas na tela:
    def draw(self):
        self.screen.fill('red') # Pinta a tela de vermelho (mudar dps)
    # Função que verifica interações do usuário:
    def check_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.type == pg.K_ESCAPE): # Permite fechar o jogo
                pg.quit()
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