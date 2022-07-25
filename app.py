from flask import Flask, render_template, request, redirect, url_for
from flask_socketio import SocketIO, emit



app = Flask(__name__)
app.config['SECRET_KEY'] = 'hackaton'
socketio = SocketIO(app)

@app.route('/', methods=['GET', 'POST'])
def inicio():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        next = request.args.get('next', None)
        if next:
            return redirect(next)
        return redirect(url_for(''))
    return render_template('index.html')


@socketio.on('alarma')
def alarm():
    print('estamos en evento alarma')
    emit('panik', "AAAAAAAAA WIIIIIUUU PANIK")

if __name__ == '__main__':
    socketio.run(app, debug=True)