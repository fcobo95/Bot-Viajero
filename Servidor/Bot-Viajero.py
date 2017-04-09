# SECCION PARA IMPORTAR MODULOS NECESARIOS
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

# SE CREA LA APLICACION DE FLASK, SE DEFINE LA LLAVE SECRETA PARA LA CREACION DE TOKENS,
# SE INICIALIZA LA AUTENTICACION BASICA Y SE IMPLEMENTA CROSS-DOMAIN CON CORS
app = Flask(__name__)
app.config['SECRET_KEY'] = 'JE9395ccce'
auth = HTTPBasicAuth()
CORS(app)

__Creators__ = 'Joshua Campos and Erick Cobo'


# ESTA FUNCION LEE CADA JSON DENTRO DE LA CARPETA DE NODOS EN LA CARPETA DE DOCUMENTOS,
# CREA EL NODO RESPECTIVO Y LE AGREGA EL JSON AL NODO
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


# ESTA FUNCION LEE CADA JSON DENTRO DE LA CARPETA DE NODOS EN LA CARPETA DE DOCUMENTOS,
# Y CREA LAS ARISTAS DEL GRAFO SEGUN LAS RELACIONES QUE ESTAN EN EL JSON Y LE ASIGNA
# EL PESO CORRESPONDIENTE A CADA ARISTA
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


# ESTA FUNCION CORRE UNA VEZ AL INICIAR EL SERVIDOR, EN DONDE CREA LA CONEXION CON LA BASE
# DE DATOS LOCAL, CREA EL GRAFO, Y UTILIZA LAS FUNCIONES ANTERIORES PARA CREAR LOS NODOS
# Y LAS ARISTAS.
with app.app_context():
    print("Cargando configuración...")
    clienteLocal = MongoClient('localhost', 27017)
    localDatabase = clienteLocal.MongoLocal
    elGrafo = nx.DiGraph()
    os.chdir('../')
    os.chdir('Documentos/Nodos')
    crearNodos()
    crearAristas()
    os.chdir('../../')
    os.chdir('Servidor/')


# ESTE METODO VERIFICA QUE EL USUARIO SEA VALIDO, AL RECIBIR DOS PARAMETROS. PRIMERO REVISA SI
# LO QUE RECIBE ES UN TOKEN Y SI ES VALIDO, SI NO ES ASI, BUSCA EL USUARIO EN LA BASE DE DATOS
# Y VERIFICA SI EL USUARIO Y LA CONTRASENA COINCIDEN CON LOS REGISTROS.
@auth.verify_password
def verifiqueContrasena(usuario_o_token, password):
    try:
        elUsuario = verifiqueToken(usuario_o_token)
        if elUsuario is None:
            elUsuario = localDatabase.Usuarios.find_one({'Usuario': usuario_o_token})
            if elUsuario is not None:
                laContrasena = elUsuario['Contrasena']
                if laContrasena != password:
                    return False
                else:
                    return True
        else:
            return True
    except Exception as e:
        return formateeElError(e)


# ESTA FUNCION RECIBE UN FORM, EL CUAL PARSEA PARA OBTENER TODOS LOS DATOS INDIVIDUALES. REVISA
# SI EL USUARIO YA EXISTE, Y SI FUERA ASI, ENVIA UN MENSAJE DE ERROR; SI NO EXISTE, CREA EL
# USUARIO Y LO INGRESA A LA BASE DE DATOS.
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


# ESTE METODO VERIFICA LOS CREDENCIALES ENVIADOS EN EL HEADER, Y LOS DECODIFICA PARA OBTENER
# EL USUARIO Y CONTRASENA ORIGINALES. POSTERIORMENTE, CREA UN TOKEN UTILIZANDO ESOS DATOS
# Y SE LO ENVIA AL CLIENTE.
@app.route('/api/login')
@auth.login_required
def obtengaToken():
    try:
        laAutorizacion = request.headers.get('authorization')
        elCodigo = laAutorizacion[6:]
        laAutenticacion = base64.b64decode(elCodigo)
        laAutenticacionComoTexto = laAutenticacion.decode("utf-8")
        losCredenciales = laAutenticacionComoTexto.split(':')
        elUsuario = losCredenciales[0]
        laContrasena = losCredenciales[1]
        elToken = genereToken(elUsuario, laContrasena)
        laRespuesta = {'Token': elToken.decode('ascii')}
        laAccion = "Login"
        ingreseElLog(laAccion)
        return jsonify(laRespuesta)
    except Exception as e:
        return formateeElError(e)


# ESTE METODO RECIBE UN JSON CON LA INFORMACION CORRESPONDIENTE PARA BUSCAR UNA RUTA. SE BUSCA
# LA RUTA MAS CORTA, Y SE TRAE LA INFORMACION CORRESPONDIENTE DE CADA UNO DE LOS NODOS QUE POSEE
# ESA RUTA, SEGUN LA PRIORIDAD ELEGIDA POR EL USUARIO. LUEGO SE ENVIA TODA ESTA INFORMACION AL CLIENTE.
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


# ESTE METODO RECIBE UN JSON CON LA INFORMACION CORRESPONDIENTE PARA BUSCAR UNA RUTA. BUSCA LAS
# CUATRO SIGUIENTES RUTAS MAS CORTAS, Y LUEGO RECORRE CADA RUTA Y TRAE LA INFORMACION CORRESPONDIENTE
# DE CADA NODO. LUEGO LE ENVIA AL CLIENTE TODA LA INFORMACION OBTENIDA.
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


# ESTA FUNCION REVISA EL USUARIO DE LA SESION. SI REALIZA UNA CONEXION DIRECTA CON EL AUTENTICADOR,
# SE OBTIENE DE AHI; SINO SE REVISA LOS CREDENCIALES DEL HEADER, SE DECODIFICAN, Y SE OBTIENE EL
# USUARIO.
def definaElUsuario():
    elUsuario = auth.username()
    if elUsuario == "":
        laAutorizacion = request.headers.get('authorization')
        elCodigo = laAutorizacion[6:]
        laAutenticacion = base64.b64decode(elCodigo)
        elToken = laAutenticacion.decode("utf-8")
        elUsuario = verifiqueToken(elToken)
    return elUsuario


# ESTA FUNCION CREA CADA LOG DE OPERACIONES. PRIMERO DEFINE EL USUARIO QUE REALIZA LA ACCION,
# LUEGO CREA EL LOG Y LO INGRESA A LA BASE DE DATOS.
def ingreseElLog(laAccion):
    elUsuario = definaElUsuario()
    elLog = {
        "_id": str(ObjectId()),
        "Usuario": elUsuario,
        "Fecha": datetime.datetime.now(),
        "Accion": laAccion
    }
    localDatabase.Log_Operaciones.insert_one(elLog)


# ESTA FUNCION OBTIENE LOS ERRORES, LOS FORMATEA Y ENVIA UNA RESPUESTA CON LA
# INFORMACION CORRESPONDIENTE.
def formateeElError(e):
    elErrorComoTexto = str(e)
    elEnunciado = "Lo lamento. Ha ocurrido un error " + elErrorComoTexto
    elEnunciadoComoJSON = json.dumps(elEnunciado)
    elErrorHTTP = elErrorComoTexto[:3]
    laActividad = elErrorComoTexto
    ingreseElLog(laActividad)
    return Response(elEnunciadoComoJSON, elErrorHTTP, mimetype="application/json")


# ESTA FUNCION CREA UN TOKEN DE AUTENTICACION. SE DEFINE LA SERIE SEGUN LA LLAVE SECRETA,
# Y LUEGO CREA EL TOKEN UTILIZANDO EL USUARIO Y CONTRASENA QUE RECIBE COMO PARAMETRO. CADA
# TOKEN EXPIRA CADA MEDIA HORA.
def genereToken(usuario, contrasena, expiration=1800):
    laSerie = Serializer(app.config['SECRET_KEY'], expires_in=expiration)
    elToken = laSerie.dumps({'Usuario': usuario, 'Contrasena': contrasena})
    return elToken


# ESTE METODO VERIFICA SI EL TOKEN ES VALIDO. DEFINE LA SERIE SEGUN LA LLAVE SECRETA,
# LUEGO CARGA EL TOKEN Y LO DECODIFICA SEGUN LA SERIE, Y REVISA SI EL TOKEN EXPIRO,
# SI ES INVALIDO, O SINO, OBTIENE EL USUARIO Y LO DEVUELVE.
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


# AQUI SE INICIALIZA EL PROGRAMA
if __name__ == '__main__':
    app.run(debug=True, port=5000, host="0.0.0.0")
