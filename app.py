from flask import Flask, render_template, request, redirect, url_for, session
from flask_socketio import SocketIO, join_room, leave_room, send

app = Flask(__name__)
app.config['SECRET_KEY'] = 'thisisafakekey'
socketio = SocketIO(app)

# 설정된 사용자들
users = {"user1": "password1", "user2": "password2"}
room = "private_room"

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in users and users[username] == password:
            session['username'] = username
            return redirect(url_for('chat'))
    return render_template('index.html')

@app.route('/chat')
def chat():
    if 'username' not in session:
        return redirect(url_for('index'))
    return render_template('chat.html', username=session['username'])

@socketio.on('join')
def on_join(data):
    username = data['username']
    join_room(room)
    send(f"{username} has entered the room.", room=room)

@socketio.on('message')
def on_message(data):
    msg = data['msg']
    username = data['username']
    send(f"{username}: {msg}", room=room)

@socketio.on('leave')
def on_leave(data):
    username = data['username']
    leave_room(room)
    send(f"{username} has left the room.", room=room)

if __name__ == '__main__':
    socketio.run(app)
