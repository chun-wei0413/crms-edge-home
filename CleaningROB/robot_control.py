from Environment import Environment
from Navigation import Navigation
import time

stop_cleaning = False  # 标志位，用于控制清洁任务的停止

def place_custom_obstacles(environment, obstacles):
    environment.place_obstacles(obstacles)

def run_cleaning():
    global stop_cleaning
    stop_cleaning=False
    while not stop_cleaning:
        env = Environment(10)

        custom_obstacles = [(0, 7), (1, 7), (1, 8), (1, 1), (1, 9), (2, 0), (3, 0), (4, 4), (7, 8), (7, 9), (8, 4), (9, 4)]

        use_custom_obstacles = False

        if use_custom_obstacles:
            place_custom_obstacles(env, custom_obstacles)
        else:
            env.random_obstacles(13)

        env.place_robot((0, 0))

        nav = Navigation(env)
        nav.clean()

        if stop_cleaning:
            break

        print("Cleaning task completed. Ready for the next run.")
        time.sleep(2)

def now_stop_cleaning():
    global stop_cleaning
    stop_cleaning=True
