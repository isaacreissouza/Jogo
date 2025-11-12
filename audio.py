import pygame as pg
import os

class Sound: #classe de som
    def __init__(self, game):

        self.game= game 
        pg.mixer.init() #funcionalidade do som
        self.path= 'sound/'
        self.shotgun= pg.mixer.Sound(self.path + 'resources_sound_shotgun.wav')
 