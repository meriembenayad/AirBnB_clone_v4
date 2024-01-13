#!/usr/bin/python3
""" List of states """
from flask import Flask, render_template
from models import storage

app = Flask(__name__)


@app.route('/states_list', strict_slashes=False)
def displayStates():
    """ Display states list """
    states = storage.all('State').values()
    return render_template('7-states_list.html', states=states)


@app.teardown_appcontext
def tearDown(exception=None):
    """ close DB """
    storage.close()


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
