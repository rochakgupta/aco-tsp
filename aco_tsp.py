import random, math
from PIL import ImageDraw, Image


class AntColonyOptimization:
    class Edge:
        def __init__(self, s, d, weight):
            self.s = s
            self.d = d
            self.weight = weight
            self.pheromone = 1

    class Ant:
        def __init__(self, alpha, beta, n_nodes, edges):
            self.alpha = alpha
            self.beta = beta
            self.n_nodes = n_nodes
            self.edges = edges
            self.tour = None

        def select_node(self):
            roulette_wheel = 0
            unvisited_nodes = [node for node in range(self.n_nodes) if node not in self.tour]
            heuristic_total = 0
            for unvisited_node in unvisited_nodes:
                heuristic_total += self.edges[self.tour[-1]][unvisited_node].weight
            for unvisited_node in unvisited_nodes:
                roulette_wheel += pow(self.edges[self.tour[-1]][unvisited_node].pheromone, self.alpha) * pow(
                    (heuristic_total / self.edges[self.tour[-1]][unvisited_node].weight), self.beta)
            random_value = random.uniform(0, roulette_wheel)
            wheel_position = 0
            for unvisited_node in unvisited_nodes:
                wheel_position += pow(self.edges[self.tour[-1]][unvisited_node].pheromone, self.alpha) * pow(
                    (heuristic_total / self.edges[self.tour[-1]][unvisited_node].weight), self.beta)
                if wheel_position >= random_value:
                    return unvisited_node

        def distance(self):
            total = 0
            for i in range(self.n_nodes):
                if i == self.n_nodes - 1:
                    total += self.edges[self.tour[i]][self.tour[0]].weight
                else:
                    total += self.edges[self.tour[i]][self.tour[i + 1]].weight
            return total

        def find_tour(self):
            self.tour = [random.randint(0, self.n_nodes - 1)]
            while len(self.tour) < self.n_nodes:
                self.tour.append(self.select_node())
            return self.tour

    def __init__(self, mode='ACS', colony_size=10, e=1, alpha=1, beta=3, rho=0.1, q=1, steps=200, n_nodes=20):
        self.mode = mode
        self.colony_size = colony_size
        self.e = e
        self.rho = rho
        self.q = q
        self.steps = steps
        self.n_nodes = n_nodes
        self.nodes = [(random.randint(0, 700), random.randint(0, 400)) for i in range(n_nodes)]
        self.edges = [[None] * n_nodes for i in range(n_nodes)]
        for i in range(n_nodes):
            for j in range(i + 1, n_nodes):
                edge = self.Edge(i, j, math.sqrt(pow(self.nodes[i][0] - self.nodes[j][0], 2) + pow(self.nodes[i][1] - self.nodes[j][1], 2)))
                self.edges[i][j] = edge
                self.edges[j][i] = edge
        self.ants = []
        for i in range(self.colony_size):
            self.ants.append(self.Ant(alpha, beta, n_nodes, self.edges))
        self.best_tour = None
        self.best_distance = float("inf")

    def _deposit_pheromone(self, ant):
        tour = ant.find_tour()
        pheromone_to_add = self.q / ant.distance()
        if ant.distance() < self.best_distance:
            self.best_distance = ant.distance()
            self.best_tour = tour
            print(self.best_distance)
            print(self.best_tour)
        for i in range(self.n_nodes):
            if i == self.n_nodes - 1:
                edge = self.edges[tour[i]][tour[0]]
            else:
                edge = self.edges[tour[i]][tour[i + 1]]
            edge.pheromone += pheromone_to_add

    def _deposit_elitist_pheromone(self, ant):
        tour = ant.find_tour()
        pheromone_to_add = self.q / ant.distance()
        for i in range(self.n_nodes):
            if i == self.n_nodes - 1:
                edge = self.edges[tour[i]][tour[0]]
            else:
                edge = self.edges[tour[i]][tour[i + 1]]
            edge.pheromone += self.e * pheromone_to_add

    def run(self):
        for step in range(self.steps):
            if self.mode == 'Elitist':
                best_ant = None
            for ant in self.ants:
                self._deposit_pheromone(ant)
                if self.mode == 'Elitist':
                    if not best_ant or ant.distance() < best_ant.distance():
                        best_ant = ant
            if self.mode == 'Elitist':
                self._deposit_elitist_pheromone(best_ant)
            for i in range(self.n_nodes):
                for j in range(i + 1, self.n_nodes):
                    self.edges[i][j].pheromone *= (1 - self.rho)

    def draw_tour(self):
        img = Image.new('RGB', (750, 450))
        drw = ImageDraw.Draw(img)
        drw.polygon([(self.nodes[node][0] + 25, self.nodes[node][1] + 25) for node in self.best_tour])
        for node in self.best_tour:
            drw.text((self.nodes[node][0] + 25, self.nodes[node][1] + 25), str(node))
        del drw
        img.save('tour.png', 'PNG')


if __name__ == '__main__':
    aco = AntColonyOptimization(mode='Elitist')
    aco.run()
    aco.draw_tour()
