import pygame as pg

class Sound: #classe de som
    def _init_(self,game): 
        self.game= game 
        pg.mixer.init() #funcionalidade do som
        self.path= 'sound/'
        self.shotgun= pg.mixer.Sound(self.path + 'shotgun.wav')
 