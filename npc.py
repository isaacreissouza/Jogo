from sprite_object import *
from random import randint, random, choices, randrange

class NPC(AnimatedSprite): #A classe herda de AnimatedSprite, o que significa que cada NPC é um sprite animado


    # Função de inicialização do NPC, definindo sua posição, escala, tempo de animação e carregando as imagens de animação
    def __init__(self, game, path='sprites/npc/soldier/0.png', pos=(10.5, 5.5), scale=0.6, shift=0.38, animation_time=180):
        super().__init__(game, path, pos, scale, shift, animation_time)
        self.attack_images = self.get_images(self.path + '/attack')
        self.death_images = self.get_images(self.path + '/death')
        self.idle_images = self.get_images(self.path + '/idle')
        self.pain_images = self.get_images(self.path + '/pain')
        self.walk_images = self.get_images(self.path + '/walk')

        self.attack_dist = randint(3, 6)
        self.speed = 0.03
        self.size = 10
        self.health = 100
        self.attack_damage = 10
        self.accuracy = 0.15
        self.alive = True
        self.pain = False
        self.ray_cast_value = False
        self.frame_counter = 0
        self.player_search_trigger = False
    # atualiza a lógica do NPC a cada frame do jogo
    def update(self):
        self.check_animation_time()
        self.get_sprite()
        self.run_logic()
        #self.draw_ray_cast() # Desenha linha de visão no inimigo na tela pra debug
    # verifica se o NPC colidiu com uma parede
    def check_wall(self, x, y):
        return (x,y) not in self.game.map.world_map
    
    #definição da colisão do npc com as paredes
    def check_wall_collision(self, dx, dy): #posição do npc no x e y
        
        if self.check_wall(int(self.x + dx*self.size), int(self.y)): #chega colisão no eixo x
            self.x+= dx
        if self.check_wall(int(self.x), int(self.y + dy*self.size)):#chega colisão no eixo y
            self.y+= dy

    # Obtém a próxima posição até o jogador usando o sistema de pathfinding (BFS)
    def movement(self):
        next_pos = self.game.pathfinding.get_path(self.map_pos, self.game.player.map_pos()) 
        next_x, next_y = next_pos
        if next_pos not in self.game.object_handler.npc_positions:#verifica se a próxima posição não está ocupada por outro NPC
            # Calcula o ângulo em direção à próxima posição e move o NPC nessa direção 
            angle = math.atan2(next_y + 0.5 - self.y, next_x + 0.5 - self.x)
            dx = math.cos(angle) * self.speed
            dy = math.sin(angle) * self.speed
            self.check_wall_collision(dx,dy)

    def attack(self): #função de ataque do NPC
            #Toca o som de tiro com base na probabilidade (accuracy), causa dano ao jogador
        if self.animation_trigger:
            self.game.sound.npc_shot.play()
            if random() < self.accuracy:
                self.game.player.get_damage(self.attack_damage)
    def animate_death(self): #Roda os frames de morte uma vez (não em loop) até o inimigo desaparecer
        if not self.alive:
            if self.game.global_trigger and self.frame_counter < len(self.death_images) - 1:
                self.death_images.rotate(-1)
                self.image = self.death_images[0]
                self.frame_counter += 1
    def animate_pain(self):#Executa animação de dor e depois retorna ao comportamento normal
        self.animate(self.pain_images)
        if self.animation_trigger:
            self.pain = False
    
    def check_hit_in_npc(self): #verifica se o NPC foi atingido pelo tiro do jogador
        if self.ray_cast_value and self.game.player.shot:#verifica se o NPC está na linha de visão do jogador e se o jogador atirou
            if HALF_WIDHT - self.sprite_half_width < self.screen_x < HALF_WIDHT + self.sprite_half_width:#verifica se o NPC está dentro da área central da tela (onde o jogador mira)
                self.game.sound.npc_pain.play()#toca o som de dor do NPC
                self.game.player.shot = False #reseta o estado de tiro do jogador
                self.pain = True#define que o NPC está em estado de dor
                self.health -= self.game.weapon.damage# reduz a saúde do NPC com base no dano da arma do jogador
                self.check_health() #verifica se o NPC morreu após o dano
    
    def check_health(self): #verifica a saúde do NPC e define se ele está vivo ou morto
        if self.health < 1:#3
            self.alive = False# toca som de morte do NPC
            self.game.sound.npc_death.play()
    
    def run_logic(self): #lógica principal do NPC a cada frame
        if self.alive:#verifica se o NPC está vivo
            self.ray_cast_value = self.ray_cast_player_npc() #verifica se o NPC pode ver o jogador
            self.check_hit_in_npc()# verifica se o NPC foi atingido pelo tiro do jogador
            if self.pain: #se o NPC está em estado de dor
                self.animate_pain()# executa a animação de dor
            elif self.ray_cast_value: #se o NPC pode ver o jogador
                self.player_search_trigger = True# ativa o gatilho de busca do jogador
                 #se a distância até o jogador for menor que a distância de ataque, executa o ataque
                if self.dist < self.attack_dist:
                    self.animate(self.attack_images)
                    self.attack()
                else:#se estiver longe, anda em direção ao jogador
                    self.animate(self.walk_images)
                    self.movement()
            elif self.player_search_trigger:#se o NPC já viu o jogador antes, mas agora não vê mais
                self.animate(self.walk_images)# anda em direção à última posição conhecida do jogador
                self.movement()
            else:#se o NPC não viu o jogador, fica em estado de ócio
                self.animate(self.idle_images)
        else:#se o NPC está morto
            self.animate_death()

    @property # Transforma map_pos em atributo, então não precisa ficar colocando parênteses toda hora
    def map_pos(self):# 
        return int(self.x), int(self.y)
    
    def ray_cast_player_npc(self): #verifica se o NPC pode ver o jogador usando ray casting
        if self.game.player.map_pos == self.map_pos:
            return True
        
        wall_dist_v, wall_dist_h = 0, 0 
        player_dist_v, player_dist_h = 0, 0

        ox, oy= self.game.player.pos() #pega a posição x e y do jogador
        x_map, y_map= self.game.player.map_pos() #mapeia essas posições onde o jogador se deslocar

        ray_angle = self.theta #angulo que o jogador se deslocar

        sin_a= math.sin(ray_angle)
        cos_a= math.cos(ray_angle)

        #mapear o jogador na horizontal
        y_hor, dy= (y_map +1, 1) if sin_a>0 else (y_map - 1e-6, -1)
        depth_hor= (y_hor - oy)/ sin_a
        x_hor= ox + depth_hor * cos_a
        delta_depth= dy/ sin_a
        dx= delta_depth * cos_a

        for i in range(MAX_DEPTH): #loop da distancia maxima do jogador pode enxergar na horizontal
            tile_hor= int(x_hor), int(y_hor)
            if tile_hor == self.map_pos:
                player_dist_h = depth_hor
                break
            if tile_hor in self.game.map.world_map: 
                wall_dist_h = depth_hor
                break
            x_hor += dx
            y_hor += dy
            depth_hor += delta_depth

        #mapear o jogador na vertical
        x_vert, dx= (x_map +1, 1) if cos_a>0 else (x_map - 1e-6, -1)
        depth_vert= (x_vert - ox)/ cos_a
        y_vert= oy + depth_vert * sin_a
        delta_depth= dx/ cos_a
        dy= delta_depth * sin_a

        for i in range(MAX_DEPTH): #loop da distancia maxima do jogador pode enxergar na vertical
            tile_vert= int(x_vert), int(y_vert)# pega a posição do tile vertical
            if tile_vert == self.map_pos: # verifica se o tile é a posição do npc
                player_dist_v = depth_vert # define a distância até o jogador
                break
            if tile_vert in self.game.map.world_map: # verifica se há uma parede no tile
                wall_dist_v = depth_vert
                break
            x_vert += dx
            y_vert += dy
            depth_vert += delta_depth
        
        player_dist = max(player_dist_v, player_dist_h) # maior distância até o jogador
        wall_dist = max(wall_dist_v, wall_dist_h) # maior distância até a parede

        if 0 < player_dist < wall_dist or not wall_dist: #se o jogador está mais próximo que a parede ou se não há parede
            return True
        return False

    def draw_ray_cast(self): # Desenha linha de visão no inimigo na tela pra debug
        pg.draw.circle(self.game.screen, 'red', (100 * self.x, 100 * self.y), 15)
        if self.ray_cast_player_npc():#verifica se o NPC pode ver o jogador
            pg.draw.line(self.game.screen, 'orange', (100 * self.game.player.x, 100 * self.game.player.y),
                         (100 * self.x, 100 * self.y), 2)
    
class SoldierNPC(NPC): #Herda de NPC e define atributos específicos para o soldado
    def __init__(self, game, path='sprites/npc/soldier/0.png', pos=(10.5, 5.5), # posição inicial do soldado
                 scale=0.6, shift=0.38, animation_time=180):# escala, deslocamento e tempo de animação
        super().__init__(game, path, pos, scale, shift, animation_time) #chama o construtor da classe base NPC

class CacoDemonNPC(NPC): #Herda de NPC e define atributos específicos para o CacoDemon
    def __init__(self, game, path='sprites/npc/caco_demon/0.png', pos=(10.5, 6.5), # posição inicial do CacoDemon
                 scale=0.7, shift=0.27, animation_time=250):
        super().__init__(game, path, pos, scale, shift, animation_time)#chama o construtor da classe base NPC
        self.attack_dist = 1.0
        self.health = 150
        self.attack_damage = 25
        self.speed = 0.05
        self.accuracy = 0.35

class CyberDemonNPC(NPC):#Herda de NPC e define atributos específicos para o CyberDemon
    def __init__(self, game, path='sprites/npc/cyber_demon/0.png', pos=(11.5, 6.0),# posição inicial do CyberDemon
                 scale=1.0, shift=0.04, animation_time=210):
        super().__init__(game, path, pos, scale, shift, animation_time)#chama o construtor da classe base NPC
        self.attack_dist = 6
        self.health = 350
        self.attack_damage = 15
        self.speed = 0.055
        self.accuracy = 0.25