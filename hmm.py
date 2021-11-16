from Maze import Maze
from MazeProblem import MazeProblem
import random

# Function to take a vector and scale it so its entries sum to 1
def normalize(vector):
    sum = 0
    for i in vector:
        sum += i
    for i in range(len(vector)):
        if sum != 0:
            vector[i] /= sum
    return vector

# Function to draw the timestamp, maze, and list of probabilities for the current square
def draw_matrix(maze_problem, observations, i, probability_matrix):

    # Timestamp
    print("\nt = " + str(i))

    # Probabilities
    to_print = probability_matrix[i]
    to_print = [round(n, 4) for n in to_print]
    print(to_print)

    # Maze
    visual_maze = []
    for m in range(maze_problem.width):
        visual_maze.append([])
        for n in range(maze_problem.height):
            if n == observations[i][0] and m == observations[i][1]:
                visual_maze[m].append(maze_problem.maze.map[maze_problem.maze.index(n, m)].upper())
            else:
                visual_maze[m].append(maze_problem.maze.map[maze_problem.maze.index(n, m)])
    for n in range(len(visual_maze) - 1, -1, -1):
        print(visual_maze[n])

# Main function in which HMM filtering is performed
def forward(probability_matrix, observations, evidence_values, maze_problem):

    # Intialize
    probability_matrix.append([])
    for i in range(len(evidence_values)):
        x, y = maze_problem.get_2D_coord(evidence_values[i])
        if maze_problem.maze.map[maze_problem.maze.index(x, y)] != "#":
            probability_matrix[0].append(1 / maze_problem.square_count)
        else:
            probability_matrix[0].append(0)
    draw_matrix(maze_problem, observations, 0, probability_matrix)

    # Iterate through each timestep
    for i in range(1, len(observations)):
        probability_matrix.append([])

        # Iterate through each square
        for j in range(len(evidence_values)):

            x1, y1 = maze_problem.get_2D_coord(j)
            index_of_color = maze_problem.colors.index(observations[i][2])
            observation_likelihood = maze_problem.observation_matrix[index_of_color][maze_problem.get_1D_coord(x1, y1)]

            # Iterate through each square, again
            probability_sum = 0
            for k in range(len(evidence_values)):
                x2, y2 = maze_problem.get_2D_coord(k)
                posterior_probability = probability_matrix[i - 1][k]
                transition_probability = maze_problem.transition_matrix[maze_problem.get_1D_coord(x2, y2)][maze_problem.get_1D_coord(x1, y1)]
                probability_sum += posterior_probability * transition_probability * observation_likelihood

            # Add results for square_j to the probability matrix at time i
            probability_matrix[i].append(probability_sum)
        normalize(probability_matrix[i])

        draw_matrix(maze_problem, observations, i, probability_matrix)

    to_return = probability_matrix[len(observations) - 1]
    to_return = [round(i, 4) for i in to_return]
    # draw_matrix(maze_problem, observations, len(observations) - 1, probability_matrix)
    return to_return


random.seed(None)

test_maze1 = Maze("maze1.maz")
maze_problem = MazeProblem(test_maze1)
probability_matrix = []
maze_problem.create_transition_matrix()


starting_location = random.randint(0, len(maze_problem.squares) - 1)
x, y = maze_problem.get_2D_coord(starting_location)

observations = []
generate_random = False

if generate_random: # NOTE: If robot starts in a wall, program will fail to execute
    for t in range(10): # t is number of timesteps

        rand = random.uniform(0, 1)
        correct_color = maze_problem.maze.map[maze_problem.maze.index(x, y)]
        if rand < 0.88:
            observations.append((x, y, correct_color))
        else:
            color_copy = maze_problem.colors.copy()
            color_copy.remove(correct_color)
            if rand < 0.92:
                observations.append((x, y, color_copy[0]))
            elif rand < 0.96:
                observations.append((x, y, color_copy[1]))
            else:
                observations.append((x, y, color_copy[2]))

        i = random.randint(0, 3)
        if i == 0: # East
            if test_maze1.is_floor(x + 1, y):
                x += 1
        elif i == 1: # West
            if test_maze1.is_floor(x - 1, y):
                x -= 1
        elif i == 2: # North
            if test_maze1.is_floor(x, y + 1):
                y += 1
        elif i == 3: # South
            if test_maze1.is_floor(x, y - 1):
                y -= 1

else:
    observations = [(2,2,"g"),(3,2,"y"),(3,3,"r"),(3,3,"r"),(2,3,"r"),(2,3,"r"),(3,3,"r"),(3,2,"y"),(3,3,"r"),(3,2,"y")]

print("Observations: " + str(observations))
result = forward(probability_matrix, observations, maze_problem.squares, maze_problem)
# for i in range(len(result)):
#     x, y = maze_problem.get_2D_coord(i)
#     print(str(x) + ", " + str(y) + ": " + str(result[i]))