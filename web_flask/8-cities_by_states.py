#!/usr/bin/python3
"""
a script that starts a Flask web application
"""
from flask import Flask
from models import storage
from models.state import State
from models.city import City
from flask import render_template


app = Flask(__name__)

@app.route("/states_list")
def states_list():
    states = []
    data = storage.all(State)
    for key, value in data.items():
        states.append(value)
    return render_template("7-states_list.html", states=states)


@app.route("/cities_by_states", strict_slashes=False)
def cities_by_states():
    states = []
    data = storage.all(State)
    for key, value in data.items():
        states.append(value)

    cities = []
    data = storage.all(City)
    for key, value in data.items():
        cities.append(value)
    return render_template("8-cities_by_states.html", states=states,
                           cities=cities)


@app.teardown_appcontext
def teardown(exc):
    """Remove the current SQLAlchemy session."""
    storage.close()


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
