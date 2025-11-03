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