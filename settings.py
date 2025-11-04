import math


# Configurações do jogo:

RES = WIDTH, HEIGHT = 1600, 900 # Altura e largura da tela
HALF_WIDHT = WIDTH // 2 # Meia largura
HALF_HEIGHT = HEIGHT // 2 # Meia altura
FPS = 60 # Frames por segundo
P_POS = 1.5, 5 # Posição inicial do jogador em relação ao mapa
P_ANGLE = 0 # Ângulo inicial do jogador
P_SPEED = 0.004 # Velocidade do jogador
P_ROT_SPEED = 0.002 # Velocidade de rotação do jogador


FOV = math.pi / 3 # campo de visão do jogador
HALF_FOV = FOV / 2  # metade do campo de visão do jogador
NUM_RAYS = 120 # número de raios para o ray casting que utilizará na função
HALF_NUM_RAYS = NUM_RAYS // 2 # metade do número de raios
DELTA_ANGLE = FOV / NUM_RAYS # variação do ângulo entre os raios
MAX_DEPTH = 20 # distância máxima que o jogador pode enxergar

SCREEN_DIST = HALF_WIDHT / math.tan(HALF_FOV) # Distância para a localização da tela
SCALE = WIDTH // NUM_RAYS # Define uma escala para garantir melhor performance

PLAYER_SIZE_SCALE = 60  # Escala do tamanho do jogador no mapa
 

#Configurações do mouse
MOUSE_SENSITIVITY = 0.0003 # Sensibilidade ao mexer no mouse
MOUSE_MAX_REL = 40  # Máximo movimento relativo do mouse
MOUSE_BOURDER_LEFT = 100  # Limite esquerdo para o mouse
MOUSE_BOURDER_RIGHT = WIDTH - 100  # Limite direito para o mouse

FLOOR_COLOR = (30, 30, 30)  

#Tamanho da textura
TEXTURE_SIZE = 256
HALF_TEXTURE_SIZE = TEXTURE_SIZE // 2   #metade do tamanho da textura
