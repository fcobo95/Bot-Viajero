# Imports section
from flask import Flask, json, Response, request
from pymongo import MongoClient
import networkx as nx
import matplotlib.pyplot as plt
import os
import socket
import datetime
from bson import ObjectId

app = Flask(__name__)

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
    # Mongo AWS Database Connection
    uri = "mongodb://ecoboe249:viper1829@ds153609.mlab.com:53609/bootowl"
    clienteWeb = MongoClient(uri)
    cloudDatabase = clienteWeb.MongoCloud
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


@app.route('/', methods=['GET'])
def index():
    return '<h1>Index Page</h1>'


@app.route('/api/get-route', methods=['POST', 'GET'])
def getRoute():
    try:
        losParametros = request.args
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


def definaElUsuario():
    elUsuario = request.remote_addr
    laSolicitud = localDatabase.Usuarios.find_one({"_id": elUsuario})
    if laSolicitud != None:
        elUsuario = laSolicitud["Nombre"]
    return elUsuario


def ingreseElLog(laAccion):
    elUsuario = definaElUsuario()
    elLog = {
        "_id": str(ObjectId()),
        "Usuario": elUsuario,
        "Fecha": datetime.datetime.now(),
        "Accion": laAccion
    }
    # cloudDatabase.Log_Operaciones.insert_one(elLog)
    localDatabase.Log_Operaciones.insert_one(elLog)


def formateeElError(e):
    elErrorComoTexto = str(e)
    elEnunciado = "Lo lamento. Ha ocurrido un error " + elErrorComoTexto
    elEnunciadoComoJSON = json.dumps(elEnunciado)
    elErrorHTTP = elErrorComoTexto[:3]
    laActividad = elErrorComoTexto
    ingreseElLog(laActividad)
    return Response(elEnunciadoComoJSON, elErrorHTTP, mimetype="application/json")


if __name__ == '__main__':
    app.run(debug=True, port=5000, host="0.0.0.0")
