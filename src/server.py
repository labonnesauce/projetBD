from flask import Flask, render_template, jsonify, request, Response
from util import connection as bd
from util import insertion_tables as insertion

app = Flask(__name__)
data = {"user": {"connecte": True, "nom_famille": "Doe", "prenom": "John"}}

@app.route("/", methods=['GET'])
def index():
    data["erreur"] = None
    requeteGetTousProduits = "SELECT P.id, P.nom, P.prix, P.poids, P.description, P.image, C.nom as Catégorie from Produit P, Categorie C WHERE P.categorie_id = C.id ORDER BY P.nom"
    requeteGetTousCategories = "SELECT C.nom FROM Categorie C"

    try:
        produits = bd.execute_commande_bd(requeteGetTousProduits, False)
        data["tousProduits"] = produits

        categories = bd.execute_commande_bd(requeteGetTousCategories, False)
        data["categories"] = categories

        bd.close_connection_and_cursor()

    except Exception as e:
        data["erreur"] = "Impossible d'obtenir les données de la base de données."

    return render_template("index.html", data=data)

if __name__ == '__main__':
    global conn
    global cursor

    # Rouler la commande "mysql -u root -p < scripts/creation_bd.sql" avant de lancer ce fichier.
    bd.execute_file("scripts/creation_table.sql")
    insertion.insert_donnees()

    conn, cursor = bd.open_connection()
    app.run(use_reloader=True, debug=True)