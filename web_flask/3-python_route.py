#!/usr/bin/python3
'''crates a flask web application'''
from flask import Flask

app = Flask(__name__)
app.url_map.strict_slashes = False


@app.route('/')
def hello():
    """Hello"""
    return 'Hello HBNB!'


@app.route('/hbnb')
def hbnb():
    """hbnb"""
    return 'HBNB'


@app.route('/c/<text>', strict_slashes=False)
def c_is_fun(text):
    """c is fun"""
    return 'C %s' % text


@app.route('/python', defaults={'text': 'is cool'}, strict_slashes=False)
@app.route('/python/<text>', strict_slashes=False)
def python_is_cool(text):
    """python is cool"""
    return 'Python %s' % text.replace("_", " ")


if __name__ == "__main__":
    app.run(host='0.0.0.0', port='5000')
