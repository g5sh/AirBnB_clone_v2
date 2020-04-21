#!/usr/bin/python3
"""script that starts a Flask web application"""
from flask import Flask


app = Flask(__name__)


@app.route('/', strict_slashes=False)
def hello():
    return('Hello HBNB!')


@app.route('/hbnb', strict_slashes=False)
def hbnb():
    return('HBNB')


@app.route('/c/<text>')
def c_isfun(text):
    return('C %s' % text.replace("_", " "))


@app.route('/python/(<text>)')
def Python_is_cool(text):
    return('Python %s' % text.replace("_", " "))


if __name__ == "__main__":
    app.run(host='0.0.0.0')
