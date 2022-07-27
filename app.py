from flask import Flask, render_template, request, redirect, url_for
from flask_socketio import SocketIO, emit
import random
import time

auth = False
paramedicos_determinantes_grave = ['no puede respirar', 'convulsiones', 'unhas y labios morados', 'hemorragia desangrante']
paramedicos_grave = ['inconsciente', 'pulso rapido']
paramedicos_intermedio = ['confusion','cefalea', 'sensibilidad a la luz', 'rigidez en el cuello', 'dolor en el hombro', 'saturacion menor a 95', 'fiebre alta', 'temperatura baja', 'dolor intenso','dolor moderado', 'hemorragia incontrolable', 'sangrado rectal', 'sangrado rectal', 'vomitos con sangre', 'golpe en la cabeza', 'golpe en el cuello', 'golpe en la espalda', 'fractura abierta']
paramedicos_leve = ['fiebre', 'lesiones leves', 'infeccion', 'perdida aguda de audicion', 'entumecimiento']

import sqlite3 as sql

def createDB():                              # Creamos la Base de Datos
    conn=sql.connect("AppDB.db")
    conn.commit()
    conn.close()


def creatTableParamedicos():                  # Crear tabla para Paramedicos
    conn = sql.connect("AppDB.db")
    cursor = conn.cursor()
    cursor.execute(                 # create table if not exists
        """ CREATE TABLE IF NOT EXISTS paramedicos (
            id integer primary key AUTOINCREMENT,
            nombre text,
            correo text,
            contraseña text
        )"""                            # --------comprobar si es que la matricula es realmente un número o si tiene también letras-------
    )
    conn.commit()
    conn.close()


def BuscarPin(pin):
    conn = sql.connect("AppDB.db")
    cursor = conn.cursor()
    instruccion=f"SELECT * FROM FormPacientes WHERE pin LIKE {pin}"
    cursor.execute(instruccion)
    paciente = cursor.fetchall()
    conn.commit()
    conn.close()  
    return paciente


def creatTableFormularioParamedicos():                           # Crear tabla para Solicitudes
    conn = sql.connect("AppDB.db")
    cursor = conn.cursor()
    cursor.execute(
        """ CREATE TABLE IF NOT EXISTS FormParamedicos (
            id_form_para integer primary key AUTOINCREMENT,
            respiracion text,
            saturacion text,
            piel text,
            traumatismos text,
            temperatura text,
            neurologicos text,
            conciencia text,
            dolor text,
            lugar_dolor text,
            vomito_diarrea text,
            pulso text,
            sangrado text,
            lugar_sangrado text,
            alergias text,
            otras_alergias text,
            cronicas text,
            otras_cronicas text,
            alimento text,
            evento text,
            tipo_sangre text,
            comentarios text
        )"""
    )
    conn.commit()
    conn.close()

def creatTableFormularioPacientes():                           # Crear tabla para Solicitudes
    conn = sql.connect("AppDB.db")
    cursor = conn.cursor()
    cursor.execute(
        """ CREATE TABLE IF NOT EXISTS FormPacientes (
            id_form_paci integer primary key AUTOINCREMENT,
            nombre_completo text,
            cedula text,
            respiracion text,
            piel text,
            fiebre text,
            neurologicos text,
            conciencia text,
            dolor text,
            lugar_dolor text,
            vomito_diarrea text,
            pulso text,
            sangrado text,
            lugar_sangrado text,
            alergias text,
            otras_alergias text,
            cronicas text,
            otras_cronicas text,
            alimento text,
            evento text,
            tipo_sangre text,
            comentarios text,
            pin text
        )"""
    )
    conn.commit()
    conn.close()

def insertRowParamedicos(nombre, correo, contrasena):         # Insertar fila
    conn = sql.connect("AppDB.db")
    cursor = conn.cursor()
    instruccion = f"INSERT INTO paramedicos(nombre, correo, contraseña) VALUES ('{nombre}', '{correo}', '{contrasena}')"
    cursor.execute(instruccion)
    conn.commit()
    conn.close()

def insertRowFormParamedicos(respiracion, saturacion, piel, traumatismos, temperatura, neurologicos, conciencia, dolor, lugar_dolor, vomito_diarrea, pulso, sangrado, lugar_sangrado, alergias, otras_alergias, cronicas, otras_cronicas, alimento, evento, tipo_sangre, comentarios):         # Insertar fila
    conn = sql.connect("AppDB.db")
    cursor = conn.cursor()
    instruccion = f"INSERT INTO FormParamedicos(respiracion, saturacion, piel, traumatismos, temperatura, neurologicos, conciencia, dolor, lugar_dolor, vomito_diarrea, pulso, sangrado, lugar_sangrado, alergias, otras_alergias, cronicas, otras_cronicas, alimento, evento, tipo_sangre, comentarios) VALUES ('{respiracion}', '{saturacion}', '{piel}', '{traumatismos}', '{temperatura}', '{neurologicos}', '{conciencia}', '{dolor}', '{lugar_dolor}', '{vomito_diarrea}', '{pulso}', '{sangrado}', '{lugar_sangrado}', '{alergias}', '{otras_alergias}', '{cronicas}', '{otras_cronicas}', '{alimento}', '{evento}', '{tipo_sangre}', '{comentarios}')"
    cursor.execute(instruccion)
    conn.commit()
    conn.close()
def insertRowFormPacientes(nombre_completo, cedula, respiracion, piel, fiebre, neurologicos, conciencia, dolor, lugar_dolor, vomito_diarrea, pulso, sangrado, lugar_sangrado, alergias, otras_alergias, cronicas, otras_cronicas, alimento, evento, tipo_sangre, comentarios):         # Insertar fila
    conn = sql.connect("AppDB.db")
    cursor = conn.cursor()
    instruccion = f"INSERT INTO FormPacientes(nombre_completo, cedula, respiracion, piel, fiebre, neurologicos, conciencia, dolor, lugar_dolor, vomito_diarrea, pulso, sangrado, lugar_sangrado, alergias, otras_alergias, cronicas, otras_cronicas, alimento, evento, tipo_sangre, comentarios) VALUES ('{nombre_completo}', '{cedula}', '{respiracion}', '{piel}', '{fiebre}', '{neurologicos}', '{conciencia}', '{dolor}', '{lugar_dolor}', '{vomito_diarrea}', '{pulso}', '{sangrado}', '{lugar_sangrado}', '{alergias}', '{otras_alergias}', '{cronicas}', '{otras_cronicas}', '{alimento}', '{evento}', '{tipo_sangre}', '{comentarios}')"
    cursor.execute(instruccion)
    conn.commit()
    conn.close()

def verificarParmedico(correo, contrasena):
    conn = sql.connect("AppDB.db")
    cursor = conn.cursor()
    instruccion = f"SELECT * FROM paramedicos WHERE correo LIKE '{correo}'"
    cursor.execute(instruccion)
    datos_correo=cursor.fetchall()         # Te trae una lista de listas
    conn.commit()
    instruccion = f"SELECT * FROM paramedicos WHERE contraseña LIKE '{contrasena}'"
    cursor.execute(instruccion)
    datos_contrasena=cursor.fetchall()         # Te trae una lista de listas
    conn.commit()
    conn.close()

    if datos_correo != [] and datos_contrasena!=[]:
        print(datos_correo[0][2])              # Indice 0 es el mejor resultado
        print(datos_contrasena[0][3])
        return 1
    elif datos_correo == [] or datos_contrasena==[]:
        # print("Contraseña y/o Correo no coinciden")
        return 0

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
    if request.method == 'POST':
        email_medico = request.form['correos']
        contrasena_medico = request.form['contrasena']
        valor = verificarParmedico(email_medico, contrasena_medico)
        if valor==1:
            return redirect('/paramedicos/formulario')
        elif valor == 0:
            return redirect("/paramedicos/login?error=1")
    return render_template("login_paramedicos.html")



@app.route('/paramedicos/formulario', methods=['GET', 'POST'])
def formulario_paramedicos():
    return render_template("formulario_paramedicos.html")

@app.route('/paciente/enviado', methods=['GET', 'POST'])
def enviado_pacientes():
    if request.method == 'POST':
        nombre_completo = request.form['nombre_completo']
        cedula = request.form['cedula']
        respiracion = request.form['respiracion']
        piel = request.form['piel']
        fiebre = request.form['fiebre']
        neurologicos = request.form['neurologicos']
        conciencia = request.form['conciencia']
        dolor = request.form['dolor']
        lugar_dolor=[]
        if "lugar_dolor" in request.form.keys():
            lugar_dolor = request.form['lugar_dolor']
        vomito_diarrea = request.form['vomito_diarrea']
        pulso = request.form['pulso']
        sangrado = request.form['sangrado']
        lugar_sangrado = request.form['lugar_sangrado']
        alergias = []
        if "alergias" in request.form.keys():
            alergias = request.form['alergias']
        otras_alergias = request.form['otras_alergias']
        cronicas = []
        if "cronicas" in request.form.keys():
            cronicas = request.form['cronicas']
        otras_cronicas=request.form['otras_cronicas']
        alimento = request.form['alimento']
        evento = []
        if "eventos" in request.form.keys():
            evento = request.form['evento']
        tipo_sangre = request.form['tipo_sangre']
        comentarios = request.form['comentarios']
        insertRowFormPacientes(nombre_completo, cedula, respiracion, piel, fiebre, neurologicos, conciencia, dolor, lugar_dolor, vomito_diarrea, pulso, sangrado, lugar_sangrado, alergias, otras_alergias, cronicas, otras_cronicas, alimento, evento, tipo_sangre, comentarios)
    return render_template("form_enviado_pacientes.html")



@app.route('/paciente/pin', methods=['GET', 'POST'])
def consultar_pin():
    print(pin)
    if False:
        return redirect(url_for(inicio))
    return render_template("consultar_pin.html",pin = pin)

@app.route('/paramedicos/estado', methods=['GET', 'POST'])
def paramedicos_estado():
    if request.method == 'POST':
        respiracion = request.form['respiracion']
        saturacion = request.form['saturacion']
        piel =[]
        if "piel" in request.form.keys():
            piel = request.form['piel']
        traumatismos = request.form['traumatismos']
        temperatura = request.form['temperatura']
        neurologicos=[]
        if "neurologicos" in request.form.keys():
            neurologicos = request.form['neurologicos']
        conciencia = request.form['conciencia']
        dolor = request.form['dolor']
        lugar_dolor=[]
        if "lugar_dolor" in request.form.keys():
            lugar_dolor = request.form['lugar_dolor']
        vomito_diarrea = request.form['vomito_diarrea']
        pulso = request.form['pulso']
        sangrado = request.form['sangrado']
        lugar_sangrado = request.form['lugar_sangrado']
        alergias = []
        if "alergias" in request.form.keys():
            alergias = request.form['alergias']
        otras_alergias = request.form['otras_alergias']
        cronicas = []
        if "cronicas" in request.form.keys():
            cronicas = request.form['cronicas']
        otras_cronicas=request.form['otras_cronicas']
        alimento = request.form['alimento']
        evento = []
        if "eventos" in request.form.keys():
            evento = request.form['evento']
        tipo_sangre = request.form['tipo_sangre']
        comentarios = request.form['comentarios']
        insertRowFormParamedicos(respiracion, saturacion, piel, traumatismos, temperatura, neurologicos, conciencia, dolor, lugar_dolor, vomito_diarrea, pulso, sangrado, lugar_sangrado, alergias, otras_alergias, cronicas, otras_cronicas, alimento, evento, tipo_sangre, comentarios)

    return render_template("paramedicos_estado.html")

@app.route('/paramedicos/confirmado', methods=['GET', 'POST'])
def formulario_estado_confirmado():
    return render_template("paramedicos_estado_confirmado.html")

@app.route('/recepcion/confirmado', methods=['GET', 'POST'])
def recepcion_confirmado():
    return render_template("confirmacion_de_solicitud.html")

@app.route('/recepcion/lista', methods=['GET', 'POST'])
def recepcion_lista():
    return render_template("lista_de_solicitudes.html")

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
if __name__ == "app":
    createDB()
    creatTableParamedicos()
    creatTableFormularioParamedicos()
    creatTableFormularioPacientes()
