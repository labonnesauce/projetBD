import base64
import hashlib

from cryptography.fernet import Fernet
from flask import Flask, render_template, jsonify, request, Response, redirect
from util import connection as bd
from util import insertion_tables as insertion
import re

app = Flask(__name__)
global data
data = {"message": {"erreur": {"active": False, "value": None}, "succes": {"active": False, "value": None}},
        "commandesClient": (), "panier": [], "user": {"connecte": False, "nom_famille": "", "prenom": "", id: None}}


def setMessage(active, type, value):
    data["message"][type] = {"active": active, "value": value}


def resetData():
    data["message"] = {"erreur": {"active": False, "value": None}, "succes": {"active": False, "value": None}}
    data["commandesClient"] = ()
    data["panier"] = []
    data["user"] = {"connecte": False, "nom_famille": "", "prenom": "", id: None}


@app.before_request
def before_request_callback():
    data["message"]["erreur"] = {"active": False, "value": None}
    data["message"]["succes"] = {"active": False, "value": None}


@app.route('/inscription', methods=['GET'])
def inscription():
    return render_template("inscription.html", data=data)

@app.route('/mon-panier', methods=['GET'])
def mon_panier():
    return render_template("mon-panier.html", data=data)


@app.route('/inscription', methods=['POST'])
def signup():
    emailPattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'

    courriel = request.form.get("courriel")
    prenom = request.form.get("prenom")
    nom_de_famille = request.form.get("nom_de_famille")
    mot_de_passe = request.form.get("mot_de_passe")
    telephone = request.form.get("telephone")

    if not re.fullmatch(emailPattern, courriel):
        setMessage(True, "erreur", "Le courriel entré est invalide.");
    elif len(prenom) == 0:
        setMessage(True, "erreur", "Le prénom fourni ne peut être vide.");
    elif not re.match(r'[a-zA-Z\s\-]+$', prenom):
        setMessage(True, "erreur", "Le prénom fourni ne peut contenir de chiffres.");
    elif not re.match(r'[a-zA-Z\s\-]+$', nom_de_famille):
        setMessage(True, "erreur", "Le nom fourni ne peut contenir de chiffres.");
    elif len(nom_de_famille) == 0:
        setMessage(True, "erreur", "Le nom fourni ne peut être vide.");
    elif len(mot_de_passe) < 6:
        setMessage(True, "erreur", "Votre mot de passe doit contenir un minimum de 7 caractères.");
    elif not re.match('[0-9]{10}', telephone):
        setMessage(True, "erreur", "Le numéro de téléphone doit avoir le format: 1234567890");

    if data["message"]["erreur"]["active"]:
        return render_template("inscription.html", data=data)

    requeteNouvelUtil = "INSERT INTO Client(telephone, courriel, adresse, nom_famille, prenom) VALUES('{0}', '{1}', null, '{2}', '{3}');"

    # Si les informations sont OK, on crée le user dans la DB
    # Si le courriel est déjà utilisé, une exception est lancée
    try:
        bd.execute_sans_resultat(requeteNouvelUtil.format(
            telephone,
            courriel,
            nom_de_famille,
            prenom
        ))
    except Exception as err:
        setMessage(True, "erreur", err)
        return render_template("inscription.html", data=data)

    requeteMotDePasse = "INSERT INTO MotDePasse (client_id, mot_de_passe) VALUES ({0}, '{1}');"
    requeteGetLastUser = "SELECT C.id FROM Client C ORDER BY C.id DESC LIMIT 1;"

    # Si les informations sont OK et le nouveau user a été créé, on insère son mot de passe
    try:
        id_user = bd.execute_commande_bd(requeteGetLastUser, fetchOne=True)[0]

        hash_bd = hashlib.sha256(mot_de_passe.encode('utf-8')).hexdigest()
        bd.execute_sans_resultat(requeteMotDePasse.format(
            id_user,
            hash_bd
        ))

    except Exception as err:
        setMessage(True, "erreur", "Une exception est survenue.")
        return render_template("inscription.html", data=data)

    data["user"] = {"connecte": True, "nom_famille": nom_de_famille, "prenom": prenom, id: id_user}
    setMessage(True, "succes", "Compte créé avec succès. Bon magasinage!")

    return render_template("index.html", data=data)


@app.route("/", methods=['GET'])
def index():
    return render_template("index.html", data=data)


@app.route("/se-connecter", methods=["GET"])
def se_connecter():
    return render_template("se-connecter.html", data=data)


@app.route("/ajout-panier", methods=["POST"])
def ajout_panier():
    produit_id = request.form.get("produit-id")

    requeteGetProduit = "SELECT P.id, P.nom, P.prix, P.poids, P.description, P.image, C.nom as Catégorie from Produit P, Categorie C WHERE P.id = {0}"
    produit = bd.execute_commande_bd(requeteGetProduit.format(produit_id), True)
    print(data["panier"])
    data["panier"].append(produit)
    setMessage(True, "succes", "Le produit " + produit_id + " a été ajouté à votre panier.")

    return render_template("index.html", data=data)


@app.route("/ajout-souhait", methods=["POST"])
def ajout_souhait():
    produit = request.form.get("produit-id")
    return redirect("/")


@app.route("/se-connecter", methods=["POST"])
def connexion():
    courriel = request.form.get("courriel")
    mot_de_passe = request.form.get("mot-de-passe")

    requeteCourriel = "SELECT * FROM Client C WHERE C.courriel = '{0}'"
    requeteMotDePasse = "SELECT M.mot_de_passe FROM MotDePasse M WHERE M.client_id = {0}"

    if courriel is None:
        setMessage(True, "erreur", "Le courriel est vide.")
        return render_template("se-connecter.html", data=data)

    if mot_de_passe is None:
        setMessage(True, "erreur", "Veuillez entrer un mot de passe.")
        return render_template("se-connecter.html", data=data)

    user = bd.execute_commande_bd(requeteCourriel.format(
        courriel
    ), fetchOne=True)

    if user is None:
        setMessage(True, "erreur", "Le courriel ne correspond à aucun utilisateur.")
        return render_template("se-connecter.html", data=data)

    user_id = user[0]

    try:
        hash_bd = bd.execute_commande_bd(requeteMotDePasse.format(
            user_id
        ), True)

        if hash_bd[0] == hashlib.sha256(mot_de_passe.encode("utf-8")).hexdigest().encode():
            setMessage(True, "succes", "Bonjour, " + user[5] + "!")
            data["user"] = {"connecte": True, "nom_famille": user[4], "prenom": user[5], id: user[0]}
            return render_template("se-connecter.html", data=data)
        else:
            setMessage(True, "erreur", "Le mot de passe est invalide.")
            return render_template("se-connecter.html", data=data)

    except Exception as err:
        setMessage(True, "erreur", "Une erreur est survenue.")
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

    bd.execute_sans_resultat("INSERT INTO Client (telephone, courriel, adresse, nom_famille, prenom) VALUES ('1111111111', 'jo@u.ca', null, 'Bessette', 'Jonathan')")
    mot_passe = hashlib.sha256('123princesse'.encode('utf-8')).hexdigest()
    bd.execute_sans_resultat("INSERT INTO MotDePasse (client_id, mot_de_passe) VALUES (101, '{0}')".format(mot_passe))

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
