import random

class Environment:
    def __init__(self, size):
        self.size = size
        self.grid = [['D' for _ in range(size)] for _ in range(size)]
        self.known_grid = [['?' for _ in range(size)] for _ in range(size)]
        self.robot_position = (0, 0)  # 起始位置 (0, 0)
        self.grid[0][0] = 'R'

    def place_obstacles(self, obstacles):
        for x, y in obstacles:
            if 0 <= x < self.size and 0 <= y < self.size:
                self.grid[x][y] = 'O'
    
    def place_robot(self, start_position):
        x, y = start_position
        if 0 <= x < self.size and 0 <= y < self.size:
            self.grid[x][y] = 'R'
            self.known_grid[x][y] = 'R'
            self.robot_position = start_position
            self.start_position = start_position
    
    def move_robot(self, new_position):
        old_x, old_y = self.robot_position
        new_x, new_y = new_position
        if (0 <= new_x < self.size and 0 <= new_y < self.size and
                self.grid[new_x][new_y] != 'O'):
            self.grid[old_x][old_y] = 'C'
            self.known_grid[old_x][old_y] = 'C'
            self.grid[new_x][new_y] = 'R'
            self.known_grid[new_x][new_y] = 'R'
            self.robot_position = new_position
    
    def display_known_grid(self):
        for row in self.known_grid:
            print(' '.join(row))
        print()

    def update_known_grid(self, surroundings):
        for (x, y), status in surroundings.items():
            if 0 <= x < self.size and 0 <= y < self.size:
                self.known_grid[x][y] = status

    def is_clean(self):
        for row in self.grid:
            if 'D' in row:
                return False
        return True
    
    def has_unknown(self):
        for row in self.known_grid:
            if '?' in row:
                return True
        return False

    def random_obstacles(self, num_obstacles):
        count = 0
        while count < num_obstacles:
            x = random.randint(0, self.size - 1)
            y = random.randint(0, self.size - 1)
            if self.grid[x][y] == 'D':
                row_obstacles = sum(1 for cell in self.grid[x] if cell == 'O')
                col_obstacles = sum(1 for row in self.grid if row[y] == 'O')
                if row_obstacles < 8 and col_obstacles < 8:
                    self.grid[x][y] = 'O'
                    count += 1
