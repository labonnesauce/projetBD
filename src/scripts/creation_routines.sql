DELIMITER //
CREATE FUNCTION
  VisibiliteProduitFiltreParNom(idProduit INT(20), nomProduit VARCHAR(100), filtre VARCHAR(100)) RETURNS INTEGER;
  BEGIN
    DECLARE visible INTEGER;


    IF stock - NEW.quantite < 0
    THEN SET NEW.id_acheteur = NULL;
    ELSE
      UPDATE Vendre V SET V.quantite = V.quantite - NEW.quantite WHERE V.id_biere = NEW.id_biere;
    END IF;
  END//
DELIMITER;