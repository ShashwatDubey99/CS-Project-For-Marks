# utils.py
import mariadb
from mariadb import Error

def connect_to_database(host, user, password, database):
    try:
        connection = mariadb.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )
        print("Connected to the database.")
        return connection
    except Error as e:
        print(f"Error connecting to database: {e}")
        return None

def execute_query(connection, query, values=None):
    try:
        cursor = connection.cursor()
        cursor.execute(query, values)
        connection.commit()
        return cursor
    except Error as e:
        print(f"Error executing query: {e}")


def fetch_all(connection, query, values=None):
    try:
        cursor = connection.cursor()
        cursor.execute(query, values)
        return cursor.fetchall()
    except Error as e:
        print(f"Error fetching data: {e}")
        return []

def create_tables(connection):
    queries = [
        """CREATE TABLE IF NOT EXISTS Customers (
            CustomerID INT AUTO_INCREMENT PRIMARY KEY,
            Name VARCHAR(100),
            Contact VARCHAR(15),
            Email VARCHAR(100),
            Address TEXT
        )""",
        """CREATE TABLE IF NOT EXISTS Vehicles (
            VehicleID INT AUTO_INCREMENT PRIMARY KEY,
            Make VARCHAR(50),
            Model VARCHAR(50),
            RegistrationNumber VARCHAR(20) UNIQUE,
            OwnerID INT,
            FOREIGN KEY (OwnerID) REFERENCES Customers(CustomerID)
        )""",
        """CREATE TABLE IF NOT EXISTS Services (
            ServiceID INT AUTO_INCREMENT PRIMARY KEY,
            VehicleID INT,
            ServiceType VARCHAR(50),
            Description TEXT,
            Status VARCHAR(20),
            Cost DECIMAL(10, 2),
            Date DATE,
            FOREIGN KEY (VehicleID) REFERENCES Vehicles(VehicleID)
        )"""
    ]

    for query in queries:
        execute_query(connection, query)
    print("Tables created successfully.")

def add_customer(connection, name, contact, email, address):
    query = "INSERT INTO Customers (Name, Contact, Email, Address) VALUES (%s, %s, %s, %s)"
    execute_query(connection, query, (name, contact, email, address))
    print("Customer added successfully.")

def view_customers(connection):
    query = "SELECT * FROM Customers"
    customers = fetch_all(connection, query)
    return customers

def add_vehicle(connection, make, model, registration_number, owner_id):
    query = "INSERT INTO Vehicles (Make, Model, RegistrationNumber, OwnerID) VALUES (%s, %s, %s, %s)"
    execute_query(connection, query, (make, model, registration_number, owner_id))
    print("Vehicle added successfully.")

def view_vehicles(connection):
    query = "SELECT * FROM Vehicles"
    vehicles = fetch_all(connection, query)
    return vehicles

def add_service(connection, vehicle_id, service_type, description, status, cost, date):
    query = "INSERT INTO Services (VehicleID, ServiceType, Description, Status, Cost, Date) VALUES (%s, %s, %s, %s, %s, %s)"
    execute_query(connection, query, (vehicle_id, service_type, description, status, cost, date))
    print("Service request added successfully.")

def view_services(connection):
    query = "SELECT * FROM Services"
    services = fetch_all(connection, query)
    return services
