DROP TABLE IF EXISTS MotDePasse;
DROP TABLE IF EXISTS Souhaiter;
DROP TABLE IF EXISTS Commander;
DROP TABLE IF EXISTS Client;
DROP TABLE IF EXISTS Produit;
DROP TABLE IF EXISTS Categorie;
DROP TABLE IF EXISTS Livreur;

CREATE TABLE IF NOT EXISTS Client (
    id        INT(20)       PRIMARY KEY AUTO_INCREMENT,
    telephone VARCHAR(10)   NOT NULL,
    courriel  VARCHAR(100)  NOT NULL UNIQUE,
    adresse   VARCHAR(100)  NOT NULL,
    nom       VARCHAR(100)  NOT NULL
);

CREATE TABLE IF NOT EXISTS MotDePasse (
    client_id    INT(20)      PRIMARY KEY,
    mot_de_passe VARCHAR(100) NOT NULL,
      CONSTRAINT FK_client_id_motpasse FOREIGN KEY (client_id) REFERENCES Client (id)
);

CREATE TABLE IF NOT EXISTS Categorie (
    id          INT(20)  PRIMARY KEY AUTO_INCREMENT,
    nom         VARCHAR(100),
    description VARCHAR(500)
);

CREATE TABLE IF NOT EXISTS Produit (
    id           INT(20)      PRIMARY KEY AUTO_INCREMENT,
    categorie_id INT(20)      NOT NULL,
    nom          VARCHAR(100) NOT NULL,
    prix         FLOAT(10,2)  NOT NULL,
    poids        INT(20)      NOT NULL,
    description  VARCHAR(500) NOT NULL,
      CONSTRAINT FK_categorie_id FOREIGN KEY (categorie_id) REFERENCES Categorie (id)
);

CREATE TABLE IF NOT EXISTS Souhaiter (
    client_id  INTEGER NOT NULL,
    produit_id INTEGER NOT NULL,
      PRIMARY KEY (client_id, produit_id),
      CONSTRAINT FK_client_id_souhait FOREIGN KEY (client_id) REFERENCES Client (id),
      CONSTRAINT FK_produit_id_souhait FOREIGN KEY (produit_id) REFERENCES Produit (id)
);

CREATE TABLE IF NOT EXISTS Livreur (
      id     INT(20) PRIMARY KEY AUTO_INCREMENT,
      statut ENUM('occupé', 'attente'),
      nom    VARCHAR(100)
);

CREATE TABLE IF NOT EXISTS Commander (
      id             INT(20)      PRIMARY KEY AUTO_INCREMENT,
      produit_id     INT(20)      NOT NULL,
      client_id      INT(20)      NOT NULL,
      livreur_id     INT(20)      NOT NULL,
      prix           FLOAT(10,2)  NOT NULL,
      date_commande  DATE         NOT NULL,
      date_livraison DATE         NOT NULL,
      recu           INT(1)       NOT NULL DEFAULT FALSE,
      quantite       INT(20)      NOT NULL,
        CONSTRAINT FK_client_id_commande FOREIGN KEY (client_id) REFERENCES Client (id),
        CONSTRAINT FK_produit_id_commande FOREIGN KEY (produit_id) REFERENCES Produit (id),
        CONSTRAINT FK_livreur_id_commande FOREIGN KEY (livreur_id) REFERENCES Livreur (id)
);