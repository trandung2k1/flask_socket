from flask import Flask, render_template, jsonify
from flask_cors import CORS
from flask_socketio import SocketIO, emit
from dotenv import load_dotenv
from dotenv import dotenv_values
from configs.db import MyDB
from routes.todo import todo
load_dotenv()
config = dotenv_values(".env")
mycursor = MyDB.cursor()
mycursor.execute("SHOW DATABASES")
list_db = []
for x in mycursor:
    list_db.append(''.join(x))

if config['DATABASE'] not in list_db:
    print(config['DATABASE'])
    createddb = 'CREATE DATABASE ' + str(config['DATABASE'])
    mycursor.execute(createddb)
else:
    print("Connected to database " + str(config['DATABASE']))
app = Flask(__name__)
cors = CORS(app)
async_mode = None
socketio = SocketIO(app, cors_allowed_origins="*",
                    logger=True, engineio_logger=True, async_mode=async_mode)

app.register_blueprint(todo, url_prefix='/todos')


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


@app.route("/api/v1/todos", methods=['GET'])
def get_all_todo():
    mycursor.execute("SELECT * FROM todos")
    myresult = mycursor.fetchall()
    rs = []
    for x in myresult:
        rs.append(
            {'id': x[0], 'title': x[1], 'des': x[2], 'completed': "false" if x[3] == 0 else 'true'})
    return jsonify({
        "status": 200,
        "data": rs
    })


if __name__ == "__main__":
    socketio.run(app, host='0.0.0.0')
