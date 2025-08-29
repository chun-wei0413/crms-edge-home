import time
import queue

# 用于存储状态更新的队列
update_queue = queue.Queue()

class Moving:
    def __init__(self, environment, sensor, navigation, battery_capacity=100):
        self.environment = environment
        self.sensor = sensor
        self.navigation = navigation
        self.battery = battery_capacity
        self.battery_capacity = battery_capacity
        self.charging_station = environment.robot_position  # 假設起始位置為充電站
        self.cleaned = set()
        self.moves_since_last_charge = 0

    def sense(self):
        self._update_status("Sensing surroundings")
        time.sleep(0.5)  # 感應1秒
        surroundings = self.sensor.sense(self.environment.robot_position)
        self.environment.update_known_grid(surroundings)
        return surroundings

    def move(self, new_position):
        if self.battery > 0:
            self._update_status(f"Current position: {self.environment.robot_position}, Moving to {new_position}")
            time.sleep(0.5)  # 移動1秒
            self.environment.move_robot(new_position)
            self.sense()
            # 每次移動更新一次地圖
            self.environment.display_known_grid()
            self.battery -= 1  # 每次移動減少一格電量
            self.display_status()  # 顯示電池電量
            self.moves_since_last_charge += 1
        else:
            self.recharge()

    def recharge(self):
        print("電池電量不足，返回充電站。。。")
        self._update_status("電池電量不足，返回充電站。。。")
        path_to_charging = self.navigation.find_path(self.environment.robot_position, self.charging_station)
        if path_to_charging:
            for position in path_to_charging[1:]:
                self.move(position)
        self._update_status("charging...")
        time.sleep(3)  # 模擬充電時間
        self.battery = self.battery_capacity  # 充滿電
        self._update_status("charging complete.")
        print("充電完成。")
        if self.navigation.task_in_progress:
            self.navigation.clean()
    
    def return_to_charge_station(self):
        print("清潔完成，返回充電站。")
        self._update_status("清潔完成，返回充電站。")
        path_to_start = self.navigation.find_path(self.environment.robot_position, self.charging_station)
        if path_to_start:
            for position in path_to_start[1:]:
                self.move(position)
        self._update_status("charging...")
        time.sleep(3) 
        self.battery = self.battery_capacity
        self._update_status("charging complete.")
        print("充電完成。")
        self.display_status()

    def _update_status(self, message):
        status = {
            "position": self.environment.robot_position,
            "cleaned": list(self.cleaned),
            "battery": self.battery,
            "revealed_map": [row[:] for row in self.environment.known_grid],
            "moves_since_last_charge": self.moves_since_last_charge,
            "message": message
        }
        update_queue.put(status)

    def display_status(self):
        print(f"剩餘電池電量: {self.battery}")
