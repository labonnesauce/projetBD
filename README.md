# Projet de base de données - GLO 2005 - 2022

## Installation

Notez que toutes les commandes suivantes s'exécutent à partir du Cmd Prompt, dans le dossier ```src/```.

1. Pour créer la base de données:
> mysql -u root -p < scripts/creation_bd.sql <br />

2. Pour créer les tables, les index et insérer les données:
> server.py --creation <br />

3. Pour créer les routines:
> mysql -u root -p < scripts/creation_routines.sql <br />

4. Pour démarrer le serveur:
> server.py <br />
