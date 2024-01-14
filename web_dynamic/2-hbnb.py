#!/usr/bin/python3
""" HBNB is alive """
from flask import Flask, render_template
from models import storage
from uuid import uuid4


app = Flask(__name__)


@app.route('/2-hbnb', strict_slashes=False)
def cities_state_db():
    """ cities of state from DBStorage """
    data = {
        'states': storage.all('State').values(),
        'amenities': storage.all('Amenity').values(),
        'places': storage.all('Place').values()
    }
    cache_id = uuid4()
    return render_template('2-hbnb.html', data=data, cache_id=cache_id)


@app.route('/states/<id>', strict_slashes=False)
def city_states_get(id):
    """ cities of state using getter method cities """
    states = None
    for st in storage.all('State').values():
        if st.id == id:
            states = st
            break
    cache_id = uuid4()
    return render_template('9-states.html', state=states, cache_id=cache_id)


@app.teardown_appcontext
def tear_down(exception=None):
    """ close DB """
    storage.close()


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
