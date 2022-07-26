from flask import Flask, render_template, request, redirect, url_for
from flask_socketio import SocketIO, emit



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
    return render_template("consultar_pin.html")

@app.route('/paramedicos/estado', methods=['GET', 'POST'])
def paramedicos_estado():
    return render_template("paramedicos_estado.html")


