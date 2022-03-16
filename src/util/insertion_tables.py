from random import *
from .connection import open_connection, close_connection_and_cursor

import datetime

LETTRES = 'abcdefghijklmnopqrstuvwxyz'

LOREM_IPSUM = ["Pellentesque diam volutpat commodo sed egestas egestas fringilla. Nulla pellentesque dignissim enim " \
               "sit amet venenatis. Est pellentesque elit ullamcorper dignissim cras tincidunt lobortis.",
               "Lorem ipsum dolor sit amet, consectetur adipiscing elit sed do eiusmod tempor incididunt ut labore " \
               "et dolore magna aliqua. Semper viverra nam libero justo laoreet sit amet. Pretium quam vulputate " \
               "dignissim suspendisse in est ante in nibh.", "Venenatis urna cursus eget nunc " \
               "scelerisque viverra. Nulla pharetra diam sit amet. Congue mauris rhoncus aenean vel elit."]

NOMS_FAMILLE = ["Gagnon", "Roy", "Côté", "Bouchard", "Gauthier", "Morin", "Lavoie", "Fortin", "Gagné", "Ouellet", "Pelletier", "Bélanger",
                "Lévesque", "Bergeron", "Leblanc", "Paquette", "Simard", "Boucher", "Beaulieu", "Poirier", "Martin", "Grenier"]

PRENOMS = ["Jacob", "Zoé", "Victoria", "Barth", "Béatrice", "Liam", "Thomas", "Sophia", "Nathan", "Léo", "Charlie", "Florence", "Édouard", "Félix", "Charlotte", "Amélie", "Amélia", "Noah", "Justine", "Juliette", "Olivia"]

STATUT_LIVREUR = ["occupé", "attente"]

ADRESSES = ["rue Pelletier", "rue Moineau", "avenue Pan", "rue Grenier", "rue Bosse", "avenue Chico", "rue Desbiens", "rue Chocolat", "rue Abricot", "rue Pomme", "rue Sirup", "rue Toit", "rue Orange", "rue Verte", "rue Rouge"]

CATEGORIES = ["Animaux", "Chasse", "Pêche", "Fruit", "Légume", "Liquides", "Randonnées", "Travail", "Bottes", "Marche", "Vêtements"]

def insert_donnees():
    conn, cursor = open_connection()

    insert_categories(conn, cursor)
    insert_clients(conn, cursor)

    close_connection_and_cursor(conn, cursor)

def insert_categories(conn, cursor):
    requete = "INSERT INTO Categorie(nom, description) VALUES('{0}', '{1}')"

    try:
        for i in range(1, len(CATEGORIES)):
            cursor.execute(requete.format(
                CATEGORIES[randint(0, len(CATEGORIES) - 1)],
                LOREM_IPSUM[randint(0, len(LOREM_IPSUM) - 1)],
            ))
    except Exception as e:
        print(e)

def insert_clients(conn, cursor):
    requete = "INSERT INTO Client(telephone, courriel, adresse, nom) VALUES('{0}', '{1}', '{2}', '{3}')"

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
                PRENOMS[randint(0, len(PRENOMS) - 1)] + ' ' + NOMS_FAMILLE[randint(0, len(NOMS_FAMILLE) - 1)]
            ))
    except Exception as e:
        print(e)