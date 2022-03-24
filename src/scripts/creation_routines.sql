#fonction total commande, je recois id_produit et quantité. prix fix taxes

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