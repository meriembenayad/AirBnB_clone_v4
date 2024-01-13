#!/usr/bin/python3
""" /python/<text> """
from flask import Flask, render_template
app = Flask(__name__)


@app.route('/', strict_slashes=False)
def hello():
    """ Hello HBNB! """
    return 'Hello HBNB!'


@app.route('/hbnb', strict_slashes=False)
def hbnb():
    """ HBNB """
    return 'HBNB'


@app.route('/c/<text>', strict_slashes=False)
def cText(text):
    """ C <text> """
    return "C {}".format(text.replace("_", " "))


@app.route('/python', strict_slashes=False)
@app.route('/python/<text>', strict_slashes=False)
def pythonText(text="is cool"):
    """ Python <text> """
    return "Python {}".format(text.replace("_", " "))


@app.route('/number/<int:n>', strict_slashes=False)
def numberN(n):
    """ n is a number """
    return f"{n} is a number"


@app.route('/number_template/<int:n>', strict_slashes=False)
def numberTemplate(n):
    """ HTML if n is a number """
    return render_template('5-number.html', n=n)


@app.route('/number_odd_or_even/<int:n>', strict_slashes=False)
def numberOddEven(n):
    """ n is Odd OR Even """
    if n % 2 == 0:
        return render_template('6-number_odd_or_even.html', n=n, result='even')
    else:
        return render_template('6-number_odd_or_even.html', n=n, result='odd')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
