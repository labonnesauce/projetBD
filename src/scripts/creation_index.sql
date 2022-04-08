use projet_glo2005;

CREATE INDEX indexCategorie ON Categorie(id, nom) USING BTREE;

CREATE INDEX indexProduit ON Produit(id, categorie_id) USING BTREE;

CREATE INDEX indexSouhaiter ON Souhaiter(client_id, produit_id) USING BTREE;

CREATE INDEX indexCommander ON Commander(id, produit_id, client_id, livreur_id, prix, date_commande, date_livraison,
                                         quantite) USING BTREE;

CREATE INDEX indexStatutLivreurs ON Livreur(statut) USING BTREE;