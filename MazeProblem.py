import numpy as np

class MazeProblem:

    def __init__(self, maze):

        self.maze = maze
        self.colors = ["r", "g", "b", "y"]
        self.width = self.maze.width
        self.height = self.maze.height
        self.square_count = self.width * self.height
        self.transition_matrix = []
        for i in range(self.square_count):
            self.transition_matrix.append([])
            for j in range(self.square_count):
                self.transition_matrix[i].append(0)
        self.squares = []
        for i in range(self.width):
            for j in range(self.height):
                self.squares.append(self.get_1D_coord(j, i))
        self.observation_matrix = []
        for i in range(len(self.colors)):
            self.observation_matrix.append([])
            for j in self.squares:
                x, y = self.get_2D_coord(j)
                if self.maze.map[self.maze.index(x, y)] == self.colors[i]:
                    self.observation_matrix[i].append(1 - (len(self.colors) - 1) * 0.04)
                else:
                    self.observation_matrix[i].append(0.04)
        for square in self.squares:
            x, y = self.get_2D_coord(square)
            if not self.maze.is_floor(x, y):
                self.square_count -= 1


    def get_1D_coord(self, x, y):
        return y * self.width + x

    def get_2D_coord(self, i):
        x = i % self.width
        y = i // self.height
        return x, y

    def create_transition_matrix(self):

        for x in self.squares:
            i, j = self.get_2D_coord(x)

            walls = 0
            if not self.maze.is_floor(i - 1, j):
                walls += 1
            if not self.maze.is_floor(i + 1, j):
                walls += 1
            if not self.maze.is_floor(i, j - 1):
                walls += 1
            if not self.maze.is_floor(i, j + 1):
                walls += 1

            if self.maze.is_floor(i, j):
                self.transition_matrix[x][x] = walls / 4
                if self.maze.is_floor(i - 1, j):
                    self.transition_matrix[x][self.get_1D_coord(i - 1, j)] = 1 / 4
                if self.maze.is_floor(i + 1, j):
                    self.transition_matrix[x][self.get_1D_coord(i + 1, j)] = 1 / 4
                if self.maze.is_floor(i, j - 1):
                    self.transition_matrix[x][self.get_1D_coord(i, j - 1)] = 1 / 4
                if self.maze.is_floor(i, j + 1):
                    self.transition_matrix[x][self.get_1D_coord(i, j + 1)] = 1 / 4