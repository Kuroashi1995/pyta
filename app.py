from flask import Flask, render_template, request, redirect, url_for, abort
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

def obtener_solicitud_con_pin(pin):
    conn = sql.connect("AppDB.db")
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM FormPacientes WHERE pin LIKE '{pin}'")

    solicitudes = cursor.fetchall() # Te trae una lista de listas
    conn.commit()
    conn.close()

    if len(solicitudes) > 0:

        def from_string_to_list(text):
            return text.replace('[', '').replace(']', '').split()

        solicitud = {
            "nombre_completo": solicitudes[0][1],
            "cedula": solicitudes[0][2],
            "respiracion": solicitudes[0][3],
            "piel": solicitudes[0][4],
            "fiebre": solicitudes[0][5],
            "neurologicos": solicitudes[0][6],
            "conciencia": solicitudes[0][7],
            "dolor": solicitudes[0][8],
            "lugar_dolor": from_string_to_list(solicitudes[0][9]),
            "vomito_diarrea": solicitudes[0][10],
            "pulso": solicitudes[0][11],
            "sangrado": solicitudes[0][12],
            "lugar_sangrado": solicitudes[0][13],
            "alergias": from_string_to_list(solicitudes[0][14]),
            "otras_alergias": solicitudes[0][15],
            "cronicas": from_string_to_list(solicitudes[0][16]),
            "otras_cronicas": solicitudes[0][17],
            "alimento": solicitudes[0][18],
            "evento": from_string_to_list(solicitudes[0][19]),
            "tipo_sangre": solicitudes[0][20],
            "comentarios": solicitudes[0][21],
            "pin": solicitudes[0][22]
        }
        return solicitud

    return

def obtener_todas_las_solicitudes():
    conn = sql.connect("AppDB.db")
    cursor = conn.cursor()

    cursor.execute(f"SELECT * FROM FormPacientes")
    resultados_pacientes = cursor.fetchall() # Te trae una lista de listas

    cursor.execute(f"SELECT * FROM FormParamedicos")
    resultados_paramedicos = cursor.fetchall() # Te trae una lista de listas

    conn.commit()
    conn.close()

    if len(resultados_pacientes) > 0:

        solicitudes = []

        def from_string_to_list(text):
            return text.replace('[', '').replace(']', '').split(',')

        for s in resultados_pacientes:  
            solicitudes.append({
                "id": s[0],
                "nombre_completo": s[1],
                "cedula": s[2],
                "respiracion": s[3],
                "piel": s[4],
                "fiebre": s[5],
                "neurologicos": s[6],
                "conciencia": s[7],
                "dolor": s[8],
                "lugar_dolor": from_string_to_list(s[9]),
                "vomito_diarrea": s[10],
                "pulso": s[11],
                "sangrado": s[12],
                "lugar_sangrado": s[13],
                "alergias": from_string_to_list(s[14]),
                "otras_alergias": s[15],
                "cronicas": from_string_to_list(s[16]),
                "otras_cronicas": s[17],
                "alimento": s[18],
                "evento": from_string_to_list(s[19]),
                "tipo_sangre": s[20],
                "comentarios": s[21],
                "pin": s[22]
            })

        for s in resultados_paramedicos:
            solicitudes.append({
                "id": s[0],
                "respiracion": s[1],
                "saturacion": s[2],
                "piel": s[3],
                "traumatismos": s[4],
                "temperatura": s[5],
                "neurologicos": s[6],
                "conciencia": s[7],
                "dolor": s[8],
                "lugar_dolor": from_string_to_list(s[9]),
                "vomito_diarrea": s[10],
                "pulso": s[11],
                "sangrado": s[12],
                "lugar_sangrado": s[13],
                "alergias": from_string_to_list(s[14]),
                "otras_alergias": s[15],
                "cronicas": from_string_to_list(s[16]),
                "otras_cronicas": s[17],
                "alimento": s[18],
                "evento": from_string_to_list(s[19]),
                "tipo_sangre": s[20],
                "comentarios": s[21]
            })

        return solicitudes

    return



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
@app.errorhandler(404)
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

@app.route('/recepcion/lista', methods=['GET', 'POST'])
def recepcion_lista():
    solicitudes = obtener_todas_las_solicitudes()
    return render_template("recepcion_lista.html", solicitudes=solicitudes)

@app.route('/recepcion/verificar', methods=['GET'])
def recepcion_verificar():
    print(request.args)
    pin = request.args['pin']
    solicitud = obtener_solicitud_con_pin(pin)
    if solicitud:
        return redirect(url_for('recepcion_solicitud', pin=pin))
    else:
        abort(404)

@app.errorhandler(404)
def solicitud_no_encontrada(error):
    print(error)
    return render_template('solicitud_no_encontrada.html'), 404


@app.route('/recepcion/solicitud/<pin>', methods=['GET'])
def recepcion_solicitud(pin=None):

    solicitud = obtener_solicitud_con_pin(pin)

    return render_template('recepcion_solicitud.html', solicitud=solicitud)


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
