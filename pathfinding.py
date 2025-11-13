from collections import deque


# Classe que vai ser responsável por calcular caminhos automáticos para NPCs:
class PathFinding:
    def __init__(self, game):
        self.game = game
        self.map = game.map.mini_map
        self.ways = [-1, 0], [0, -1], [1, 0], [0, 1], [-1, -1], [1, -1], [1, 1], [-1, 1] # Movimentos possíveis (cima, baixo, esquerda, direita e diagonais) 8 posiiblidades
        self.graph = {} # Dicionário que representa o grafo do mapa
        self.get_graph()# Constrói o grafo do mapa

    # Função que percorre o grafo para encontrar o melhor caminho do ponto inicial ao ponto final:
    def get_path(self, start, goal):
        self.visited = self.breadth_first_search(start, goal, self.graph) # Eealiza a busca em largura para encontrar o caminho
        path = [goal] # Adiciona o objetivo final
        step = self.visited.get(goal, start) # Volta pelo caminho encontrado do objetivo ao ponto inicial

        while step and step != start: # Percorre passo a passo pra encontrar caminhos válidos
            path.append(step)
            step = self.visited[step]
        return path[-1] # Retorna último passo

    # Busca em largura para encontrar o caminho mais curto:
    def breadth_first_search(self, start, goal, graph):
        queue = deque([start]) # Fila para explorar os nós
        visited = {start: None} # Dicionário para rastrear os nós visitados e seus predecessores

        while queue: # Enquanto houver nós para explorar
            cur_node = queue.popleft() # Remove e retorna o elemento do começo da fila
            if cur_node == goal: # Objetivo alcançado
                break
            next_nodes = graph[cur_node] # Obtém os nós vizinhos do nó atual

            for next_node in next_nodes: # Explora cada nó vizinho
                if next_node not in visited and next_node not in self.game.object_handler.npc_positions: # Verifica se o nó já foi visitado e não está ocupado por um NPC
                    queue.append(next_node)
                    visited[next_node] = cur_node # Eegistra o nó predecessor
        return visited # Retorna o dicionário de nós visitados
    
    # Obtém os nós vizinhos acessíveis a partir da posição (x, y) e retorna todos os vizinhos que estão dentro das direções possíveis e  não são paredes:
    def get_next_nodes(self, x, y):
        return [(x + dx, y + dy) for dx, dy in self.ways if (x + dx, y + dy) not in self.game.map.world_map] # Retorna todos os vizinhos que estão dentro das direções possíveis e  não são paredes

    # Percorre o mapa e constrói o grafo de posições acessíveis:
    def get_graph(self):
        for y, row in enumerate(self.map): # Percorre cada linha do mapa
            for x, col in enumerate(row): # Se a célula estiver vazia (sem parede), adiciona as posições vizinhas acessíveis ao grafo
                if not col:
                    self.graph[(x, y)] = self.graph.get((x, y), []) + self.get_next_nodes(x, y) # Adiciona as posições vizinhas acessíveis ao grafo