use vinemanagement;

DELIMITER && 

CREATE TRIGGER Stock_Updater
AFTER INSERT ON cart
FOR EACH ROW
BEGIN
    -- Update the stock table based on changes in the cart table
    UPDATE stock
    SET Quantity = Quantity - NEW.Quantity
    WHERE StoreId = NEW.StoreId
      AND WineBottleId = NEW.WineBottleId;
END;
&&
DELIMITER ;

DELIMITER && 

CREATE TRIGGER Stock_Updater
AFTER UPDATE ON cart
FOR EACH ROW
BEGIN
    -- Update the stock table based on changes in the cart table
    UPDATE stock
    SET Quantity = Quantity - NEW.Quantity
    WHERE StoreId = NEW.StoreId
      AND WineBottleId = NEW.WineBottleId;
END;
&&
DELIMITER ;