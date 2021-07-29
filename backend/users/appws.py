from flask import Flask
from flask_socketio import SocketIO

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*", engineio_logger=True)

print("--------started this thing-------------")


@app.route("/")
def test():
    return {"status": "success"}


@socketio.on('connect')
def test_connect():
    print("client connected")


@socketio.on("my event")
def handle_my_event():
    print("my event received")


@socketio.on('disconnect')
def test_disconnect():
    print('Client disconnected')


if __name__ == '__main__':
    socketio.run(app, host="127.0.0.1", port=5001, debug=True)