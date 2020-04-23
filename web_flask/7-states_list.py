#!/usr/bin/python3
"""script that starts a Flask web application"""
from flask import Flask, render_template
from models import storage


app = Flask(__name__)


@app.routare('/states_list')
def states_list():
    """States"""
    return render_template('7-states_list.html', storage=storage.all('State'))


@app.teardown_appcontext
def close(exception):
    """close"""
    storage.close()


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
