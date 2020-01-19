from flask import Flask, render_template, url_for
from Consultas import BaseDatos
import sqlite3

app = Flask(__name__)

@app.route('/')
def index():
    bbdd = BaseDatos()
    informes = bbdd.consultarInformes()
    return render_template('index.html', tasks=informes)

@app.route('/<string:page_name>/')
def render_static(page_name):
    return render_template(page_name + ".html")

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')
