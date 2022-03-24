from random import *
from .connection import open_connection, close_connection_and_cursor
from datetime import date, timedelta

import datetime

LETTRES = 'abcdefghijklmnopqrstuvwxyz'

LOREM_IPSUM = ["Pellentesque diam volutpat commodo sed egestas egestas fringilla Nulla pellentesque dignissim enim " \
               "sitas amet venenatis Est pellentesque elit ullamcorper dignissim cras tincidunt loborti",
               "Lorem ipsum dolor sitds amet consectetur adipiscing elitee sedwe doweq eiusmod tempor incididunt utilis labore " \
               "etasd dolore magna aliqua. Semper viverra nam libero justo laoreet sit amet Pretium quam vulputate " \
               "dignissim suspendisse inwes este ante ineed nibh", "Venenatis urna cursus eget nuncf " \
               "scelerisque viverra Nulla pharetra diam sital amet Congue mauris rhoncus aenean vel elit",
               "Donec non quam enim Sed consectetur tellus non odio posuere iaculis Class aptent taciti sociosqu Also litora torquent per conubia nostra per inceptos himenaeos",
               "Phasellus eu sapien eu augue gravida fermentum porta non ex Mauris nec rhoncus leoriegh Maecenas auctor tellus in urna malesuada aasdo posuere estssee iaculis", "Utsios enim ad minima veniam, quiss nostrum exercitationem ullam corporis suscipit laboriosam, nisi utasde aliquid exdd eaer commodi consequatur Quis autem velour eumum iure reprehenderit quiquon iner earon voluptate velit esse quam nihil molestiae consequatur, velon illum quiquon dolorem eumee fugiat quo voluptas nulla pariatur?"]

NOMS_FAMILLE = ["Gagnon", "Roy", "Côté", "Bouchard", "Gauthier", "Morin", "Lavoie", "Fortin", "Gagné", "Ouellet", "Pelletier", "Bélanger",
                "Lévesque", "Bergeron", "Leblanc", "Paquette", "Simard", "Boucher", "Beaulieu", "Poirier", "Martin", "Grenier"]

PRENOMS = ["Jacob", "Zoé", "Victoria", "Barth", "Béatrice", "Liam", "Thomas", "Sophia", "Nathan", "Léo", "Charlie", "Florence", "Édouard", "Félix", "Charlotte", "Amélie", "Amélia", "Noah", "Justine", "Juliette", "Olivia"]

STATUT_LIVREUR = ["occupé", "attente"]

ADRESSES = ["rue Pelletier", "rue Moineau", "avenue Pan", "rue Grenier", "rue Bosse", "avenue Chico", "rue Desbiens", "rue Chocolat", "rue Abricot", "rue Pomme", "rue Sirup", "rue Toit", "rue Orange", "rue Verte", "rue Rouge"]

CATEGORIES = ["Animaux", "Chasse", "Pêche", "Fruit", "Légume", "Liquide", "Randonnées", "Travail", "Bottes", "Marche", "Vêtements"]

def insert_donnees():
    conn, cursor = open_connection()

    insert_categories(cursor)
    insert_clients(cursor)
    insert_produits(cursor)
    insert_livreurs(cursor)
    insert_commandes(cursor)
    insert_souhaiter(cursor)

    close_connection_and_cursor(conn, cursor)

def insert_categories(cursor):
    requete = "INSERT INTO Categorie(nom, description) VALUES('{0}', '{1}')"

    try:
        for i in range(1, len(CATEGORIES)+1):
            cursor.execute(requete.format(
                CATEGORIES[i-1],
                LOREM_IPSUM[randint(0, len(LOREM_IPSUM) - 1)],
            ))
    except Exception as e:
        print(e)

def insert_clients(cursor):
    requete = "INSERT INTO Client(telephone, courriel, adresse, nom_famille, prenom) VALUES('{0}', '{1}', '{2}', '{3}', '{4}')"

    COURRIELS = set()
    for i in range(1, 101):
        COURRIELS.add(''.join(LETTRES[randint(0, len(LETTRES)-1)] for x in range(15)) + '@ulaval.ca')
    COURRIELS = [*COURRIELS]

    try:
        for i in range(1, 101):
            cursor.execute(requete.format(
                str(randint(1111111111, 9999999999)),
                COURRIELS[i-1],
                str(randint(1,10000)) + ' ' + ADRESSES[randint(0, len(ADRESSES) - 1)],
                PRENOMS[randint(0, len(PRENOMS) - 1)],
                NOMS_FAMILLE[randint(0, len(NOMS_FAMILLE) - 1)]
            ))
    except Exception as e:
        print(e)

def insert_mots_de_passe(cursor):
    # do nothing for now
    cursor = cursor

def insert_produits(cursor):
    requete = "INSERT INTO Produit(categorie_id, nom, prix, poids, description, image) VALUES({0}, '{1}', {2}, {3}, '{4}', '{5}')"

    NOMS = set()
    while len(NOMS) != 100:
        randomNom = LOREM_IPSUM[randint(1, len(LOREM_IPSUM) - 1)].split(" ")
        NOMS.add(randomNom[randint(1, len(randomNom)-1)].capitalize())
    NOMS = [*NOMS]

    try:
        for i in range(1, 101):
            categorie_id = randint(1, len(CATEGORIES))

            cursor.execute(requete.format(
                categorie_id,
                NOMS[i-1],
                uniform(5.0, 150.0),
                randint(3,20),
                LOREM_IPSUM[randint(0, len(LOREM_IPSUM) - 1)],
                getRandomImage(cursor, categorie_id)
            ))

    except Exception as e:
        print(e)

def insert_livreurs(cursor):
    requete = "INSERT INTO Livreur(statut, nom) VALUES('{0}', '{1}')"

    try:
        for i in range(1, 21):
            cursor.execute(requete.format(
                STATUT_LIVREUR[randint(0, 1)],
                PRENOMS[randint(0, len(PRENOMS) - 1)] + ' ' + NOMS_FAMILLE[randint(0, len(NOMS_FAMILLE) - 1)]
            ))

    except Exception as e:
        print(e)

def insert_commandes(cursor):
    requete = "INSERT INTO Commander(produit_id, client_id, livreur_id, quantite, prix, date_commande, date_livraison, recu) VALUES({0}, {1}, {2}, {3}, {4}, '{5}', '{6}', {7})"
    # requeteLivreurs = "SELECT L.id FROM Livreur L WHERE COUNT(*) = (SELECT COUNT(*) FROM Commander C WHERE C.livreur_id = L.id AND C.recu = 0) ORDER BY RAND() LIMIT 1;"
    requeteProduits = "SELECT P.prix FROM Produit P WHERE P.id = {0}"

    for i in range(1, 101):
        # cursor.execute(requeteLivreurs)
        # valeurLivreur = cursor.fetchone();
        # livreurValide = valeurLivreur[0]

        produit_id = randint(1, 100)
        quantite = randint(1, 10)

        cursor.execute(requeteProduits.format(
            produit_id
        ))
        prix_individuel = cursor.fetchone()[0]

        start_dt = date.today().replace(day=1, month=1).toordinal()
        end_dt = date.today().toordinal()
        random_date_start = date.fromordinal(randint(start_dt, end_dt))
        random_date_end = random_date_start + timedelta(days = randint(2,7))

        cursor.execute(requete.format(
            produit_id,
            randint(1, 100),
            randint(1, 20),
            quantite,
            quantite * prix_individuel * 1.15 + 10,
            random_date_start,
            random_date_end,
            randint(0,1)
        ))

def insert_souhaiter(cursor):
    requete = "INSERT INTO Souhaiter(client_id, produit_id) VALUES({0}, {1})"

    SOUHAITS = set()
    while len(SOUHAITS) != 200:
        randomClient = randint(1, 100)
        randomProduit = randrange(1, 100)
        SOUHAITS.add((randomClient, randomProduit))

    try:
        for client, produit in SOUHAITS:
            cursor.execute(requete.format(
                client,
                produit
            ))

    except Exception as e:
        print(e)


def getRandomImage(cursor, categorie_id):
    requete = "SELECT C.nom FROM Categorie C WHERE {0} = C.id"

    try:
        cursor.execute(requete.format(
            categorie_id
        ))

        categorie = cursor.fetchone()[0]

    except Exception as e:
        print(e)

    categorie = categorie.lower()

    if categorie == "pêche":
        categorie = "peche"
    elif (categorie == "randonnées"):
        categorie = "randonnees"
    elif categorie == "vêtements":
        categorie = "vetements"
    elif categorie == "légume":
        categorie = "legume"

    return "../static/public/images/" + categorie + str(randint(1, 3)) + ".jpg"