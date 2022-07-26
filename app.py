from multiprocessing import AuthenticationError
from flask import Flask, render_template, request, redirect, url_for
from flask_socketio import SocketIO, emit
import random
import time

auth = False
paramedicos_determinantes_grave = ['no puede respirar', 'convulsiones', 'unhas y labios morados', 'hemorragia desangrante']
paramedicos_grave = ['inconsciente', 'pulso rapido']
paramedicos_intermedio = ['confusion','cefalea', 'sensibilidad a la luz', 'rigidez en el cuello', 'dolor en el hombro', 'saturacion menor a 95', 'fiebre alta', 'temperatura baja', 'dolor intenso','dolor moderado', 'hemorragia incontrolable', 'sangrado rectal', 'sangrado rectal', 'vomitos con sangre', 'golpe en la cabeza', 'golpe en el cuello', 'golpe en la espalda', 'fractura abierta']
paramedicos_leve = ['fiebre', 'lesiones leves', 'infeccion', 'perdida aguda de audicion', 'entumecimiento']

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

control = ['no puede respirar', 'inconsciente', 'pulso rapido', 'cefalea']

def triage_paramedicos(datos):
    contador_det_grave = 0
    contador_grave = 0
    contador_intermedio = 0
    contador_leve = 0
    for dato in datos:
        if dato in paramedicos_determinantes_grave:
            contador_det_grave += 1
        elif dato in paramedicos_grave:
            contador_grave += 1
        elif dato in paramedicos_intermedio:
            contador_intermedio += 1
        elif dato in paramedicos_leve: 
            contador_leve += 1
    
    if contador_det_grave > 0 or contador_grave > 1:
        return('rojo')
    elif contador_grave > 0 and contador_intermedio > 2:
        return('rojo')
    elif contador_intermedio > 2:
        return('naranja')
    elif contador_intermedio > 1 and contador_leve > 2:
        return('naranja')
    else:
        return('verde')


print(triage_paramedicos(control))
