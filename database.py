import mysql.connector
import pandas as pd
from config import HOST, USER, PASSWORD, PORT
import xml.etree.ElementTree as ET

connection = mysql.connector.connect(
    host=HOST,
    user=USER,
    password=PASSWORD,
    port=PORT,
)

cursor = connection.cursor()
cursor.execute("DROP DATABASE IF EXISTS VineManagement")
cursor.execute("CREATE DATABASE IF NOT EXISTS VineManagement")
cursor.execute("USE VineManagement")


def create_tables():
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS C_Customer (
            Name VARCHAR(30),
            Cust_Id int,
            Phone_Number VARCHAR(30),
            Password VARCHAR(30),
            PRIMARY KEY(Cust_Id, Phone_Number)
        )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Store (
        Store_Id int PRIMARY KEY,
        Store_Name VARCHAR(30),
        Phone_Number VARCHAR(30) UNIQUE,
        Email_Id VARCHAR(30) UNIQUE,
        Location VARCHAR(1000),
        Landmark VARCHAR(1000),
        City VARCHAR(1000),
        State VARCHAR(1000)
    )
   ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Stock (
            Store_Id int,
            Wine_Bottle_Id int,
            Quantity int,
            Retailer_Id int,
            PRIMARY KEY (Store_Id,Wine_Bottle_Id,Retailer_Id)
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS N_Stock (
            Store_Id int,
            Wine_Bottle_Id int,
            Quantity int,
            PRIMARY KEY (Store_Id,Wine_Bottle_Id)
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Wine_Bottles (
            Wine_Bottle_Id int,
            Name VARCHAR(30),
            MRP int,
            Type VARCHAR(15),
            Age int,
            ABV VARCHAR(30),
            Demand VARCHAR(30),
            PRIMARY KEY (Wine_Bottle_Id)
        )
    ''')


    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Cart (
            Store_Id int,
            Wine_Bottle_Id int,
            Quantity int,
            PRIMARY KEY (Store_Id,Wine_Bottle_Id)
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Bill (
            Bill int,
            Created_Time VARCHAR(100),
            PRIMARY KEY (Created_Time)
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Manufacturer (
            Man_Id int PRIMARY KEY,
            Name VARCHAR(30),
            Type VARCHAR(30),
            Capacity int,
            Manufacturer_Selling_Price int,
            Phone_Number VARCHAR(30),
            Location VARCHAR(1000)
        )
    ''')

    cursor.execute('''
        ALTER TABLE Stock
        ADD FOREIGN KEY (Store_Id) REFERENCES Store(Store_Id)              
    ''')

def add_data(uploadedFile):
    tree = ET.parse(uploadedFile)
    StoresData = tree.findall('Store')
    CustomersData = tree.findall('C_Customer')
    WineBottleData = tree.findall('winebottle')
    StockData = tree.findall('stock')
    ManufacturerData = tree.findall('manufacturer')

    for store in StoresData:
        store_id = int(store.find('StoreId').text)
        store_name = store.find('StoreName').text
        phone_number = int(store.find('PhoneNumber').text)
        email_id = store.find('EmailId').text
        location = store.find('Location').text
        location_sub=location.split()
        landmark = location_sub[0]
        city = location_sub[1]
        state = location_sub[2]

        # Insert the data into the 'Stores' table
        cursor.execute("INSERT INTO Store (Store_Id, Store_Name, Phone_Number, Email_Id, Location, Landmark, City, State) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",(store_id, store_name, phone_number, email_id, location, landmark, city, state))

    for customer in CustomersData:
        Password = customer.find('Password').text
        name = customer.find('Name').text
        cust_id = int(customer.find('CustId').text)
        phone_number = int(customer.find('PhoneNumber').text)

        # Insert the data into the 'Customers' table
        cursor.execute("INSERT INTO C_Customer (Password, Name, Cust_Id, Phone_Number) VALUES (%s, %s, %s, %s)",(Password, name, cust_id, phone_number))

    for winebottle in WineBottleData:
        wine_bottle_id = int(winebottle.find('WineBottleId').text)
        name = winebottle.find('Name').text
        mrp = float(winebottle.find('MRP').text)
        wine_type = winebottle.find('Type').text
        age = int(winebottle.find('Age').text)
        abv = winebottle.find('ABV').text
        demand = winebottle.find('Demand').text

        # Insert the data into the 'WineBottles' table
        cursor.execute("INSERT INTO Wine_Bottles (Wine_Bottle_Id, Name, MRP, Type, Age, ABV, Demand) VALUES (%s, %s, %s, %s, %s, %s, %s)",(wine_bottle_id, name, mrp, wine_type, age, abv, demand))

    for stock in StockData:
        store_id = int(stock.find('StoreId').text)
        wine_bottle_id = int(stock.find('WineBottleId').text)
        quantity = int(stock.find('Quantity').text)
        retailer_id = int(stock.find('RetailerId').text)

        # Insert the data into the 'Stock' table
        cursor.execute("INSERT INTO Stock (Store_Id, Wine_Bottle_Id, Quantity, Retailer_Id) VALUES (%s, %s, %s, %s)",(store_id, wine_bottle_id, quantity, retailer_id))

    for manufacturer in ManufacturerData:
        man_id = int(manufacturer.find('ManId').text)
        name = manufacturer.find('Name').text
        wine_type = manufacturer.find('Type').text
        capacity = int(manufacturer.find('Capacity').text)
        man_selling_price = float(manufacturer.find('ManufacturerSellingPrice').text)
        phone_number = int(manufacturer.find('PhoneNumber').text)
        location = manufacturer.find('Location').text

        # Insert the data into the 'Manufacturers' table
        cursor.execute("INSERT INTO Manufacturer (Man_Id, Name, Type, Capacity, Manufacturer_Selling_Price, Phone_Number, Location) VALUES (%s, %s, %s, %s, %s, %s, %s)",(man_id, name, wine_type, capacity, man_selling_price, phone_number, location))


    cursor.execute("SELECT Store_ID,WINE_BOTTLE_ID,SUM(Quantity) from STOCK GROUP BY Store_Id, Wine_Bottle_Id")
    result=cursor.fetchall()
    for i in result:
        cursor.execute("INSERT INTO N_Stock (Store_Id, Wine_Bottle_Id, Quantity) VALUES (%s, %s, %s)",(i[0],i[1],i[2]))
    connection.commit()

def view_data():
    cursor.execute("SELECT * from Store")
    StoreData = cursor.fetchall()

    cursor.execute("SELECT * from Wine_Bottles")
    Wine_BottlesData = cursor.fetchall()

    cursor.execute("SELECT * from N_Stock")
    StockData = cursor.fetchall()
    
    cursor.execute("SELECT * from Cart")
    CartData = cursor.fetchall()

    cursor.execute("SELECT * from Bill")
    BillData = cursor.fetchall()

    return StoreData, Wine_BottlesData, StockData, CartData, BillData


def runquery(command):
    cursor.execute(command)
    result=cursor.fetchall()
    return result 


def call_procedure(store,qty,bottle):
    cursor.callproc("update_stock_after_cart_operation", (store,bottle,qty))


def exists_database():
    try:
        cursor.execute("USE VINEMANAGEMENT")
    except:
        return 1
    return 0

def delete_data(cart_id):
    cursor.execute("DROP DATABASE VINEMANAGEMENT")
    cursor.execute("CREATE DATABASE IF NOT EXISTS VineManagement")
    cursor.execute("USE VineManagement")

    connection.commit()


def update_cart(store,bottle,qty):
    if qty>0:

        cursor.execute('Select Quantity from N_STOCK where Store_Id = %s and Wine_Bottle_Id = %s',(store,bottle))
        result=cursor.fetchall()
        if result[0][0]>qty:
            cursor.execute('Select * from Cart where Store_Id = %s and Wine_Bottle_Id=%s', (store,bottle))
            result=cursor.fetchall()
            if result:
                cursor.execute('UPDATE Cart SET Quantity = Quantity+%s WHERE Store_Id = %s and Wine_Bottle_Id= %s', (qty, store,bottle))
                call_procedure(store,qty,bottle)
                #cursor.execute('UPDATE N_STOCK SET Quantity=Quantity-%s Where Store_Id = %s and Wine_Bottle_Id = %s',(qty,store,bottle))
            else:
                cursor.execute('INSERT INTO CART (Store_Id,Wine_Bottle_Id,Quantity) VALUES (%s,%s,%s)',(store,bottle,qty))
                call_procedure(store,qty,bottle)
                #cursor.execute('UPDATE N_STOCK SET Quantity=Quantity-%s Where Store_Id = %s and Wine_Bottle_Id = %s',(qty,store,bottle))
            connection.commit()
            return 1
        else:
            return 0
    else:
        try:
            cursor.execute('Select * from Cart where Store_Id = %s and Wine_Bottle_Id=%s', (store,bottle))
            result=cursor.fetchall()
            row = result[0]
        except:
            return 0
        if row[2]>=-qty:
            cursor.execute('UPDATE Cart SET Quantity = Quantity+%s WHERE Store_Id = %s and Wine_Bottle_Id= %s', (qty, store,bottle))
            #cursor.execute('UPDATE N_STOCK SET Quantity=Quantity-%s Where Store_Id = %s and Wine_Bottle_Id = %s',(qty,store,bottle))
            call_procedure(store,qty,bottle)
            cursor.execute('Select Quantity from Cart where Store_Id = %s and Wine_Bottle_Id=%s', (store,bottle))
            result=cursor.fetchall()
            row1 = result[0][0]
            if row1==0:
                cursor.execute('Delete from Cart WHERE Store_Id = %s and Wine_Bottle_Id= %s', (store,bottle))
            return 1
        else:
            return 0

def runquery(command):
    cursor.execute(command)
    result=cursor.fetchall()
    return result 

def make_bill():
    cursor.execute('Select Cart.Quantity, Wine_Bottles.MRP from Cart INNER JOIN Wine_Bottles on Wine_Bottles.Wine_Bottle_Id=Cart.Wine_Bottle_Id')
    result=cursor.fetchall()
    total_price=0
    for i in result:
        total_price+=(i[0]*i[1])
    return total_price

def procedures():
    cursor.execute('''
        DROP PROCEDURE IF EXISTS update_stock_after_cart_operation
    ''')
    cursor.execute('''
        CREATE PROCEDURE update_stock_after_cart_operation(IN store_id INT, IN wine_bottle_id INT, IN quantity_change INT)
        BEGIN
            -- Update the stock table based on changes in the cart table
            UPDATE N_stock
            SET Quantity = Quantity - quantity_change
            WHERE Store_Id = store_id
            AND Wine_Bottle_Id = wine_bottle_id;
        END;
    ''')


def triggers():
    cursor.execute('''
        DROP TRIGGER IF EXISTS generate_bill_insert
   ''')
    cursor.execute('''
        CREATE TRIGGER generate_bill_insert
        AFTER INSERT ON cart
        FOR EACH ROW
        BEGIN
            DECLARE total_amount INT;
            
            -- Calculate total amount by multiplying quantity and MRP
            SELECT SUM(c.Quantity * wb.MRP)
            INTO total_amount
            FROM cart c
            INNER JOIN wine_bottles wb ON c.Wine_Bottle_Id = wb.Wine_Bottle_Id;
            
            -- Insert the bill into the 'bill' table
            DELETE FROM BILL;
            INSERT INTO bill (Bill, Created_Time)
            VALUES (total_amount, NOW());
        END;
    ''')
    
    cursor.execute('''
        DROP TRIGGER IF EXISTS generate_bill_update
   ''')
    cursor.execute('''
        CREATE TRIGGER generate_bill_update
        AFTER UPDATE ON cart
        FOR EACH ROW
        BEGIN
            DECLARE total_amount INT;
            
            -- Calculate total amount by multiplying quantity and MRP
            SELECT SUM(c.Quantity * wb.MRP)
            INTO total_amount
            FROM cart c
            INNER JOIN wine_bottles wb ON c.Wine_Bottle_Id = wb.Wine_Bottle_Id;
            
            -- Insert the bill into the 'bill' table
            DELETE FROM BILL;
            INSERT INTO bill (Bill, Created_Time)
            VALUES (total_amount, NOW());
        END;
    ''')


    

# def create_xml_file():
#     cursor.execute("SELECT * from Books")
#     booksData = cursor.fetchall()

#     cursor.execute("SELECT * from Users")
#     usersData = cursor.fetchall()

#     cursor.execute("SELECT * from Carts")
#     cartsData = cursor.fetchall()

#     books_df = pd.DataFrame(booksData, columns=["BookID", "Title", "Author", "Price", "Quantity"])
#     users_df = pd.DataFrame(usersData, columns=["UserID", "Username", "Password"])
#     carts_df = pd.DataFrame(cartsData, columns=["CartID", "UserID", "BookID", "Quantity"])

#     root = ET.Element("root")

#     for _, row in books_df.iterrows():
#         book_element = ET.SubElement(root, "Book")
#         for col in books_df.columns:
#             sub_element = ET.SubElement(book_element, col)
#             sub_element.text = str(row[col])

#     for _, row in users_df.iterrows():
#         user_element = ET.SubElement(root, "User")
#         for col in users_df.columns:
#             sub_element = ET.SubElement(user_element, col)
#             sub_element.text = str(row[col])

#     for _, row in carts_df.iterrows():
#         cart_element = ET.SubElement(root, "Cart")
#         for col in carts_df.columns:
#             sub_element = ET.SubElement(cart_element, col)
#             sub_element.text = str(row[col])

#     new_tree = ET.ElementTree(root)
#     with open("OnlineBookstoreUpdated.xml", "wb") as file:
#         new_tree.write(file, encoding="utf-8", xml_declaration=True)
