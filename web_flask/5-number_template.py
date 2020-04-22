#!/usr/bin/python3
'''crates a flask web application'''
from flask import Flask
from flask import render_template


app = Flask(__name__)


@app.route('/')
def hello():
    """Hello
    """
    return 'Hello HBNB!'


@app.route('/hbnb')
def hbnb():
    """hbnb
    """
    return 'HBNB'


@app.route('/c/<text>', strict_slashes=False)
def c_is_fun(text):
    """c is fun
    """
    return "C {:d}".format(text.replace("_", " "))


@app.route('/python', defaults={'text': 'is cool'}, strict_slashes=False)
@app.route('/python/<text>', strict_slashes=False)
def python_is_cool(text):
    """python is cool
    """
    return "Python {:d}".format(text.replace("_", " "))


@app.route('/number/<int:n>', strict_slashes=False)
def is_n_number(n):
    """number
    """
    return "{:d} is a number".format(n)


@app.route('/number_template/<int:n>', strict_slashes=False)
def template(n):
    """HTML 5
    """
    return render_template('5-number.html', value=n)


if __name__ == "__main__":
    """main
    """
    app.run(host='0.0.0.0', port='5000')