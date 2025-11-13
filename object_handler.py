from sprite_object import *
from npc import *

# Classe que gerencia todos os objetos e NPCs no jogo:
class ObjectHandler: 
    def __init__(self, game): # Construtor da classes
        self.game = game
        self.sprite_list = [] # Guarda lista de sprites
        self.npc_list = [] # Guarda lista de NPCs
        self.npc_sprite_path = 'sprites/npc/' # Padroniza caminho até sprites de NPC
        self.static_sprite_path = 'sprites/sprites_rigid/' # Padroniza caminho até sprites estáticos
        self.anim_sprite_path = 'sprites/sprites_animated/' # Padroniza caminho até sprites animados
        add_sprite = self.add_sprite # Adiciona sprites
        add_npc = self.add_npc # Adiciona NPCs
        self.npc_positions = {} # Guarda posição dos NPCs no mapa

        # Mapa de sprites:
        add_sprite(SpriteObject(game))
        add_sprite(AnimatedSprite(game))
        add_sprite(AnimatedSprite(game,pos=(1.5,1.5)))
        add_sprite(AnimatedSprite(game,pos=(1.5,7.5)))
        add_sprite(AnimatedSprite(game,pos=(5.5,3.25)))
        add_sprite(AnimatedSprite(game,pos=(5.5,4.75)))
        add_sprite(AnimatedSprite(game,pos=(7.5,2.5)))
        add_sprite(AnimatedSprite(game,pos=(7.5,5.5)))
        add_sprite(AnimatedSprite(game,pos=(14.5,1.5)))
        add_sprite(AnimatedSprite(game,path=self.anim_sprite_path + 'red_light/0.png',pos=(14.5,7.5)))
        add_sprite(AnimatedSprite(game,path=self.anim_sprite_path + 'red_light/0.png',pos=(12.5,7.5)))
        add_sprite(AnimatedSprite(game,path=self.anim_sprite_path + 'red_light/0.png',pos=(9.5,7.5)))
    
        # Mapa de NPCs:
        add_npc(SoldierNPC(game, pos=(11.0, 19.0)))
        add_npc(SoldierNPC(game, pos=(11.5, 4.5)))
        add_npc(SoldierNPC(game, pos=(13.5, 6.5)))
        add_npc(SoldierNPC(game, pos=(2.0, 20.0)))
        add_npc(SoldierNPC(game, pos=(4.0, 29.0)))
        add_npc(CacoDemonNPC(game, pos=(5.5, 14.5)))
        add_npc(CacoDemonNPC(game, pos=(5.5, 16.5)))
        add_npc(CyberDemonNPC(game, pos=(14.5, 25.5)))

    # Verifica se todos os NPCs foram eliminados e mostra tela de vitória no canto superior esquerdo:
    def check_win(self): 
        if not len(self.npc_positions): # Se não houver mais NPCs vivos
            self.game.object_renderer.win() # Chama a função de vitória do renderizador
            pg.display.flip()
            pg.time.delay(1500)
            self.game.new_game()

    # Atualiza os objetos e NPCs no jogo:
    def update(self): 
        self.npc_positions = {npc.map_pos for npc in self.npc_list if npc.alive} # Cria um conjunto com as posições dos NPCs vivos
        [sprite.update() for sprite in self.sprite_list] # Atualiza todas as sprites estáticas e animadas
        [npc.update() for npc in self.npc_list] # Atualiza todos os NPCs
        self.check_win() # Verifica se o jogador venceu o jogo

    # Adiciona um NPC à lista de NPCs:
    def add_npc(self, npc): 
        self.npc_list.append(npc)

    # Adiciona uma sprite à lista de sprites:
    def add_sprite(self, sprite):
        self.sprite_list.append(sprite)