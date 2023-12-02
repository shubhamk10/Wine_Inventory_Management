import mysql.connector
import pandas as pd
from Admin_config import HOST, USER, PASSWORD, PORT
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
        CREATE TABLE IF NOT EXISTS Customer (
            Store_Id int,
            Name VARCHAR(30),
            Cust_Id int,
            Status VARCHAR(20),
            Phone_Number VARCHAR(30),
            PRIMARY KEY(Cust_Id, Store_Id)
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Admin (
            Admin_Id int,
            Name VARCHAR(30),
            Phone_Number VARCHAR(30),
            Password VARCHAR(20),
            PRIMARY KEY(Admin_Id)
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
            CREATE TABLE IF NOT EXISTS Retailer (
                Retailer_Id int,
                Name VARCHAR(30),
                Wine_Bottle_Id int,
                R_Selling_Price int,
                PRIMARY KEY(Retailer_ID,Wine_Bottle_Id)
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
        CREATE TABLE IF NOT EXISTS Cellar (
            Man_Id int,
            Cellar_Id int,
            Name VARCHAR(30),
            Quantity int,
            PRIMARY KEY (Man_Id,Cellar_Id)
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
        ALTER TABLE Customer
        ADD FOREIGN KEY (Store_Id) REFERENCES Store(Store_Id)
    ''')

    cursor.execute('''
        ALTER TABLE Stock
        ADD FOREIGN KEY (Store_Id) REFERENCES Store(Store_Id)              
    ''')

    cursor.execute('''
        ALTER TABLE Cellar
        ADD FOREIGN KEY (Man_Id) REFERENCES Manufacturer(Man_Id)              
    ''')

def add_data(uploadedFile):
    tree = ET.parse(uploadedFile)
    StoresData = tree.findall('Store')
    CustomersData = tree.findall('Customer')
    WineBottleData = tree.findall('winebottle')
    RetailerData = tree.findall('retailer')
    ManufacturerData = tree.findall('manufacturer')
    CellarData = tree.findall('cellar')
    StockData = tree.findall('stock')
    AdminData = tree.findall('Admin')

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
        store_id = int(customer.find('StoreId').text)
        name = customer.find('Name').text
        cust_id = int(customer.find('CustId').text)
        status = customer.find('Status').text
        phone_number = int(customer.find('PhoneNumber').text)

        # Insert the data into the 'Customers' table
        cursor.execute("INSERT INTO Customer (Store_Id, Name, Cust_Id, Status, Phone_Number) VALUES (%s, %s, %s, %s, %s)",(store_id, name, cust_id, status, phone_number))

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

    for retailer in RetailerData:
        retailer_id = int(retailer.find('RetailerId').text)
        name = retailer.find('Name').text
        wine_bottle_id = int(retailer.find('WineBottleId').text)
        r_selling_price = float(retailer.find('RSellingPrice').text)

        # Insert the data into the 'Retailers' table
        cursor.execute("INSERT INTO Retailer (Retailer_Id, Name, Wine_Bottle_Id, R_Selling_Price) VALUES (%s, %s, %s, %s)",(retailer_id, name, wine_bottle_id, r_selling_price))

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

    for cellar in CellarData:
        man_id = int(cellar.find('Man_Id').text)
        cellar_id = int(cellar.find('Cellar_Id').text)
        name = cellar.find('Name').text
        quantity = int(cellar.find('Quantity').text)

        # Insert the data into the 'Cellar' table
        cursor.execute("INSERT INTO Cellar (Man_Id, Cellar_Id, Name, Quantity) VALUES (%s, %s, %s, %s)",(man_id, cellar_id, name, quantity))
    
    for stock in StockData:
        store_id = int(stock.find('StoreId').text)
        wine_bottle_id = int(stock.find('WineBottleId').text)
        quantity = int(stock.find('Quantity').text)
        retailer_id = int(stock.find('RetailerId').text)

        # Insert the data into the 'Stock' table
        cursor.execute("INSERT INTO Stock (Store_Id, Wine_Bottle_Id, Quantity, Retailer_Id) VALUES (%s, %s, %s, %s)",(store_id, wine_bottle_id, quantity, retailer_id))

    for admin in AdminData:
        admin_id = int(admin.find('AdminId').text)
        name = admin.find('Name').text
        PhoneNumber = admin.find('PhoneNumber').text
        Password = admin.find('Password').text

        cursor.execute("INSERT INTO Admin (Admin_Id, Name, Phone_Number, Password) VALUES (%s, %s, %s, %s)",(admin_id, name, PhoneNumber, Password))
    connection.commit()


def view_data():
    cursor.execute("SELECT * from Store")
    StoreData = cursor.fetchall()

    cursor.execute("SELECT * from Customer")
    CustomerData = cursor.fetchall()

    cursor.execute("SELECT * from Wine_Bottles")
    Wine_BottlesData = cursor.fetchall()

    cursor.execute("SELECT * from Stock")
    StockData = cursor.fetchall()
    
    cursor.execute("SELECT * from Retailer")
    RetailerData = cursor.fetchall()
    
    cursor.execute("SELECT * from Manufacturer")
    ManufacturerData = cursor.fetchall()

    cursor.execute("SELECT * from Cellar")
    CellarData = cursor.fetchall()

    return StoreData, CustomerData, Wine_BottlesData, StockData, RetailerData, ManufacturerData, CellarData 


def runquery(command):
    cursor.execute(command)
    result=cursor.fetchall()
    return result    

def get_cartids():
    cursor.execute("SELECT CartID FROM Carts")
    data = cursor.fetchall()
    return data


def delete_data(cart_id):
    cursor.execute('DELETE FROM Carts WHERE CartID="{}"'.format(cart_id))
    connection.commit()


def update_book_quantity(book_id, newQuant):
    cursor.execute('UPDATE Books SET Quantity = %s WHERE BookID = %s', (newQuant, book_id))
    connection.commit()


def create_xml_file():
    cursor.execute("SELECT * from Books")
    booksData = cursor.fetchall()

    cursor.execute("SELECT * from Users")
    usersData = cursor.fetchall()

    cursor.execute("SELECT * from Carts")
    cartsData = cursor.fetchall()

    books_df = pd.DataFrame(booksData, columns=["BookID", "Title", "Author", "Price", "Quantity"])
    users_df = pd.DataFrame(usersData, columns=["UserID", "Username", "Password"])
    carts_df = pd.DataFrame(cartsData, columns=["CartID", "UserID", "BookID", "Quantity"])

    root = ET.Element("root")

    for _, row in books_df.iterrows():
        book_element = ET.SubElement(root, "Book")
        for col in books_df.columns:
            sub_element = ET.SubElement(book_element, col)
            sub_element.text = str(row[col])

    for _, row in users_df.iterrows():
        user_element = ET.SubElement(root, "User")
        for col in users_df.columns:
            sub_element = ET.SubElement(user_element, col)
            sub_element.text = str(row[col])

    for _, row in carts_df.iterrows():
        cart_element = ET.SubElement(root, "Cart")
        for col in carts_df.columns:
            sub_element = ET.SubElement(cart_element, col)
            sub_element.text = str(row[col])

    new_tree = ET.ElementTree(root)
    with open("OnlineBookstoreUpdated.xml", "wb") as file:
        new_tree.write(file, encoding="utf-8", xml_declaration=True)
