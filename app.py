from flask import Flask, render_template
from flask_socketio import SocketIO
import psutil
import eventlet

eventlet.monkey_patch()

app = Flask(__name__)
socketio = SocketIO(app, async_mode='eventlet')

@app.route('/')
def index():
    return render_template('index.html')

def get_system_stats():
    """Get CPU and Memory usage."""
    while True:
        cpu_percent = psutil.cpu_percent(interval=1)
        memory_info = psutil.virtual_memory()

        # Convert bytes to GB for readability
        memory_used_gb = round(memory_info.used / (1024**3), 1)
        memory_total_gb = round(memory_info.total / (1024**3), 1)

        socketio.sleep(1)
        socketio.emit('system_update', {
            'cpu': cpu_percent,
            'memory': memory_info.percent,
            'memory_used_gb': memory_used_gb,
            'memory_total_gb': memory_total_gb
        })

@socketio.on('connect')
def handle_connect():
    print('Client connected')
    socketio.start_background_task(get_system_stats)

if __name__ == '__main__':
    socketio.run(app, debug=True)
