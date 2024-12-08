import pygame
import random
import time
from queue import PriorityQueue

# Constants
CELL_SIZE = 20
FPS = 30
WALL_COLOR = (0, 0, 0)
PATH_COLOR = (255, 255, 255)
START_COLOR = (0, 255, 0)
END_COLOR = (255, 0, 0)
VISITED_COLOR = (0, 0, 255)
FINAL_PATH_COLOR = (255, 255, 0)

# Create a solvable maze
def create_solvable_maze(rows, cols):
    maze = [["#" for _ in range(cols)] for _ in range(rows)]
    start = (1, 1)
    end = (rows - 2, cols - 2)
    stack = [start]
    visited = set()
    visited.add(start)
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    while stack:
        current = stack.pop()
        maze[current[0]][current[1]] = " "
        random.shuffle(directions)
        for dx, dy in directions:
            nx, ny = current[0] + dx * 2, current[1] + dy * 2
            if 1 <= nx < rows - 1 and 1 <= ny < cols - 1 and (nx, ny) not in visited:
                maze[current[0] + dx][current[1] + dy] = " "
                visited.add((nx, ny))
                stack.append((nx, ny))

    maze[start[0]][start[1]] = "S"
    maze[end[0]][end[1]] = "E"
    return maze

# A* Algorithm for pathfinding
def astar_solve(maze, start, end, visualize_callback):
    rows, cols = len(maze), len(maze[0])
    open_set = PriorityQueue()
    open_set.put((0, start))
    came_from = {}
    
    # Initialize g_score and f_score for all cells in the maze
    g_score = { (r, c): float("inf") for r in range(rows) for c in range(cols) }
    g_score[start] = 0
    f_score = { (r, c): float("inf") for r in range(rows) for c in range(cols) }
    f_score[start] = heuristic(start, end)
    
    visited = set()

    while not open_set.empty():
        _, current = open_set.get()
        visited.add(current)

        if current == end:
            return reconstruct_path(came_from, current, visualize_callback)

        for neighbor in get_neighbors(current, maze):
            temp_g_score = g_score[current] + 1
            if temp_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = temp_g_score
                f_score[neighbor] = temp_g_score + heuristic(neighbor, end)
                if neighbor not in visited:
                    open_set.put((f_score[neighbor], neighbor))
                    visited.add(neighbor)
                    visualize_callback(neighbor, VISITED_COLOR)

    return []


def heuristic(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def reconstruct_path(came_from, current, visualize_callback):
    path = []
    while current in came_from:
        path.append(current)
        current = came_from[current]
        visualize_callback(current, FINAL_PATH_COLOR)
    return path[::-1]

def get_neighbors(pos, maze):
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    neighbors = []
    for dx, dy in directions:
        x, y = pos[0] + dx, pos[1] + dy
        if 0 <= x < len(maze) and 0 <= y < len(maze[0]) and maze[x][y] != "#":
            neighbors.append((x, y))
    return neighbors

# Visualize the maze and pathfinding
def visualize_maze(maze, path=None):
    rows, cols = len(maze), len(maze[0])
    width, height = cols * CELL_SIZE, rows * CELL_SIZE
    pygame.init()
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Maze Solver")
    clock = pygame.time.Clock()

    def draw_grid():
        for row in range(rows):
            for col in range(cols):
                rect = pygame.Rect(col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                color = WALL_COLOR if maze[row][col] == "#" else PATH_COLOR
                if maze[row][col] == "S":
                    color = START_COLOR
                elif maze[row][col] == "E":
                    color = END_COLOR
                pygame.draw.rect(screen, color, rect)
                pygame.draw.rect(screen, (200, 200, 200), rect, 1)

    def visualize_callback(position, color):
        x, y = position
        rect = pygame.Rect(y * CELL_SIZE, x * CELL_SIZE, CELL_SIZE, CELL_SIZE)
        pygame.draw.rect(screen, color, rect)
        pygame.draw.rect(screen, (200, 200, 200), rect, 1)
        pygame.display.update()
        clock.tick(FPS)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill((0, 0, 0))
        draw_grid()
        pygame.display.update()

        start = (1, 1)
        end = (rows - 2, cols - 2)
        path = astar_solve(maze, start, end, visualize_callback)
        print(f"Path found: {path}")
        time.sleep(2)
        running = False

    pygame.quit()

# Main
if __name__ == "__main__":
    rows, cols = random.randint(10,40), random.randint(10,40)  # Adjust maze size
    maze = create_solvable_maze(rows, cols)
    visualize_maze(maze)
