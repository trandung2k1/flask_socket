from flask import Flask, render_template
from flask_cors import CORS
from flask_socketio import SocketIO, emit
app = Flask(__name__)
cors = CORS(app)
async_mode = None
socketio = SocketIO(app, cors_allowed_origins="*",
                    logger=True, engineio_logger=True, async_mode=async_mode)


@app.route("/")
def hello_world():
    return render_template('index.html')


@socketio.on('connect')
def test_connect():
    emit('connect-success', {'data': 'Client connected'})


@socketio.on('register')
def handle_register(json):
    emit('register-success', {'data': str(json)})


@socketio.on('send-msg')
def handle_event(json):
    print('Msg received:', str(json))


@socketio.on('disconnect')
def test_disconnect():
    print('User disconnected')


if __name__ == "__main__":
    socketio.run(app, host='0.0.0.0')
