from multiprocessing import AuthenticationError
from flask import Flask, render_template, request, redirect, url_for
from flask_socketio import SocketIO, emit
import random
import time

auth = False

def generar_pin():
    pin = int(random.randint(1000,10000))
    return pin

pin = generar_pin()

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hackaton'
socketio = SocketIO(app)

@app.route('/', methods=['GET', 'POST'])
def inicio():
    return render_template("index.html")

@app.route('/paciente', methods=['GET', 'POST'])
def formulario_pacientes():
    return render_template("formulario_pacientes.html")

@app.route('/paramedicos/login', methods=['GET', 'POST'])
def login_paramedicos():
    return render_template("login_paramedicos.html")

@app.route('/paramedicos/formulario', methods=['GET', 'POST'])
def formulario_paramedicos():
    return render_template("formulario_paramedicos.html")

@app.route('/paciente/enviado', methods=['GET', 'POST'])
def enviado_pacientes():
    return render_template("enviado_pacientes.html")

@app.route('/paciente/pin', methods=['GET', 'POST'])
def consultar_pin():
    print(pin)
    if False:
        return redirect(url_for(inicio))
    return render_template("consultar_pin.html",pin = pin)

@app.route('/paramedicos/estado', methods=['GET', 'POST'])
def paramedicos_estado():
    return render_template("paramedicos_estado.html")

@socketio.on('pin solicitado')
def refrescar_pin():
    print("estamos en evento pin solicitado")
    while True:
        global pin
        pin = generar_pin()
        socketio.emit('new pin', pin)
        print(pin)
        time.sleep(30)
