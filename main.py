import pygame as pg

class Game:
    # Inicia o jogo e define parâmetros base (Resolução e FPS):
    def __init__(self):
        pg.init() # Começa a operação do jogo
        self.screen = pg.display.set_mode() # Define uma variável pra tela (Botar "RES" nos () depois que criar arquivo settings)
        self.clock = pg.time.Clock() # Define uma variável pro clock
    # Cria novo jogo :
    def new_game(self):
        pass # Depois adiciona coisas
    # Atualiza as informações da tela:
    def update(self):
        pg.display.flip()
        self.clock.tick() # Botar "FPS" depois que criar e definir no arquivo settings
        pg.display.set_caption(f'{self.clock.get_fps() :.1f}') # Mostra FPS na tela
    # Desenha coisas na tela:
    def draw(self):
        self.screen.fill('red') # Pinta a tela de vermelho (mudar dps)
    # Verifica interações do usuário:
    def check_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.type == pg.K_ESCAPE): # Permite fechar o jogo
                pg.quit()
    # Loop que roda o jogo:
    def run(self):
        while True:
            self.update() # Atualiza
            self.draw() # Desenha
