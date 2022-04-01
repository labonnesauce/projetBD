USE projet_glo2005;

DROP FUNCTION IF EXISTS CalculPrixTotal;
DROP TRIGGER IF EXISTS AssignationLivreur;
DROP TRIGGER IF EXISTS CourrielDejaPresent;

DELIMITER //
CREATE FUNCTION CalculPrixTotal(produit_id INT(20), quantite INT(20)) RETURNS FLOAT(10,2) DETERMINISTIC
BEGIN
        DECLARE prix_unitaire FLOAT(10,2);
        DECLARE total FLOAT(10,2);

        SELECT P.prix into prix_unitaire FROM Produit P WHERE P.id = produit_id;
        SET total = prix_unitaire * quantite * 1.15 + 10;
        RETURN total;
END //
DELIMITER ;

DELIMITER //
CREATE TRIGGER AssignationLivreur
    BEFORE INSERT ON Commander
    FOR EACH ROW
    BEGIN
        IF (SELECT COUNT(*) FROM Livreur L WHERE L.statut = 'attente') = 0
        THEN
            SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT = "Aucun livreur n'est disponible en ce moment";
        END IF;
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