from flask import Flask, render_template, request, redirect, url_for
from flask_socketio import SocketIO, emit
import random
import time

auth = False
paramedicos_determinantes_grave = ['dificultad al respirar', 'convulsiones', 'coloracion morada en unhas o labios', 'mucho sangrado', 'hemorragia desangrante', 'sangrado abundante']
paramedicos_grave = ['inconciente', 'pulso acelerado']
paramedicos_intermedio = ['confundido','en la cabeza', 'sensibilidad a la luz', 'rigidez en el cuello', 'en el hombro', 'fiebre alta', 'dolor intenso','dolor moderado', 'hemorragia incontrolable', 'vomito o diarrea con sangre', 'golpe en la cabeza', 'golpe en el cuello', 'golpe en la espalda', 'fractura abierta']
paramedicos_leve = ['fiebre', 'lesiones leves', 'infeccion', 'perdida de la audicion', 'entumecimiento']

import sqlite3 as sql
### Crea la base de datos-------------------------------
def createDB():                              # Creamos la Base de Datos
    conn=sql.connect("AppDB.db")
    conn.commit()
    conn.close()

### Crea tabla PARAMEDICOS------------------------------
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

### Busca el pin en la lista----------------------------
def BuscarPin(pin):
    conn = sql.connect("AppDB.db")
    cursor = conn.cursor()
    instruccion=f"SELECT * FROM FormPacientes WHERE pin LIKE {pin}"
    cursor.execute(instruccion)
    paciente = cursor.fetchall()[0]
    conn.commit()
    conn.close()  
    return paciente

### Crea la tabla de FORMULARIOS DE PARAMEDICOS---------
def creatTableFormularioParamedicos():                           # Crear tabla para Solicitudes
    conn = sql.connect("AppDB.db")
    cursor = conn.cursor()
    cursor.execute(
        """ CREATE TABLE IF NOT EXISTS FormParamedicos (
            id integer primary key AUTOINCREMENT,
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

### Crea la tabla de FORMULARIOS DE PACIENTES-----------
def creatTableFormularioPacientes():                           # Crear tabla para Solicitudes
    conn = sql.connect("AppDB.db")
    cursor = conn.cursor()
    cursor.execute(
        """ CREATE TABLE IF NOT EXISTS FormPacientes (
            id integer primary key AUTOINCREMENT,
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
            pin text,
            verificado integer default 0
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


def cambiarVerificacion(pin):         # Insertar fila
    conn = sql.connect("AppDB.db")
    cursor = conn.cursor()
    instruccion = f"UPDATE FormPacientes SET verificado = 1 WHERE pin LIKE '{pin}'"
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
    id = cursor.lastrowid
    print(id)
    conn.commit()
    conn.close()
    return id

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


def obtener_todas_las_solicitudes():
    conn = sql.connect("AppDB.db")
    cursor = conn.cursor()

    cursor.execute(f"SELECT * FROM FormPacientes WHERE verificado LIKE 0")
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
            resultado = generar_descripcion(s[0], "FormPacientes")
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
                "pin": s[22],
                "triage": resultado["triage"],
                "descripcion": resultado["descripcion"]
            })

        for s in resultados_paramedicos:
            resultado = generar_descripcion(s[0], "FormParamedicos")
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
                "comentarios": s[21],
                "triage": resultado["triage"],
                "descripcion": resultado["descripcion"]
            })

        return solicitudes

    return []


def generar_descripcion(id, tabla):
    conn = sql.connect("AppDB.db")
    cursor = conn.cursor()
    instruccion = f"SELECT * FROM '{tabla}' WHERE id LIKE '{id}'"
    cursor.execute(instruccion)
    lista=cursor.fetchall()[0]
    descripcion = 'LLegando paciente con: '
    for elemento in lista:
        if elemento != 'sin problemas' and elemento != '[]' and elemento != '' and elemento != None:
            if elemento == "dolor moderado" or elemento == "dolor intenso":
                descripcion += f'{elemento} '
            else:
                descripcion += f'{elemento}, '
    
    print(descripcion)
    return {
        "triage": triage_paramedicos(lista),
        "descripcion" : descripcion
    }


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

@app.route('/verficarpin', methods=['GET'])
def verificar_pin():
    pin=request.args["pin"]
    # TO DO: Hacer update de verificacion del ROW con el PIN X
    cambiarVerificacion(pin)
    socketio.emit('verificar pin')
    return redirect(url_for("recepcion_lista"))

@app.route('/recepcion/login', methods=['GET', 'POST'])
def login_recepcion():
    if request.method == 'POST':
        email_medico = request.form['correos']
        contrasena_medico = request.form['contrasena']
        valor = verificarParmedico(email_medico, contrasena_medico)
        if valor==1:
            return redirect('/recepcion/lista')
        elif valor == 0:
            return redirect("/recepcion/login?error=1")
    return render_template("login_recepcion.html")



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
        id = insertRowFormPacientes(nombre_completo, cedula, respiracion, piel, fiebre, neurologicos, conciencia, dolor, lugar_dolor, vomito_diarrea, pulso, sangrado, lugar_sangrado, alergias, otras_alergias, cronicas, otras_cronicas, alimento, evento, tipo_sangre, comentarios)
        print(id)
        socketio.emit('nueva solicitud')
    return render_template("form_enviado_pacientes.html", id=id)



@app.route('/paciente/pin/<id>', methods=['GET', 'POST'])
def consultar_pin(id):
    pin = generar_pin()
    conn = sql.connect("AppDB.db")
    cursor = conn.cursor()
    instruccion = f"UPDATE FormPacientes SET pin = '{pin}' WHERE id LIKE '{id}'"
    cursor.execute(instruccion)
    conn.commit()
    conn.close()
    return render_template("consultar_pin.html", pin=pin)


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
        socketio.emit('nueva solicitud')

    return render_template("paramedicos_estado.html")


@app.route('/paramedicos/confirmado', methods=['GET', 'POST'])
def formulario_estado_confirmado():
    return render_template("paramedicos_estado_confirmado.html")


@app.route('/recepcion/confirmado', methods=['GET', 'POST'])
def recepcion_confirmado():
    return render_template("confirmacion_de_solicitud.html")


@app.route('/recepcion/lista', methods=['GET'])
def recepcion_lista():
    solicitudes = obtener_todas_las_solicitudes()

    return render_template("lista_de_solicitudes.html", solicitudes=solicitudes)


@socketio.on('pin solicitado')
def refrescar_pin(id):
    print("estamos en evento pin solicitado")
    while True:
        time.sleep(30)
        pin = generar_pin()
        conn = sql.connect("AppDB.db")
        cursor = conn.cursor()
        instruccion = f"UPDATE FormPacientes SET pin = '{pin}' WHERE id LIKE '{id}'"
        cursor.execute(instruccion)
        conn.commit()
        conn.close()
        socketio.emit('new pin', pin)
        print(pin)

control = ['no puede respirar', 'inconsciente', 'pulso rapido', 'cefalea']



if __name__ == "app":
    createDB()
    creatTableParamedicos()
    creatTableFormularioParamedicos()
    creatTableFormularioPacientes()
