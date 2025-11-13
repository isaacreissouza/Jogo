from sprite_object import *
from npc import *

class ObjectHandler: # classe que gerencia todos os objetos e NPCs no jogo
    def __init__(self, game): # construtor da classe
        self.game = game
        self.sprite_list = []
        self.npc_list = []
        self.npc_sprite_path = 'sprites/npc/'
        self.static_sprite_path = 'sprites/sprites_rigid/'
        self.anim_sprite_path = 'sprites/sprites_animated/'
        add_sprite = self.add_sprite
        add_npc = self.add_npc
        self.npc_positions = {}

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

    def spawn_npc(self): # Função para spawnar NPCs aleatoriamente no mapa
        for i in range(self.enemies):# número de inimigos a serem spawnados
                npc = choices(self.npc_types, self.weights)[0]
                pos = x, y = randrange(self.game.map.cols), randrange(self.game.map.rows)
                while (pos in self.game.map.world_map) or (pos in self.restricted_area): # verifica se a posição não é uma parede ou área restrita
                    pos = x, y = randrange(self.game.map.cols), randrange(self.game.map.rows)
                self.add_npc(npc(self.game, pos=(x + 0.5, y + 0.5)))# adiciona o NPC na posição gerada

    def check_win(self): #verifica se todos os NPCs foram eliminados
        if not len(self.npc_positions): #se não houver mais NPCs vivos
            self.game.object_renderer.win() #chama a função de vitória do renderizador
            pg.display.flip()
            pg.time.delay(1500)
            self.game.new_game()

    def update(self): #atualiza os objetos e NPCs no jogo
        self.npc_positions = {npc.map_pos for npc in self.npc_list if npc.alive}# cria um conjunto com as posições dos NPCs vivos
        [sprite.update() for sprite in self.sprite_list]# atualiza todas as sprites estáticas e animadas
        [npc.update() for npc in self.npc_list]# atualiza todos os NPCs
        self.check_win()# verifica se o jogador venceu o jogo


    def add_npc(self, npc): #adiciona um NPC à lista de NPCs
        self.npc_list.append(npc)# adiciona o NPC à lista de NPCs

    def add_sprite(self, sprite):# adiciona uma sprite à lista de sprites
        self.sprite_list.append(sprite)