from flask import Flask, render_template, jsonify, request, Response, redirect
from util import connection as bd
from util import insertion_tables as insertion
import re

app = Flask(__name__)
global data
data = {"message": {}, "commandesClient": (), "panier": [], "user": {"connecte": False, "nom_famille": "", "prenom": "", id: None}}

def resetData():
    data["user"]["connecte"] = False
    data["user"]["nom_famille"] = ""
    data["user"]["prenom"] = ""
    data["user"]["id"] = None
    data["message"] = {}
    data["commandesClient"] = ()
    data["panier"] = []

@app.before_request
def before_request_callback():
    data["message"]["erreur"] = None
    data["message"]["succes"] = None

@app.route('/inscription', methods=['GET'])
def inscription():
    return render_template("inscription.html", data=data)

@app.route('/inscription', methods=['POST'])
def signup():
    emailPattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'

    courriel = request.form.get("courriel")
    prenom = request.form.get("prenom")
    nom_de_famille = request.form.get("nom_de_famille")
    mot_de_passe = request.form.get("mot_de_passe")
    telephone = request.form.get("telephone")

    if not re.fullmatch(emailPattern, courriel):
        data["message"]["erreur"] = "Le courriel entré est invalide."
    elif len(prenom) == 0:
        data["message"]["erreur"] = "Le prénom fourni ne peut être vide."
    elif not re.match(r'[a-zA-Z\s\-]+$', prenom):
        data["message"]["erreur"] = "Le prénom fourni ne peut contenir de chiffres."
    elif not re.match(r'[a-zA-Z\s\-]+$', nom_de_famille):
        data["message"]["erreur"] = "Le nom fourni ne peut contenir de chiffres."
    elif len(nom_de_famille) == 0:
        data["message"]["erreur"] = "Le nom fourni ne peut être vide."
    elif len(mot_de_passe) < 6:
        data["message"]["erreur"] = "Votre mot de passe doit contenir un minimum de 7 caractères."
    elif not re.match(r'[0-9\-]+$', telephone):
        data["message"]["erreur"] = "Le numéro de téléphone doit avoir le format: 123-456-7890"

    if data["message"]["erreur"] is not None:
        return render_template("inscription.html", data=data)

    return redirect("/")


@app.route("/", methods=['GET'])
def index():
    return render_template("index.html", data=data)


@app.route("/se-connecter", methods=["GET"])
def se_connecter():
    return render_template("se-connecter.html", data=data)


@app.route("/se-connecter", methods=["POST"])
def connexion():
    courriel = request.form.get("courriel")
    mot_de_passe = request.form.get("mot-de-passe")

    data["user"]["connecte"] = True
    data["user"]["nom_famille"] = "Skywalker"
    data["user"]["prenom"] = "Anakin"
    data["user"]["id"] = 1

    return render_template("se-connecter.html", data=data)


@app.route('/deconnexion', methods=['POST'])
def deconnexion():
    resetData()

    return redirect("/")

@app.route('/mon-compte', methods=['GET'])
def mes_souhaits():

    # si le user est pas logged in, redirect: /
    if not data["user"]["connecte"]:
        return redirect("/")

    requeteGetTousCommandes = "SELECT P.nom, C.prix as 'prix_total', C.date_commande, C.date_livraison, C.recu, C.quantite, P.image FROM Produit P INNER JOIN Commander C on P.id = C.produit_id WHERE C.client_id = {0};"

    try:
        commandes = bd.execute_commande_bd(requeteGetTousCommandes.format(data["user"]["id"]), False)
        data["commandesClient"] = commandes
        data["nombreCommandes"] = len(commandes)
    except Exception as e:
        data["erreur"] = "Impossible d'obtenir les données de la base de données."

    return render_template("mon-compte.html", data=data)

if __name__ == '__main__':
    global conn
    global cursor

    # Rouler la commande "mysql -u root -p < scripts/creation_bd.sql" avant de lancer ce fichier.
    bd.execute_file("scripts/creation_table.sql")
    insertion.insert_donnees()

    # Insertion des produits de la base de données
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

    conn, cursor = bd.open_connection()
    app.run(use_reloader=True, debug=True)
