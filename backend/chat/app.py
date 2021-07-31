import os

from flask import Flask, render_template, session, copy_current_request_context
from flask_socketio import SocketIO, emit, disconnect
from threading import Lock
import logging
logging.basicConfig(level=logging.DEBUG)


async_mode = 'gevent'
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socket_ = SocketIO(app, async_mode=async_mode,
                   cors_allowed_origins=["http://localhost:8080", "http://localhost:8081", 'http://localhost:5010'])
thread = None
thread_lock = Lock()


@app.route('/')
def index():
    return render_template('index.html', async_mode=socket_.async_mode)


@socket_.on('event', namespace='/message')
def test_message(message):
    session['receive_count'] = session.get('receive_count', 0) + 1
    emit('response',
         {'data': message['data'], 'count': session['receive_count']})


@socket_.on('broadcast', namespace='/message')
def test_broadcast_message(message):
    session['receive_count'] = session.get('receive_count', 0) + 1
    emit('response',
         {'data': message['data'], 'count': session['receive_count']},
         broadcast=True)


@socket_.on('disconnect', namespace='/message')
def disconnect_request():
    @copy_current_request_context
    def can_disconnect():
        disconnect()

    session['receive_count'] = session.get('receive_count', 0) + 1
    emit('response',
         {'data': 'Disconnected!', 'count': session['receive_count']},
         callback=can_disconnect)


if __name__ == '__main__':
    port = int(os.environ.get("WEBSOCKET_PORT", 5010))
    socket_.run(app, debug=True, port=port)
