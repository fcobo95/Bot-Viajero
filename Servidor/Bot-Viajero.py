# Imports section
from flask import Flask, json, Response, request
from pymongo import MongoClient
import networkx as nx
import matplotlib.pyplot as plt
import os
import socket

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
            # print(elGrafo.nodes())


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
            # print(elGrafo.edges())


with app.app_context():
    print("Cargando configuración...")
    # Mongo AWS Database Connection
    uri = "mongodb://ecoboe249:viper1829@ds153609.mlab.com:53609/bootowl"
    clientWeb = MongoClient(uri)
    # Mongo Local Database Connection
    clientLocal = MongoClient('localhost', 35250)
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


@app.route('/api/draw-map/')
def node_mapping():
    losNodos = elGrafo.nodes()
    lasRelaciones = elGrafo.edges()
    lasCosas = elGrafo.get_edge_data(elGrafo, losNodos, lasRelaciones)
    lasAdyacencias = elGrafo.adjacency_list()
    laRespuestaJSON = json.dumps(lasCosas)

    return Response(laRespuestaJSON, status=200, mimetype='application/json')


@app.route('/api/get-route', methods=['POST', 'GET'])
def getRoute():
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
    return Response(laRutaSeleccionadaComoJSON, status=200, mimetype='application/json')


def printNodes():
    nodes = elGrafo.nodes()

    return nodes


def printEdges():
    edges = elGrafo.edges()

    return edges


def printNodeDegree(node=1):
    degree = elGrafo.degree(node)

    return degree


def drawGraph(user=""):
    nx.draw(elGrafo)
    plt.savefig("C:\\Users\\" + user + "\\Pictures\\elGrafo.png")
    return plt.show()


if __name__ == '__main__':
    app.run(debug=True, port=5000, host="0.0.0.0")
