# Imports section
import datetime
import networkx as nx
import matplotlib.pyplot as plt

graph = nx.Graph()
from pymongo import MongoClient
from flask import Flask, json, Response, jsonify, render_template

app = Flask(__name__)

__Creators__ = 'Joshua Campos and Erick Cobo'

# Mongo AWS Database connection
uri = "mongodb://ecoboe249:viper1829@ds153609.mlab.com:53609/bootowl"
client = MongoClient(uri)

# Mongo Local Database connection
client = MongoClient('localhost', 35250)


@app.route('/', methods=['GET', 'POST'])
def index():
    return '<h1>Index Page</h1>'


@app.route('/api/draw-map/')
def node_mapping():
    graph.add_nodes_from([1, 24])
    # Vamos a quitar esto de aqui luego, para agregar logica.
    # Esto es solo para tener la lista de relaciones de unos
    # nodos con los otros.

    """
    Mi idea es la siguiente, Joshua.

    Mira, digamos que pasamos las relaciones a formato JSON.

    Entonces,

    nodex = request.json['nodex']
    nodey = request.json['nodey']
    peso = request.json['weight']

    entonces

    for each node in JSONDictionary:
        graph.add_edges_from(nodex, nodey, weight)

    return blablabla


    No se algo asi digo yo hahaha.

    Al metodo de printNodeDegree le puse como parametro node=1, para que por default tenga un valor de algun nodo.
    """
    graph.add_edges_from(
        [
            (1, 3, {'weight': 1.10}),
            (1, 7, {'weight': 3.50}),
            (1, 9, {'weight': 4.50}),
            (1, 16, {'weight': 2.10}),
            (1, 22, {'weight': 3.10}),
            (2, 13, {'weight': 2.40}),
            (2, 14, {'weight': 2.90}),
            (2, 24, {'weight': 9.20}),
            (24, 2, {'weight': 9.20}),
            (3, 16, {'weight': 10}),
            (3, 24, {'weight': 3.45}),
            (4, 9, {'weight': 3.30}),
            (4, 21, {'weight': 14.20}),
            (4, 22, {'weight': 3.95}),
            (4, 23, {'weight': 5.30}),
            (5, 14, {'weight': 4.30}),
            (5, 20, {'weight': 6.40}),
            (6, 8, {'weight': 2}),
            (6, 11, {'weight': 2.60}),
            (6, 19, {'weight': 2.70}),
            (7, 9, {'weight': 2.30}),
            (7, 23, {'weight': 1.70}),
            (8, 16, {'weight': 0.30}),
            (8, 22, {'weight': 1.80}),
            (9, 23, {'weight': 2}),
            (11, 19, {'weight': 13.20}),
            (11, 24, {'weight': 1.30}),
            (12, 15, {'weight': 0.65}),
            (12, 18, {'weight': 3.65}),
            (12, 21, {'weight': 7.40}),
            (12, 23, {'weight': 1.65}),
            (13, 15, {'weight': 2.70}),
            (13, 18, {'weight': 2.10}),
            (14, 18, {'weight': 3}),
            (15, 23, {'weight': 1.50}),
            (18, 20, {'weight': 3.40}),
            (19, 24, {'weight': 4.50}),
            (20, 9, {'weight': 2.15})
        ]
    )
    # nodes = printNodes()
    # edges = printEdges()
    degree = printNodeDegree()
    drawGraph()
    # resp = json.dumps(edges)

    return render_template('../HTML/mainpage.html')  # Response(resp, status=200)


def printNodes():
    nodes = graph.nodes()

    return nodes


def printEdges():
    edges = graph.edges()

    return edges


def printNodeDegree(node=1):
    degree = graph.degree(node)

    return degree


def drawGraph():
    nx.draw(graph)
    plt.savefig("C:\\Users\\Erick Fernando Cobo\\Pictures\\graph.png")
    return plt.show()


if __name__ == '__main__':
    app.run(debug=True, port=5000, host="localhost")
