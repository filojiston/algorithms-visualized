import pygame
import sys
import random

# width and height of the screen
WIDTH = 600
HEIGHT = 600

# lesser this is, bigger grid array, so it will take much more time to solve it.
# choose this one carefully
GRID_SIZE = 6

# colors i've used in this program
COLORS = {
    "white": pygame.Color("white"),
    "red": pygame.Color("red"),
    "green": pygame.Color("green"),
    "blue": pygame.Color("blue"),
    "black": pygame.Color("black"),
    "yellow": pygame.Color("yellow")
}

# game screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Path Finding Visualizer")

# our grid representation. it has few attributes:
# x,y positions of the grid
# width and height of the grid
# color
# is_visited (bool)
# g and h values for calculating path using a* algorithm
# parent node, also used in a* algorithm


class Grid:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = GRID_SIZE
        self.height = GRID_SIZE
        self.color = COLORS["black"]
        self.is_visited = False
        self.g = 0
        self.h = 0
        self.parent = None

    def visit(self):
        self.is_visited = True
        if not self.color == COLORS["green"]:
            self.color = COLORS["red"]

    def set_wall(self):
        self.is_visited = True
        self.color = COLORS["white"]

    def show(self):
        pygame.draw.rect(screen, self.color,
                         (self.x * self.width, self.y * self.height, self.width, self.height))


# our grid array representation with some extra functionalities.
# in init method, we create the map randomly
# in show method, we draw the map to the screen
class Map:
    def __init__(self, srcx, srcy, destx, desty):
        self.grids = []
        for x in range(WIDTH // GRID_SIZE):
            max_visited = (WIDTH // GRID_SIZE) // 3
            visited = 0
            row = []
            for y in range(HEIGHT // GRID_SIZE):
                grid = Grid(x, y)
                k = random.randint(0, 4)
                if k == 1 and visited < max_visited:
                    visited += 1
                    grid.set_wall()
                row.append(grid)
            self.grids.append(row)
            row = []

        self.set_source(srcx, srcy)
        self.set_destination(destx, desty)

    def show(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    sys.exit()
        for row in self.grids:
            for grid in row:
                grid.show()
        pygame.display.flip()

    def set_source(self, x, y):
        self.grids[x][y].color = COLORS["green"]
        self.grids[x][y].is_wall = False
        self.grids[x][y].is_visited = False
        self.src = self.grids[x][y]

    def set_destination(self, x, y):
        self.grids[x][y].color = COLORS["green"]
        self.grids[x][y].is_wall = False
        self.grids[x][y].is_visited = False
        self.dest = self.grids[x][y]


# our path finding algorithms live in this class.
# currently, there are 4:
# bfs, dfs, dfs_iterative and astar algorithms
# class also has some helper functions like getting children of a node
# or tracking and drawing the shortest path found in algorithm etc.
class Solver:
    def __init__(self, map):
        self.map = map
        self.grids = map.grids
        self.src = self.map.src
        self.dest = self.map.dest

    def bfs(self):
        queue = [[self.src]]
        while len(queue) > 0:
            path = queue.pop(0)
            current = path[-1]
            current.visit()
            self.map.show()
            if current == self.dest:
                self.track_path(path)
                return True
            children = self.get_children(current)
            for child in children:
                child.visit()
                child.color = COLORS["yellow"]
                new_path = list(path)
                new_path.append(child)
                queue.append(new_path)
        return False

    def dfs(self, path=None):
        if path is None:
            path = [self.src]

        current = path[-1]
        if current == self.dest:
            self.track_path(path)
            return True
        current.visit()
        self.map.show()
        children = self.get_children(current)
        for child in children:
            child.visit()
            path.append(child)
            if (self.dfs(path)):
                return True
            path = path[:-1]
        return False

    def dfs_iterative(self):
        stack = [[self.src]]
        while len(stack) > 0:
            path = stack.pop(-1)
            current = path[-1]
            current.visit()
            self.map.show()
            if current == self.dest:
                self.track_path(path)
                return True
            children = self.get_children(current)
            for child in children:
                child.visit()
                child.color = COLORS["yellow"]
                new_path = list(path)
                new_path.append(child)
                stack.append(new_path)
        return False

    # https://mat.uab.cat/~alseda/MasterOpt/AStar-Algorithm.pdf

    def astar(self):
        open_list = [self.src]
        closed_list = []

        while len(open_list) > 0:
            current = self.find_lowest_f(open_list)
            current.color = COLORS["yellow"] if not current == self.src else COLORS["green"]
            if current == self.dest:
                curr = self.dest
                path = []
                while not curr.parent == None:
                    path.append(curr)
                    curr = curr.parent
                path.append(self.src)
                self.track_path(path)
                return True

            self.map.show()

            closed_list.append(current)
            children = self.get_children(current)
            for child in children:
                successor_current_cost = current.g + 1
                if child in open_list:
                    if child.g <= successor_current_cost:
                        continue
                elif child in closed_list:
                    if child.g <= successor_current_cost:
                        continue
                    open_list.append(child)
                    closed_list.remove(child)
                else:
                    child.h = self.calculateHeuristic(child)
                    open_list.append(child)
                child.g = successor_current_cost
                child.parent = current
                child.visit()

            closed_list.append(current)
            open_list.remove(current)

        return False

    def calculateHeuristic(self, grid):
        return ((self.dest.x - grid.x) ** 2) + ((self.dest.y - grid.y) ** 2)

    def find_lowest_f(self, open_list):
        min_f = open_list[0].g + open_list[0].h
        min_grid = open_list[0]
        for i in range(1, len(open_list)):
            if open_list[i].g + open_list[i].h < min_f:
                min_f = open_list[i].g + open_list[i].h
                min_grid = open_list[i]

        return min_grid

    def get_children(self, grid):
        children = []
        pos = [[grid.x - 1, grid.y], [grid.x, grid.y + 1],
               [grid.x + 1, grid.y], [grid.x, grid.y - 1]]

        for p in pos:
            if 0 <= p[0] < (WIDTH // GRID_SIZE) and 0 <= p[1] < (HEIGHT // GRID_SIZE):
                if not self.grids[p[0]][p[1]].is_visited:
                    children.append(self.grids[p[0]][p[1]])

        return children

    def track_path(self, path):
        for i, grid in enumerate(path):
            if i == 0 or i == len(path) - 1:
                grid.color = COLORS["green"]
            else:
                grid.color = COLORS["blue"]
                map.show()

    def print_path(self, path):
        for i, grid in enumerate(path):
            print(f"{i}. grid: {grid.x} {grid.y}")


# init the map with random source and destination grids
startx = random.randint(0, WIDTH // GRID_SIZE - 1)
starty = random.randint(0, HEIGHT // GRID_SIZE - 1)
endx = random.randint(0, WIDTH // GRID_SIZE - 1)
endy = random.randint(0, HEIGHT // GRID_SIZE - 1)
map = Map(startx, starty, endx, endy)
# map = Map(0, 0, 159, 159)

# create a solver with given map
solver = Solver(map)
# solve the map with desired algorithm
# NOTE!! it is possible that algorithm can not solve the map
# because map is generated randomly and the source or destination point may be
# surrounded by walls. in that case, the result will be false.
result = solver.dfs_iterative()

# continue to draw the result while user has not clicked the exit button
running = True
while running:
    map.show()
