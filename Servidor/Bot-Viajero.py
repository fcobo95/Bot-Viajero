import socket

from flask import Flask

app = Flask(__name__)


@app.route('/')
def index():
    return '<h1>Index Page</h1>'


host_name = socket.gethostname()
ipNumber = socket.gethostbyname(host_name)
if __name__ == '__main__':
    app.run(debug=True, port=5000, host=ipNumber)
