CREATE TABLE IF NOT EXISTS Clients (
    id        INTEGER AUTO_INCREMENT PRIMARY KEY,
    telephone CHAR(10)      NOT NULL,
    courriel  VARCHAR(100)  NOT NULL UNIQUE,
    adresse   VARCHAR(100)  NOT NULL,
    nom       VARCHAR(100)  NOT NULL
);

CREATE TABLE IF NOT EXISTS Mot_de_passe (
    id           INTEGER      PRIMARY KEY,
    mot_de_passe VARCHAR(100) NOT NULL,
      CONSTRAINT FK_client_id_motpasse FOREIGN KEY (id) REFERENCES Clients (id)
);

CREATE TABLE IF NOT EXISTS Categorie (
    id          INTEGER PRIMARY KEY,
    description VARCHAR(200),
    nom         VARCHAR(100)
);

CREATE TABLE IF NOT EXISTS Produits (
    id           INTEGER      PRIMARY KEY,
    categorie_id INTEGER,
    nom          VARCHAR(100) NOT NULL UNIQUE,
    prix         INTEGER      NOT NULL,
    poids        INTEGER      NOT NULL,
      CONSTRAINT FK_categorie_id FOREIGN KEY (categorie_id) REFERENCES Categorie (id)
);

CREATE TABLE IF NOT EXISTS Souhaiter (
    client_id  INTEGER NOT NULL,
    produit_id INTEGER NOT NULL,
      PRIMARY KEY (client_id, produit_id),
      CONSTRAINT FK_client_id_souhait FOREIGN KEY (client_id) REFERENCES Clients (id),
      CONSTRAINT FK_produit_id_souhait FOREIGN KEY (produit_id) REFERENCES Produits (id)
);

CREATE TABLE IF NOT EXISTS Livreur (
      id     INTEGER PRIMARY KEY,
      statut ENUM('occupe', 'attente'),
      nom    VARCHAR(100)
);

CREATE TABLE IF NOT EXISTS Commander (
      id             INTEGER PRIMARY KEY AUTO
      produit_id     INTEGER NOT NULL,
      client_id      INTEGER NOT NULL,
      livreur_id     INTEGER NOT NULL,
      prix           INTEGER NOT NULL,
      date_commande  DATE NOT NULL,
      date_livraison DATE NOT NULL,
        PRIMARY KEY (id, produit_id, client_id),
        CONSTRAINT FK_client_id_commande FOREIGN KEY (client_id) REFERENCES Clients (id),
        CONSTRAINT FK_produit_id_commande FOREIGN KEY (produit_id) REFERENCES Produits (id)
)