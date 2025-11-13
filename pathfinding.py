from collections import deque


# vai ser responsável por calcular caminhos automáticos para NPCs e inimigos no jogo
class PathFinding:
    def __init__(self, game):
        self.game = game
        self.map = game.map.mini_map
        self.ways = [-1, 0], [0, -1], [1, 0], [0, 1], [-1, -1], [1, -1], [1, 1], [-1, 1]# movimentos possíveis (cima, baixo, esquerda, direita e diagonais) 8 posiiblidades
        self.graph = {} # dicionário que representa o grafo do mapa
        self.get_graph()# constrói o grafo do mapa

    # funcao que percorre o grafo para encontrar o melhor caminho do ponto inicial ao ponto final
    def get_path(self, start, goal):
        self.visited = self.breadth_first_search(start, goal, self.graph)# realiza a busca em largura para encontrar o caminho
        path = [goal] #
        step = self.visited.get(goal, start)# volta pelo caminho encontrado do objetivo ao ponto inicial

        while step and step != start:
            path.append(step)
            step = self.visited[step]
        return path[-1]

    def breadth_first_search(self, start, goal, graph): #busca em largura para encontrar o caminho mais curto
        queue = deque([start])# fila para explorar os nós
        visited = {start: None} # dicionário para rastrear os nós visitados e seus predecessores

        while queue:# enquanto houver nós para explorar
            cur_node = queue.popleft()
            if cur_node == goal: # objetivo alcançado
                break
            next_nodes = graph[cur_node] # obtém os nós vizinhos do nó atual

            for next_node in next_nodes: # explora cada nó vizinho
                if next_node not in visited and next_node not in self.game.object_handler.npc_positions:# verifica se o nó já foi visitado e não está ocupado por um NPC
                    queue.append(next_node)
                    visited[next_node] = cur_node # registra o nó predecessor
        return visited # retorna o dicionário de nós visitados
    
    def get_next_nodes(self, x, y): # obtém os nós vizinhos acessíveis a partir da posição (x, y) e  retorna todos os vizinhos que estão dentro das direções possíveis e  não são paredes
        return [(x + dx, y + dy) for dx, dy in self.ways if (x + dx, y + dy) not in self.game.map.world_map] # retorna todos os vizinhos que estão dentro das direções possíveis e  não são paredes

    def get_graph(self): #percorre o mapa e constrói o grafo de posições acessíveis
        for y, row in enumerate(self.map):# percorre cada linha do mapa
            for x, col in enumerate(row):# se a célula estiver vazia (sem parede), adiciona as posições vizinhas acessíveis ao grafo
                if not col:
                    self.graph[(x, y)] = self.graph.get((x, y), []) + self.get_next_nodes(x, y) # adiciona as posições vizinhas acessíveis ao grafo