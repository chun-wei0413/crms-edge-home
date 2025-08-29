from flask import Flask, json, jsonify, request, render_template, Response
import threading
from Moving import update_queue
from robot_control import *

app = Flask(__name__)

# 机器人状态
robot_state = {
    "is_on": False,
    "position": (0, 0),
    "cleaned": set(),
    "battery": 100,
    "revealed_map": [['?' for _ in range(10)] for _ in range(10)],
    "moves_since_last_charge": 0
}

cleaning_thread = None
stop_event = threading.Event()  # 使用线程事件来控制停止

def run_cleaning_task():
    run_cleaning()

@app.route('/on', methods=['POST'])
def turn_on():
    global cleaning_thread
    if not robot_state["is_on"]:
        robot_state["is_on"] = True
        stop_event.clear()
        cleaning_thread = threading.Thread(target=run_cleaning_task)
        cleaning_thread.start()
        print("Robot cleaning task started.")
    return jsonify({"message": "Robot turned on"}), 200

@app.route('/off', methods=['POST'])
def turn_off():
    print("off get")
    global cleaning_thread
    robot_state["is_on"] = False
    stop_event.set()
    now_stop_cleaning()
    if cleaning_thread is not None:
        cleaning_thread.join()
        cleaning_thread = None
    print("Robot cleaning task stopped.")
    return jsonify({"message": "Robot turned off"}), 200

@app.route('/state', methods=['GET'])
def get_state():
    return jsonify(robot_state), 200

@app.route('/events')
def events():
    def generate():
        while True:
            status = update_queue.get()
            yield f"data: {json.dumps(status)}\n\n"
    return Response(generate(), mimetype='text/event-stream')

@app.route('/')
def index():
    return render_template('index.html', state=robot_state)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
