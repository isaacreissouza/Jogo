import pygame as pg
import os

# Classe de som:
class Sound:
    def __init__(self, game):

        self.game= game 
        pg.mixer.init() # Inicializa funcionalidade do som
        self.path= 'sound/' # Padroniza o caminho em que os sons ficam
        self.shotgun= pg.mixer.Sound(self.path + 'resources_sound_shotgun.wav') # Som do tiro
        self.npc_pain = pg.mixer.Sound(self.path + 'npc_pain.wav') # Som de dano do NPC
        self.npc_death = pg.mixer.Sound(self.path + 'npc_death.wav') # Som de morte do NPC
        self.npc_shot = pg.mixer.Sound(self.path + 'npc_attack.wav') # Som de ataque do NPC
        self.player_pain = pg.mixer.Sound(self.path + 'player_pain.wav') # Som de dano do jogador
        self.theme = pg.mixer.music.load(self.path + 'theme.mp3') # Música
        pg.mixer.music.set_volume(0.3) # Volume
 