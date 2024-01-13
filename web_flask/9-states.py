#!/usr/bin/python3
""" Cities by States """
from flask import Flask, render_template
from models import storage

app = Flask(__name__)


@app.route('/states', strict_slashes=False)
def cities_state_db():
    """ cities of state from DBStorage """
    states = storage.all('State').values()
    return render_template('7-states_list.html', states=states)


@app.route('/states/<id>', strict_slashes=False)
def city_states_get(id):
    """ cities of state using getter method cities """
    states = None
    for st in storage.all('State').values():
        if st.id == id:
            states = st
            break
    return render_template('9-states.html', state=states)


@app.teardown_appcontext
def tear_down(exception=None):
    """ close DB """
    storage.close()


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
