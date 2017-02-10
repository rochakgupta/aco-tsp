import math
import random
from PIL import ImageDraw, Image


class AntColonyOptimization:
    class Edge:
        def __init__(self, s, d, weight, initial_pheromone):
            self.s = s
            self.d = d
            self.weight = weight
            self.pheromone = initial_pheromone

    class Ant:
        def __init__(self, alpha, beta, n_nodes, edges):
            self.alpha = alpha
            self.beta = beta
            self.n_nodes = n_nodes
            self.edges = edges
            self.tour = None
            self.distance = 0

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

        def find_tour(self):
            self.tour = [random.randint(0, self.n_nodes - 1)]
            while len(self.tour) < self.n_nodes:
                self.tour.append(self.select_node())
            return self.tour

        def get_distance(self):
            self.distance = 0
            for i in range(self.n_nodes):
                if i == self.n_nodes - 1:
                    self.distance += self.edges[self.tour[i]][self.tour[0]].weight
                else:
                    self.distance += self.edges[self.tour[i]][self.tour[i + 1]].weight
            return self.distance

    def __init__(self, mode='ACS', colony_size=10, elitist_weight=1, alpha=1, beta=3, rho=0.1, pheromone_deposit_weight=1,
                 initial_pheromone=1, steps=200, n_nodes=20):
        self.mode = mode
        self.colony_size = colony_size
        self.elitist_weight = elitist_weight
        self.rho = rho
        self.pheromone_deposit_weight = pheromone_deposit_weight
        self.steps = steps
        self.n_nodes = n_nodes
        self.nodes = [(random.randint(0, 700), random.randint(0, 400)) for i in range(n_nodes)]
        self.edges = [[None] * n_nodes for i in range(n_nodes)]
        for i in range(n_nodes):
            for j in range(i + 1, n_nodes):
                edge = self.Edge(i, j, math.sqrt(pow(self.nodes[i][0] - self.nodes[j][0], 2) + pow(self.nodes[i][1] - self.nodes[j][1], 2)),
                                 initial_pheromone)
                self.edges[i][j] = edge
                self.edges[j][i] = edge
        self.ants = []
        for i in range(self.colony_size):
            self.ants.append(self.Ant(alpha, beta, n_nodes, self.edges))
        self.global_best_tour = None
        self.global_best_distance = float("inf")

    def _update_pheromone(self, ant):
        tour = ant.find_tour()
        pheromone_to_add = self.pheromone_deposit_weight / ant.get_distance()
        for i in range(self.n_nodes):
            if i == self.n_nodes - 1:
                edge = self.edges[tour[i]][tour[0]]
            else:
                edge = self.edges[tour[i]][tour[i + 1]]
            edge.pheromone += pheromone_to_add

    def _update_elitist_pheromone(self):
        pheromone_to_add = self.pheromone_deposit_weight / self.global_best_distance
        for i in range(self.n_nodes):
            if i == self.n_nodes - 1:
                edge = self.edges[self.global_best_tour[i]][self.global_best_tour[0]]
            else:
                edge = self.edges[self.global_best_tour[i]][self.global_best_tour[i + 1]]
            edge.pheromone += self.elitist_weight * pheromone_to_add

    def run(self):
        for step in range(self.steps):
            for ant in self.ants:
                self._update_pheromone(ant)
                if ant.distance < self.global_best_distance:
                    self.global_best_tour = ant.tour
                    self.global_best_distance = ant.distance
                    print(self.global_best_tour)
                    print(self.global_best_distance)
            if self.mode == 'Elitist':
                self._update_elitist_pheromone()
            for i in range(self.n_nodes):
                for j in range(i + 1, self.n_nodes):
                    self.edges[i][j].pheromone *= (1 - self.rho)

    def draw_tour(self):
        img = Image.new('RGB', (750, 450))
        drw = ImageDraw.Draw(img)
        drw.polygon([(self.nodes[node][0] + 25, self.nodes[node][1] + 25) for node in self.global_best_tour])
        for node in self.global_best_tour:
            drw.text((self.nodes[node][0] + 25, self.nodes[node][1] + 25), str(node))
        del drw
        img.save('tour.png', 'PNG')


if __name__ == '__main__':
    aco = AntColonyOptimization(mode='Elitist')
    aco.run()
    aco.draw_tour()
