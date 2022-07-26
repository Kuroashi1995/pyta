from flask import Flask, render_template, request, redirect, url_for
from flask_socketio import SocketIO, emit
import sqlite3 as sql

def createDB():                              # Creamos la Base de Datos
    conn=sql.connect("AppDB.db")
    conn.commit()
    conn.close()


def creatTableParamedicos():                           # Crear tabla para Paramedicos
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


def creatTableSolicitudes():                           # Crear tabla para Solicitudes
    conn = sql.connect("AppDB.db")
    cursor = conn.cursor()
    cursor.execute(
        """ CREATE TABLE IF NOT EXISTS solicitudes (
            id_sol integer primary key AUTOINCREMENT,
            estado text NOT NULL,
            tipo text NOT NULL
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
        nombre_medico = request.form['nombres']
        email_medico = request.form['correos']
        contrasena_medico = request.form['contrasena']
        insertRowParamedicos(nombre_medico, email_medico, contrasena_medico)
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


if __name__ == "app":
    createDB()
    creatTableParamedicos()
    creatTableSolicitudes()