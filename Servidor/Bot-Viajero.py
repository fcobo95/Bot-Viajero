import networkx as nx

from flask import Flask

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
    return '<h1>Index Page</h1>'


if __name__ == '__main__':
    app.run(debug=True, port=5000, host="0.0.0.0")
