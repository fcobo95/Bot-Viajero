# Imports section
from flask import Flask, json, Response, request, jsonify
from pymongo import MongoClient
import networkx as nx
import os
import datetime
import base64
from bson import ObjectId
from flask_cors import CORS
from flask_httpauth import HTTPBasicAuth
from itsdangerous import (TimedJSONWebSignatureSerializer
                          as Serializer, BadSignature, SignatureExpired)

app = Flask(__name__)
app.config['SECRET_KEY'] = '12345'
auth = HTTPBasicAuth()
CORS(app)

__Creators__ = 'Joshua Campos and Erick Cobo'


def crearNodos():
    elIndice = 1
    for cadaArchivo in range(len(os.listdir(os.getcwd()))):
        elNodoPrincipal = "N" + str(elIndice)
        elArchivo = open(elNodoPrincipal + ".json").read()
        elArchivoComoJSON = json.loads(elArchivo)
        elGrafo.add_node(elNodoPrincipal, Data=elArchivoComoJSON)
        elIndice += 1
        if elIndice == 10 or elIndice == 17:
            elIndice += 1


def crearAristas():
    elIndice = 1
    for cadaArchivo in range(len(os.listdir(os.getcwd()))):
        elNodoPrincipal = "N" + str(elIndice)
        elArchivo = open(elNodoPrincipal + ".json").read()
        elArchivoComoDiccionario = json.loads(elArchivo)
        for cadaLlave in elArchivoComoDiccionario:
            laDistancia = elArchivoComoDiccionario[cadaLlave]["Distancia"]
            elGrafo.add_edge(elNodoPrincipal, cadaLlave, Weight=laDistancia)
        elIndice += 1
        if elIndice == 10 or elIndice == 17:
            elIndice += 1


with app.app_context():
    print("Cargando configuración...")
    # Mongo Local Database Connection
    clienteLocal = MongoClient('localhost', 27017)
    localDatabase = clienteLocal.MongoLocal
    # Graph Creation and Configuration
    elGrafo = nx.DiGraph()
    os.chdir('../')
    os.chdir('Documentos/Nodos')
    crearNodos()
    crearAristas()
    os.chdir('../../')
    os.chdir('Servidor/')


@auth.get_password
def getPassword(elUsuario):
    laVerificacion = localDatabase.Usuarios.find_one({'Usuario': elUsuario})
    if laVerificacion is not None:
        return laVerificacion['Contrasena']
    else:
        return None


@app.route('/', methods=['GET'])
@auth.verify_password
def login():
    try:
        laRespuesta = {"id": 1, "Mensaje": "Welcome, " + auth.username() + "!"}
        laRespuestaComoJSON = json.dumps(laRespuesta)
        laAccion = "Login"
        ingreseElLog(laAccion)
        return Response(laRespuestaComoJSON, 200, mimetype='application/json')
    except Exception as e:
        return formateeElError(e)


@app.route('/api/create-user', methods=['POST'])
def createUser():
    try:
        losParametros = request.form
        laIdentificacion = str(ObjectId())
        elNombre = losParametros['Nombre']
        elApellido = losParametros['Apellido']
        elCorreo = losParametros['Correo']
        elUsuario = losParametros['Usuario']
        laContrasena = losParametros['Contrasena']
        laVerificacion = localDatabase.Usuarios.find_one({'Usuario': elUsuario})
        if laVerificacion is not None:
            laRespuesta = {"id": 2, "Mensaje": "Error: El usuario ya existe."}
            laRespuestaComoJSON = json.dumps(laRespuesta)
            laAccion = "Create user error."
            ingreseElLog(laAccion)
            return Response(laRespuestaComoJSON, 200, mimetype='application/json')
        elRegistro = {
            "_id": laIdentificacion,
            "Nombre": elNombre,
            "Apellido": elApellido,
            "Correo": elCorreo,
            "Usuario": elUsuario,
            "Contrasena": laContrasena
        }
        localDatabase.Usuarios.insert_one(elRegistro)
        laRespuesta = {"id": 1, "Mensaje": "El usuario se ha creado exitosamente."}
        laRespuestaComoJSON = json.dumps(laRespuesta)
        laAccion = "Create user: " + elUsuario
        ingreseElLog(laAccion)
        return Response(laRespuestaComoJSON, 200, mimetype='application/json')
    except Exception as e:
        return formateeElError(e)


@app.route('/api/get-route', methods=['POST'])
@auth.login_required
def getRoute():
    try:
        losParametros = request.json
        elOrigen = "N" + losParametros['Origen']
        elDestino = "N" + losParametros['Destino']
        laPrioridad = losParametros['Prioridad']
        elIndice = 0
        laRuta = nx.dijkstra_path(elGrafo, elOrigen, elDestino)
        laCantidadDeViajes = len(laRuta) - 1
        laRutaSeleccionada = {'Orden': laRuta}
        for cadaViaje in range(laCantidadDeViajes):
            elNodoActual = laRuta[elIndice]
            elNodoSiguiente = laRuta[elIndice + 1]
            elTransporteDisponible = elGrafo.node[elNodoActual]['Data'][elNodoSiguiente]['Transporte']
            laDistancia = elGrafo[elNodoActual][elNodoSiguiente]['Weight']
            if laDistancia < 5:
                if laPrioridad == 'E':
                    elTransporteAdecuado = elTransporteDisponible['Bus']
                    laRutaSeleccionada[elNodoActual] = {'Bus': elTransporteAdecuado}
                else:
                    elTransporteAdecuado = elTransporteDisponible['Taxi']
                    laRutaSeleccionada[elNodoActual] = {'Taxi': elTransporteAdecuado}
            elif 5 <= laDistancia < 10:
                if laPrioridad == 'E':
                    elTransporteAdecuado = elTransporteDisponible['Bus']
                    laRutaSeleccionada[elNodoActual] = {'Bus': elTransporteAdecuado}
                else:
                    elTransporteAdecuado = elTransporteDisponible['Tren']
                    laRutaSeleccionada[elNodoActual] = {'Tren': elTransporteAdecuado}
            else:
                if laPrioridad == 'E':
                    elTransporteAdecuado = elTransporteDisponible['Tren']
                    laRutaSeleccionada[elNodoActual] = {'Tren': elTransporteAdecuado}
                else:
                    elTransporteAdecuado = elTransporteDisponible['Avion']
                    laRutaSeleccionada[elNodoActual] = {'Avion': elTransporteAdecuado}
            elIndice += 1
        laRutaSeleccionadaComoJSON = json.dumps(laRutaSeleccionada)
        laAccion = elOrigen + " - " + elDestino + " : " + laPrioridad
        ingreseElLog(laAccion)
        return Response(laRutaSeleccionadaComoJSON, status=200, mimetype='application/json')
    except Exception as e:
        return formateeElError(e)


@app.route('/api/get-alternatives', methods=['POST'])
@auth.login_required
def getAlternatives():
    try:
        losParametros = request.json
        elOrigen = "N" + losParametros['Origen']
        elDestino = "N" + losParametros['Destino']
        laPrioridad = losParametros['Prioridad']
        otrasRutas = (list(nx.shortest_simple_paths(elGrafo, elOrigen, elDestino)))[1:5]
        lasAlternativas = {}
        for i in range(4):
            unaRuta = otrasRutas[i]
            laCantidadDeViajes = len(unaRuta) - 1
            laAlternativa = "Alternativa" + str(i + 1)
            lasAlternativas[laAlternativa] = {'Orden': unaRuta}
            for n in range(laCantidadDeViajes):
                elNodoActual = unaRuta[n]
                elNodoSiguiente = unaRuta[n + 1]
                elTransporteDisponible = elGrafo.node[elNodoActual]['Data'][elNodoSiguiente]['Transporte']
                laDistancia = elGrafo[elNodoActual][elNodoSiguiente]['Weight']
                if laDistancia < 5:
                    if laPrioridad == 'E':
                        elTransporteAdecuado = elTransporteDisponible['Bus']
                        lasAlternativas[laAlternativa][elNodoActual] = {'Bus': elTransporteAdecuado}
                    else:
                        elTransporteAdecuado = elTransporteDisponible['Taxi']
                        lasAlternativas[laAlternativa][elNodoActual] = {'Taxi': elTransporteAdecuado}
                elif 5 <= laDistancia < 10:
                    if laPrioridad == 'E':
                        elTransporteAdecuado = elTransporteDisponible['Bus']
                        lasAlternativas[laAlternativa][elNodoActual] = {'Bus': elTransporteAdecuado}
                    else:
                        elTransporteAdecuado = elTransporteDisponible['Tren']
                        lasAlternativas[laAlternativa][elNodoActual] = {'Tren': elTransporteAdecuado}
                else:
                    if laPrioridad == 'E':
                        elTransporteAdecuado = elTransporteDisponible['Tren']
                        lasAlternativas[laAlternativa][elNodoActual] = {'Tren': elTransporteAdecuado}
                    else:
                        elTransporteAdecuado = elTransporteDisponible['Avion']
                        lasAlternativas[laAlternativa] = {'Avion': elTransporteAdecuado}
        lasAlternativasComoJSON = json.dumps(lasAlternativas)
        laAccion = "Alternativas: " + elOrigen + " - " + elDestino + " : " + laPrioridad
        ingreseElLog(laAccion)
        return Response(lasAlternativasComoJSON, status=200, mimetype='application/json')
    except Exception as e:
        return formateeElError(e)


def definaElUsuario():
    elUsuario = auth.username()
    if elUsuario == "":
        elUsuario = request.remote_addr
    return elUsuario


def ingreseElLog(laAccion):
    elUsuario = definaElUsuario()
    elLog = {
        "_id": str(ObjectId()),
        "Usuario": elUsuario,
        "Fecha": datetime.datetime.now(),
        "Accion": laAccion
    }
    localDatabase.Log_Operaciones.insert_one(elLog)


def formateeElError(e):
    elErrorComoTexto = str(e)
    elEnunciado = "Lo lamento. Ha ocurrido un error " + elErrorComoTexto
    elEnunciadoComoJSON = json.dumps(elEnunciado)
    elErrorHTTP = elErrorComoTexto[:3]
    laActividad = elErrorComoTexto
    ingreseElLog(laActividad)
    return Response(elEnunciadoComoJSON, elErrorHTTP, mimetype="application/json")


@app.route('/api/login')
@auth.login_required
def obtengaToken():
    laAutorizacion = request.headers.get('authorization')
    elCodigo = laAutorizacion[6:]
    laAutenticacion = base64.b64decode(elCodigo)
    laAutenticacionComoTexto = laAutenticacion.decode("utf-8")
    losCredenciales = laAutenticacionComoTexto.split(':')
    elUsuario = losCredenciales[0]
    laContrasena = losCredenciales[1]
    elToken = genereToken(elUsuario, laContrasena)
    laRespuesta = {'Token': elToken.decode('ascii')}
    return jsonify(laRespuesta)


def genereToken(usuario, contrasena, expiration=1800):
    laSerie = Serializer(app.config['SECRET_KEY'], expires_in=expiration)
    elToken = laSerie.dumps({'Usuario': usuario, 'Contrasena': contrasena})
    return elToken


def verifiqueToken(token):
    laSerie = Serializer(app.config['SECRET_KEY'])
    try:
        losDatos = laSerie.loads(token)
    except SignatureExpired:
        return None
    except BadSignature:
        return None
    elUsuario = losDatos['Usuario']
    return elUsuario


@auth.verify_password
def verifiqueContrasena(usuario_o_token, password):
    elUsuario = verifiqueToken(usuario_o_token)
    if elUsuario is None:
        elUsuario = localDatabase.Usuarios.find_one({'Usuario': usuario_o_token})
        if elUsuario['Contrasena'] != password:
            return False
    return True


if __name__ == '__main__':
    app.run(debug=True, port=5000, host="0.0.0.0")
