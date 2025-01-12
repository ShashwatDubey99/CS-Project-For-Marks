import mariadb

# Function to get a database connection
def get_connection():
    return mariadb.connect(
        user='root',
        password='chill@hell',
        host='127.0.0.1',
        database='vehicle_service_center'
    )

# Initialize the database
def initialize_db():
    conn = get_connection()
    cursor = conn.cursor()

    # Create necessary tables
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS VehicleTypes (
            vehicle_type_id VARCHAR(10) PRIMARY KEY,
            vehicle_type_name TEXT UNIQUE
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Customers (
            customer_id INT PRIMARY KEY AUTO_INCREMENT,
            customer_name TEXT,
            mobile_no TEXT UNIQUE,
            address TEXT
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Services (
            service_id INT PRIMARY KEY AUTO_INCREMENT,
            service_name TEXT UNIQUE,
            cost REAL
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS VehicleRegistrations (
            registration_id INT PRIMARY KEY AUTO_INCREMENT,
            vehicle_type_id VARCHAR(10),
            license_plate TEXT,
            customer_id INT,
            service_ids TEXT,
            status TEXT DEFAULT 'in_queue',
            FOREIGN KEY (customer_id) REFERENCES Customers (customer_id),
            FOREIGN KEY (vehicle_type_id) REFERENCES VehicleTypes (vehicle_type_id)
        )
    ''')

    conn.commit()
    conn.close()


# Add a vehicle type
def add_vehicle_type():
    conn = get_connection()
    cursor = conn.cursor()
    vehicle_type_id = input("Enter vehicle type ID: ")
    vehicle_type_name = input("Enter vehicle type name (e.g., Two Wheeler, Car, Truck): ")
    try:
        cursor.execute('INSERT INTO VehicleTypes (vehicle_type_id, vehicle_type_name) VALUES (?, ?)',
                       (vehicle_type_id, vehicle_type_name))
        conn.commit()
        print("Vehicle type added successfully.")
    except mariadb.IntegrityError:
        print("Vehicle type ID or name already exists.")
    conn.close()


# Remove a vehicle type
def remove_vehicle_type():
    conn = get_connection()
    cursor = conn.cursor()
    vehicle_type_id = input("Enter the Vehicle Type ID to remove: ")
    cursor.execute('DELETE FROM VehicleTypes WHERE vehicle_type_id = ?', (vehicle_type_id,))
    conn.commit()
    if cursor.rowcount > 0:
        print("Vehicle type removed successfully.")
    else:
        print("Vehicle type not found.")
    conn.close()


# Add a customer
def add_customer():
    conn = get_connection()
    cursor = conn.cursor()
    customer_name = input("Enter customer name: ")
    mobile_no = input("Enter mobile number: ")
    address = input("Enter address: ")
    try:
        cursor.execute('INSERT INTO Customers (customer_name, mobile_no, address) VALUES (?, ?, ?)',
                       (customer_name, mobile_no, address))
        conn.commit()
        print("Customer added successfully.")
    except mariadb.IntegrityError:
        print("Customer with this mobile number already exists.")
    conn.close()


# Remove a customer
def remove_customer():
    conn = get_connection()
    cursor = conn.cursor()
    customer_id = int(input("Enter Customer ID to remove: "))
    cursor.execute('DELETE FROM Customers WHERE customer_id = ?', (customer_id,))
    conn.commit()
    if cursor.rowcount > 0:
        print("Customer removed successfully.")
    else:
        print("Customer not found.")
    conn.close()


# Add a service
def add_service():
    conn = get_connection()
    cursor = conn.cursor()
    service_name = input("Enter service name (e.g., Car Wash, Oil Change): ")
    cost = float(input("Enter service cost: "))
    try:
        cursor.execute('INSERT INTO Services (service_name, cost) VALUES (?, ?)',
                       (service_name, cost))
        conn.commit()
        print("Service added successfully.")
    except mariadb.IntegrityError:
        print("Service already exists.")
    conn.close()


# Remove a service
def remove_service():
    conn = get_connection()
    cursor = conn.cursor()
    service_id = int(input("Enter Service ID to remove: "))
    cursor.execute('DELETE FROM Services WHERE service_id = ?', (service_id,))
    conn.commit()
    if cursor.rowcount > 0:
        print("Service removed successfully.")
    else:
        print("Service not found.")
    conn.close()


# Register a vehicle
def register_vehicle():
    conn = get_connection()
    cursor = conn.cursor()
    vehicle_type_id = input("Enter vehicle type ID: ")
    license_plate = input("Enter license plate: ")
    customer_id = int(input("Enter customer ID: "))
    service_ids = input("Enter service IDs (comma-separated): ")
    try:
        cursor.execute('''
            INSERT INTO VehicleRegistrations (vehicle_type_id, license_plate, customer_id, service_ids) 
            VALUES (?, ?, ?, ?)
        ''', (vehicle_type_id, license_plate, customer_id, service_ids))
        conn.commit()
        print("Vehicle registered successfully.")
    except mariadb.IntegrityError:
        print("Vehicle with this license plate already exists.")
    finally:
        conn.close()


# Update service status
def update_service_status():
    conn = get_connection()
    cursor = conn.cursor()
    registration_id = int(input("Enter Registration ID: "))
    status = input("Enter new status (in_queue, ongoing, finished): ")
    cursor.execute('UPDATE VehicleRegistrations SET status = ? WHERE registration_id = ?',
                   (status, registration_id))
    conn.commit()
    if cursor.rowcount > 0:
        print("Service status updated successfully.")
    else:
        print("Registration ID not found.")
    conn.close()


# View details by various filters
def view_details_by_status():
    conn = get_connection()
    cursor = conn.cursor()
    status = input("Enter status (in_queue, ongoing, finished): ")
    cursor.execute('''
        SELECT vr.registration_id, vr.license_plate, c.customer_name, vt.vehicle_type_id, vr.status
        FROM VehicleRegistrations vr
        JOIN Customers c ON vr.customer_id = c.customer_id
        JOIN VehicleTypes vt ON vr.vehicle_type_id = vt.vehicle_type_id
        WHERE vr.status = ?
    ''', (status,))
    results = cursor.fetchall()

    print("\n--- Vehicles with Status: {} ---\n".format(status))
    if results:
        for result in results:
            print(f"(registration_id, license_plate, customer_name, vehicle_type_id, status) -> {result}")
    else:
        print("No records found.")
    conn.close()


# Generate bill
def generate_bill():
    conn = get_connection()
    cursor = conn.cursor()
    registration_id = int(input("Enter Registration ID: "))
    cursor.execute('''
        SELECT vr.service_ids, c.customer_name, c.address, vt.vehicle_type_id
        FROM VehicleRegistrations vr
        JOIN Customers c ON vr.customer_id = c.customer_id
        JOIN VehicleTypes vt ON vr.vehicle_type_id = vt.vehicle_type_id
        WHERE vr.registration_id = ?
    ''', (registration_id,))
    result = cursor.fetchone()

    if result:
        service_ids, customer_name, address, vehicle_type_id = result
        ids = service_ids.split(',')
        total_cost = 0
        for service_id in ids:
            cursor.execute('SELECT cost FROM Services WHERE service_id = ?', (service_id,))
            cost = cursor.fetchone()[0]
            total_cost += cost
        gst = 0.18 * total_cost
        total_bill = total_cost + gst

        print("\n--- Bill Details ---")
        print(f"Customer Name: {customer_name}")
        print(f"Address: {address}")
        print(f"Vehicle Type ID: {vehicle_type_id}")
        print(f"Total Cost: {total_cost:.2f}")
        print(f"GST (18%): {gst:.2f}")
        print(f"Total Bill: {total_bill:.2f}")
    else:
        print("Registration not found.")
    conn.close()


# Display tables
def display_tables():
    conn = get_connection()
    cursor = conn.cursor()

    print("\n--- Vehicle Types ---")
    cursor.execute('SELECT * FROM VehicleTypes')
    vehicle_types = cursor.fetchall()
    for vehicle_type in vehicle_types:
        print(f"(vehicle_type_id, vehicle_type_name) ->\n {vehicle_type}")

    print("\n--- Customers ---")
    cursor.execute('SELECT * FROM Customers')
    customers = cursor.fetchall()
    for customer in customers:
        print(f"(customer_id, customer_name, mobile_no, address) -> \n {customer}")
    
    print("\n--- Services ---")
    cursor.execute('SELECT * FROM Services')
    services = cursor.fetchall()
    for customer in customers:
        print(f"(service_id, Service_name, cost) -> \n{services}")

    conn.close()

