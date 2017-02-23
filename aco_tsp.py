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

        def _select_node(self):
            roulette_wheel = 0
            unvisited_nodes = [node for node in range(self.n_nodes) if node not in self.tour]
            heuristic_total = 0
            for unvisited_node in unvisited_nodes:
                heuristic_total += self.edges[self.tour[-1]][unvisited_node].weight
            for unvisited_node in unvisited_nodes:
                roulette_wheel += pow(self.edges[self.tour[-1]][unvisited_node].pheromone, self.alpha) * \
                                  pow((heuristic_total / self.edges[self.tour[-1]][unvisited_node].weight), self.beta)
            random_value = random.uniform(0, roulette_wheel)
            wheel_position = 0
            for unvisited_node in unvisited_nodes:
                wheel_position += pow(self.edges[self.tour[-1]][unvisited_node].pheromone, self.alpha) * \
                                  pow((heuristic_total / self.edges[self.tour[-1]][unvisited_node].weight), self.beta)
                if wheel_position >= random_value:
                    return unvisited_node

        def find_tour(self):
            self.tour = [random.randint(0, self.n_nodes - 1)]
            while len(self.tour) < self.n_nodes:
                self.tour.append(self._select_node())
            return self.tour

        def get_distance(self):
            self.distance = 0
            for i in range(self.n_nodes):
                if i == self.n_nodes - 1:
                    self.distance += self.edges[self.tour[i]][self.tour[0]].weight
                else:
                    self.distance += self.edges[self.tour[i]][self.tour[i + 1]].weight
            return self.distance

    def __init__(self, mode='ACS', colony_size=10, elitist_weight=1, min_scaling_factor=0.001, alpha=1, beta=3,
                 rho=0.1, pheromone_deposit_weight=1, initial_pheromone=1, steps=200, n_nodes=20, nodes=None):
        self.mode = mode
        self.colony_size = colony_size
        self.elitist_weight = elitist_weight
        self.min_scaling_factor = min_scaling_factor
        self.rho = rho
        self.pheromone_deposit_weight = pheromone_deposit_weight
        self.steps = steps
        if nodes:
            self.n_nodes = len(nodes)
            self.nodes = nodes
        else:
            self.n_nodes = n_nodes
            self.nodes = [(random.randint(0, 700), random.randint(0, 400)) for i in range(n_nodes)]
        self.edges = [[None] * n_nodes for i in range(n_nodes)]
        for i in range(n_nodes):
            for j in range(i + 1, n_nodes):
                edge = self.Edge(i, j, math.sqrt(
                    pow(self.nodes[i][0] - self.nodes[j][0], 2) + pow(self.nodes[i][1] - self.nodes[j][1], 2)),
                                 initial_pheromone)
                self.edges[i][j] = edge
                self.edges[j][i] = edge
        self.ants = []
        for i in range(self.colony_size):
            self.ants.append(self.Ant(alpha, beta, n_nodes, self.edges))
        self.global_best_tour = None
        self.global_best_distance = float("inf")

    def _add_pheromone(self, tour, distance, weight=1):
        pheromone_to_add = self.pheromone_deposit_weight / distance
        for i in range(self.n_nodes):
            if i == self.n_nodes - 1:
                edge = self.edges[tour[i]][tour[0]]
            else:
                edge = self.edges[tour[i]][tour[i + 1]]
            edge.pheromone += weight * pheromone_to_add

    def _acs(self):
        for step in range(self.steps):
            for ant in self.ants:
                self._add_pheromone(ant.find_tour(), ant.get_distance())
                if ant.distance < self.global_best_distance:
                    self.global_best_tour = ant.tour
                    self.global_best_distance = ant.distance
            for i in range(self.n_nodes):
                for j in range(i + 1, self.n_nodes):
                    self.edges[i][j].pheromone *= (1 - self.rho)

    def _elitist(self):
        for step in range(self.steps):
            for ant in self.ants:
                self._add_pheromone(ant.find_tour(), ant.get_distance())
                if ant.distance < self.global_best_distance:
                    self.global_best_tour = ant.tour
                    self.global_best_distance = ant.distance
            self._add_pheromone(self.global_best_tour, self.global_best_distance, weight=self.elitist_weight)
            for i in range(self.n_nodes):
                for j in range(i + 1, self.n_nodes):
                    self.edges[i][j].pheromone *= (1 - self.rho)

    def _max_min(self):
        for step in range(self.steps):
            iteration_best_tour = None
            iteration_best_distance = float("inf")
            for ant in self.ants:
                ant.find_tour()
                if ant.get_distance() < iteration_best_distance:
                    iteration_best_tour = ant.tour
                    iteration_best_distance = ant.distance
            if float(step + 1) / float(self.steps) <= 0.75:
                self._add_pheromone(iteration_best_tour, iteration_best_distance)
                max_pheromone = self.pheromone_deposit_weight / iteration_best_distance
            else:
                if iteration_best_distance < self.global_best_distance:
                    self.global_best_tour = iteration_best_tour
                    self.global_best_distance = iteration_best_distance
                self._add_pheromone(self.global_best_tour, self.global_best_distance)
                max_pheromone = self.pheromone_deposit_weight / self.global_best_distance
            min_pheromone = max_pheromone * self.min_scaling_factor
            for i in range(self.n_nodes):
                for j in range(i + 1, self.n_nodes):
                    self.edges[i][j].pheromone *= (1 - self.rho)
                    if self.edges[i][j].pheromone > max_pheromone:
                        self.edges[i][j].pheromone = max_pheromone
                    elif self.edges[i][j].pheromone < min_pheromone:
                        self.edges[i][j].pheromone = min_pheromone

    def run(self):
        if self.mode == 'ACS':
            self._acs()
        elif self.mode == 'Elitist':
            self._elitist()
        elif self.mode == 'MaxMin':
            self._max_min()
        else:
            print('Wrong mode. Choose ACS or Elitist or MaxMin')

    def draw_tour(self, name=None):
        img = Image.new('RGB', (750, 450))
        drw = ImageDraw.Draw(img)
        drw.polygon([(self.nodes[node][0] + 25, self.nodes[node][1] + 25) for node in self.global_best_tour])
        for node in self.global_best_tour:
            drw.text((self.nodes[node][0] + 25, self.nodes[node][1] + 25), str(node))
        del drw
        if not name:
            name = self.mode + '_tour.png'
        img.save(name, 'PNG')


if __name__ == '__main__':
    acs = AntColonyOptimization(mode='ACS')
    acs.run()
    acs.draw_tour()
    print(acs.global_best_distance)
    elitist = AntColonyOptimization(mode='Elitist', nodes=acs.nodes)
    elitist.run()
    elitist.draw_tour()
    print(elitist.global_best_distance)
    max_min = AntColonyOptimization(mode='MaxMin', nodes=acs.nodes)
    max_min.run()
    max_min.draw_tour()
    print(max_min.global_best_distance)
