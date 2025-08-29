from Sensor import Sensor
from Moving import Moving
from collections import deque

class Navigation:
    def __init__(self, environment):
        self.environment = environment
        self.sensor = Sensor(environment)
        self.moving = Moving(environment, self.sensor, self)
        self.current_direction = 1  # 1表示从左到右，-1表示从右到左
        self.task_in_progress = False  # 添加任务进行标志

    def find_path(self, start, goal):
        queue = deque([(start, [start])])
        seen = set([start])
        while queue:
            (current, path) = queue.popleft()
            if current == goal:
                return path
            for direction in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                neighbor = (current[0] + direction[0], current[1] + direction[1])
                if (0 <= neighbor[0] < self.environment.size and
                        0 <= neighbor[1] < self.environment.size and
                        neighbor not in seen and
                        self.environment.grid[neighbor[0]][neighbor[1]] != 'O'):
                    queue.append((neighbor, path + [neighbor]))
                    seen.add(neighbor)
        return None
    
    def calculate_required_battery(self, start, goal):
        path = self.find_path(start, goal)
        if path:
            return len(path)  # 每次移動消耗一點電量
        return float('inf')  # 如果找不到路徑，返回無窮大
    
    def mark_unreachable(self):
        for x in range(self.environment.size):
            for y in range(self.environment.size):
                if self.environment.known_grid[x][y] == 'D' or self.environment.known_grid[x][y] == '?':
                    self.environment.known_grid[x][y] = 'X'

    def find_nearest_target(self, start):
        queue = deque([start])
        seen = set([start])
        while queue:
            current = queue.popleft()
            x, y = current
            if self.environment.known_grid[x][y] == 'D' or self.environment.known_grid[x][y] == '?':
                return current
            for direction in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                neighbor = (x + direction[0], y + direction[1])
                if (0 <= neighbor[0] < self.environment.size and
                        0 <= neighbor[1] < self.environment.size and
                        neighbor not in seen and
                        self.environment.grid[neighbor[0]][neighbor[1]] != 'O'):
                    queue.append(neighbor)
                    seen.add(neighbor)
        return None

    def clean(self):
        self.task_in_progress = True 
        while self.task_in_progress and (self.environment.has_unknown() or not self.environment.is_clean()):
            print(f"Current robot position: {self.environment.robot_position}, Battery: {self.moving.battery}") 
            if self.moving.battery <= 10 or self.calculate_required_battery(self.environment.robot_position, self.moving.charging_station) >= self.moving.battery:
                self.moving.recharge()
                continue

            next_target = None
            # 先找D
            for x in range(self.environment.size):
                for y in range(self.environment.size):
                    if self.environment.known_grid[x][y] == 'D':
                        next_target = (x, y)
                        break
                if next_target:
                    break
            # 如果没有D，再找?
            if not next_target:
                for x in range(self.environment.size):
                    for y in range(self.environment.size):
                        if self.environment.known_grid[x][y] == '?':
                            next_target = (x, y)
                            break
                    if next_target:
                        break
            
            if next_target:
                path = self.find_path(self.environment.robot_position, next_target)
                if path:
                    print(f"Path found to target {next_target}: {path}") 
                    for position in path[1:]:
                        # 檢查電量是否足夠回充電站
                        if self.calculate_required_battery(position, self.moving.charging_station) < self.moving.battery:
                            self.moving.move(position)
                        else:
                            self.moving.recharge()
                            return

            # 如果当前行已清扫完成，寻找下一行中最近的目标
            robot_x, robot_y = self.environment.robot_position
            if self.current_direction == 1 and robot_y == self.environment.size - 1:
                next_position = (robot_x + 1, robot_y)
                self.current_direction = -1
            elif self.current_direction == -1 and robot_y == 0:
                next_position = (robot_x + 1, robot_y)
                self.current_direction = 1
            else:
                next_position = (robot_x, robot_y + self.current_direction)

            # 确保下一个位置是可达的，如果不可达，寻找最近的目标
            if 0 <= next_position[0] < self.environment.size and 0 <= next_position[1] < self.environment.size:
                if self.environment.grid[next_position[0]][next_position[1]] != 'O':
                    if self.calculate_required_battery(next_position, self.moving.charging_station) < self.moving.battery:
                        self.moving.move(next_position)
                    else:
                        self.moving.recharge()
                else:
                    nearest_target = self.find_nearest_target(self.environment.robot_position)
                    if nearest_target:
                        path = self.find_path(self.environment.robot_position, nearest_target)
                        if path:
                            for position in path[1:]:
                                if self.calculate_required_battery(position, self.moving.charging_station) < self.moving.battery:
                                    self.moving.move(position)
                                else:
                                    self.moving.recharge()
                                    break
                        else:
                            print("Unable to find path to nearest target, marking as unreachable.")
                            self.mark_unreachable()
                            self.moving._update_status("剩餘區域無法清掃，即將返回充電站。")
                            self.moving.return_to_charge_station()
                            self.task_in_progress = False
                            return
                    else:
                        print("No nearest target found, marking as unreachable.")
                        self.mark_unreachable()
                        self.moving._update_status("剩餘區域無法清掃，即將返回充電站。")
                        self.moving.return_to_charge_station()
                        self.task_in_progress = False
                        return

        # 清潔完成回到充電站
        self.moving.return_to_charge_station()
        self.moving._update_status("Cleaning task completed. Ready for the next run.")
        self.task_in_progress = False
