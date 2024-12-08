import os
import random
import keyboard  # Install using `pip install keyboard`

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def create_solvable_maze(rows, cols):
    # Create an empty maze
    maze = [["#" for _ in range(cols)] for _ in range(rows)]
    for i in range(rows):
        for j in range(cols):
            maze[i][j] = "#"  # Initially, everything is a wall
    
    # Create the start and end points
    start = (1, 1)
    end = (rows - 2, cols - 2)

    # Initialize a stack for DFS and visited set
    stack = [start]
    visited = set()
    visited.add(start)

    # Directions for movement: up, down, left, right
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    while stack:
        current = stack.pop()
        maze[current[0]][current[1]] = " "  # Mark current cell as open
        random.shuffle(directions)  # Shuffle directions for randomness
        
        for dx, dy in directions:
            nx, ny = current[0] + dx * 2, current[1] + dy * 2  # Check the cell two steps away
            if 1 <= nx < rows - 1 and 1 <= ny < cols - 1 and (nx, ny) not in visited:
                # Remove the wall between current and the next cell
                maze[current[0] + dx][current[1] + dy] = " "
                visited.add((nx, ny))
                stack.append((nx, ny))

    # Set the start and end positions
    maze[start[0]][start[1]] = " "
    maze[end[0]][end[1]] = "E"
    return maze

def display_maze(maze, player_pos):
    for row in range(len(maze)):
        for col in range(len(maze[row])):
            if (row, col) == player_pos:
                print("P", end=" ")  # Player's position
            else:
                print(maze[row][col], end=" ")
        print()

def move_player(position, direction, maze):
    x, y = position
    if direction == "up":  # Up
        new_pos = (x - 1, y)
    elif direction == "down":  # Down
        new_pos = (x + 1, y)
    elif direction == "left":  # Left
        new_pos = (x, y - 1)
    elif direction == "right":  # Right
        new_pos = (x, y + 1)
    else:
        return position  # Invalid key, stay in place
    
    # Check if the new position is within bounds and not a wall
    if 0 <= new_pos[0] < len(maze) and 0 <= new_pos[1] < len(maze[0]) and maze[new_pos[0]][new_pos[1]] != "#":
        return new_pos
    else:
        return position  # Stay in place if move is invalid

def main():
    rows, cols = 40,40  # Maze dimensions (odd numbers for better maze generation)
    maze = create_solvable_maze(rows, cols)
    player_pos = (1, 1)  # Starting position
    exit_pos = (rows - 2, cols - 2)  # Exit position

    print("Use arrow keys or W/A/S/D to move. Press ESC to quit.")
    while True:
        clear_screen()
        display_maze(maze, player_pos)
        if player_pos == exit_pos:
            print("🎉 Congratulations! You found the exit! 🎉")
            break

        # Wait for a valid key press
        key = keyboard.read_event()
        if key.event_type == "down":  # Check keypress event
            if key.name in ["up", "down", "left", "right"]:
                player_pos = move_player(player_pos, key.name, maze)
            elif key.name in ["w", "s", "a", "d"]:
                direction_map = {"w": "up", "s": "down", "a": "left", "d": "right"}
                player_pos = move_player(player_pos, direction_map[key.name], maze)
            elif key.name == "esc":
                print("Exiting the game. Goodbye!")
                break

if __name__ == "__main__":
    main()
