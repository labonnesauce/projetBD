USE projet_glo2005;

DROP FUNCTION IF EXISTS CalculPrixTotal;
DROP TRIGGER IF EXISTS AssignationLivreur;
DROP TRIGGER IF EXISTS CourrielDejaPresent;

DELIMITER //
CREATE FUNCTION CalculPrixTotal(produit_id INTEGER, quantite INTEGER) RETURNS FLOAT DETERMINISTIC
    BEGIN
        DECLARE prix_unitaire FLOAT;
        DECLARE total FLOAT;

        SELECT P.prix into prix_unitaire FROM Produit P WHERE P.id = produit_id;
        SET total = prix_unitaire * quantite * 1.15 + 3;
        RETURN total;
    END //
DELIMITER ;

DELIMITER //
CREATE FUNCTION LivreurAvecMoinsCommande() RETURNS INTEGER DETERMINISTIC
    BEGIN
        DECLARE idLivreur INTEGER;
        IF (SELECT COUNT(*) FROM Livreur L WHERE L.statut = 'attente') = 0
        THEN
            SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT = "Aucun livreur n'est disponible en ce moment";
        ELSE SELECT L.id INTO idLivreur FROM Livreur L WHERE L.statut = 'attente' ORDER BY RAND() LIMIT 1;
        END IF;

        RETURN idLivreur;
    END //
DELIMITER ;

DELIMITER //
CREATE TRIGGER CourrielDejaPresent
    BEFORE INSERT ON Client
    FOR EACH ROW
    BEGIN
        IF (SELECT COUNT(*) FROM Client C WHERE C.courriel = NEW.courriel) = 1
        THEN
            SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT = "Un autre compte utilise ce courriel";
        END IF;
    END //
DELIMITER ;