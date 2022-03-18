from flask import Flask, render_template, jsonify, request, Response
from util import connection as bd
from util import insertion_tables as insertion

app = Flask(__name__)
model = {}

@app.route("/")
def index():
    cursor.execute("SELECT * FROM Souhaiter LIMIT 1")
    return render_template("index.html", x=cursor.fetchone())


if __name__ == '__main__':
    global conn
    global cursor

    # Rouler la commande "mysql -u root -p < scripts/creation_bd.sql" avant de lancer ce fichier.
    bd.execute_file("scripts/creation_table.sql")
    insertion.insert_donnees()

    conn, cursor = bd.open_connection()
    app.run()