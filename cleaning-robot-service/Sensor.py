class Sensor:
    def __init__(self, environment):
        self.environment = environment
    
    def sense(self, position):
        x, y = position
        directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
        surroundings = {}
        
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < self.environment.size and 0 <= ny < self.environment.size:
                surroundings[(nx, ny)] = self.environment.grid[nx][ny]
            else:
                surroundings[(nx, ny)] = None  # 超出邊界的情況
        
        return surroundings
