
import eventlet,cookiejar
from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit, disconnect
eventlet.monkey_patch()
app = Flask(__name__)
#app.debug = True

app.config['SECRET_KEY'] = 'crazycrackers'
socketio = SocketIO(app)


@app.route('/')
def chat():
    return render_template('chat.html')


@app.route('/login')
def login():
    return render_template('login.html')

def printout_users(users={}):
    user_list = "Connected users: \n" + "\n"
    for k,v in users.items():
        user_list+= k + "\n"
    return user_list
@socketio.on('message', namespace='/chat')
def chat_message(message):

    if(message['data']['author'] == 'Sudo_user'):

        if(message['data']['message'].lower().strip() == "users"):

            message['data']['message'] = printout_users(clients)

            emit('message', {'data': message['data']}, broadcast=False)
        if(message['data']['message'].strip() in clients):
            disconnect(clients[message['data']['message'].strip()])
            del clients[message['data']['message'].strip()]
            chat()

    else:
         emit('message', {'data': message['data']}, broadcast=True)


clients = {}


@socketio.on('connect', namespace='/chat')
def test_connect():

    print('Client connected:' +request.cookies['realtime-chat-nickname'])
    if(request.cookies['realtime-chat-nickname'] not in clients):
        clients[request.cookies['realtime-chat-nickname']] = request.sid

    emit('my response', {'data': 'Connected', 'count': 0})


@socketio.on('disconnect', namespace='/chat')
def test_disconnect():
    print('Client disconnected')



if __name__ == '__main__':
    print("Running on: 0.0.0.0:5000")
    socketio.run(app,host="0.0.0.0")

