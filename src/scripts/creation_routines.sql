DELIMITER //
CREATE FUNCTION PrixTotal(produit_id INT(20), quantite INT(20)) RETURNS FLOAT(10,2)
BEGIN
        DECLARE item FLOAT(10,2);
        DECLARE total FLOAT(10,2);

        SELECT P.prix into item FROM Produit P, Commander C WHERE C.id = produit_id;
        SET total = item * quantite * 1.15 + 10;
        RETURN total;
end //
DELIMITER ;


DELIMITER //
CREATE TRIGGER HeureLivraisonInvalide
    BEFORE INSERT ON commander
    FOR EACH ROW
    BEGIN
        IF (SELECT commander.date_livraison FROM commander )< (SELECT commander.date_commande FROM commander)
        THEN
            SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT = "Date de livraison invalide";
        end if;
    end //
DELIMITER ;


DELIMITER //
CREATE TRIGGER AssignationLivreur
    BEFORE INSERT ON commander
    FOR EACH ROW
    BEGIN
        if (SELECT COUNT(*) FROM livreur L WHERE L.statut = 'attente') = 0
        THEN
            SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT = "Aucun livreur n'est disponible en ce moment";
        end if;
    end //
DELIMITER ;