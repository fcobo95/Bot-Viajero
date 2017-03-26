# Imports section
from flask import Flask, json, Response, request, jsonify, render_template
from pymongo import MongoClient
import networkx as nx
import matplotlib.pyplot as plt
import datetime
import os

app = Flask(__name__)


def crearNodos():
    elIndice = 1
    for cadaArchivo in range(len(os.listdir(os.getcwd()))):
        elNodoPrincipal = "N" + str(elIndice)
        elArchivo = open(elNodoPrincipal+".json").read()
        elArchivoComoJSON = json.dumps(elArchivo)
        elGrafo.node[elNodoPrincipal] = elArchivoComoJSON
        elIndice += 1
        if elIndice == 10 or elIndice == 17:
            elIndice += 1
    print(elGrafo.nodes())


def crearAristas():
    elIndice = 1
    for cadaArchivo in range(len(os.listdir(os.getcwd()))):
        elNodoPrincipal = "N" + str(elIndice)
        elArchivo = open(elNodoPrincipal+".json").read()
        elArchivoComoDiccionario = json.loads(elArchivo)
        for cadaLlave in elArchivoComoDiccionario:
            laDistancia = elArchivoComoDiccionario[cadaLlave]["Distancia"]
            elGrafo.add_edge(elNodoPrincipal, cadaLlave, weight=laDistancia)
        elIndice += 1
        if elIndice == 10 or elIndice == 17:
            elIndice += 1
    print(elGrafo.edges())


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

__Creators__ = 'Joshua Campos and Erick Cobo'


@app.route('/', methods=['GET', 'POST'])
def index():
    return '<h1>Index Page</h1>'


@app.route('/api/draw-map/')
def node_mapping():
    # nodes = printNodes()
    edges = printEdges()
    degree = printNodeDegree()
    drawGraph("Erick Fernando Cobo")
    resp = json.dumps(edges)

    return Response(resp, status=200)


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
