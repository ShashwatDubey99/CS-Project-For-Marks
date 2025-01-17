import mysql.connector
from mysql.connector import IntegrityError

# Function to get a database connection
def get_connection():
    return mysql.connector.connect(
        user='root',
        password='chill@hell',
        host='127.0.0.1',
        database='VSC'
    )

# Initialize the database
def initialize_db():
    conn = get_connection()
    cursor = conn.cursor()

    # Create necessary tables
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS VehicleTypes (
            vehicle_type_id VARCHAR(10) PRIMARY KEY,
            vehicle_type_name VARCHAR(40) UNIQUE
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Customers (
            customer_id INT PRIMARY KEY AUTO_INCREMENT,
            customer_name VARCHAR(40),
            mobile_no VARCHAR(40) UNIQUE,
            address VARCHAR(40)
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Services (
            service_id INT PRIMARY KEY AUTO_INCREMENT,
            service_name VARCHAR(40) UNIQUE,
            cost REAL
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS VehicleRegistrations (
            registration_id INT PRIMARY KEY AUTO_INCREMENT,
            vehicle_type_id VARCHAR(10),
            license_plate VARCHAR(40) UNIQUE,
            customer_id INT,
            service_ids VARCHAR(40),
            status VARCHAR(40) DEFAULT 'in_queue',
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
    vehicle_type_id = input("Enter vehicle type ID: ").strip()
    vehicle_type_name = input("Enter vehicle type name (e.g., Two Wheeler, Car, Truck): ").strip()
    try:
        cursor.execute(
            'INSERT INTO VehicleTypes (vehicle_type_id, vehicle_type_name) VALUES (%s, %s)',
            (vehicle_type_id, vehicle_type_name)
        )
        conn.commit()
        print("Vehicle type added successfully.")
    except IntegrityError as e:
        print("Error: Vehicle type ID or name already exists.")
    finally:
        conn.close()

# Remove a vehicle type
def remove_vehicle_type():
    conn = get_connection()
    cursor = conn.cursor()
    vehicle_type_id = input("Enter the Vehicle Type ID to remove: ").strip()
    cursor.execute('DELETE FROM VehicleTypes WHERE vehicle_type_id = %s', (vehicle_type_id,))
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
    customer_name = input("Enter customer name: ").strip()
    mobile_no = input("Enter mobile number: ").strip()
    address = input("Enter address: ").strip()
    try:
        cursor.execute(
            'INSERT INTO Customers (customer_name, mobile_no, address) VALUES (%s, %s, %s)',
            (customer_name, mobile_no, address)
        )
        conn.commit()
        print("Customer added successfully.")
    except IntegrityError as e:
        print("Error: Customer with this mobile number already exists.")
    finally:
        conn.close()

# Remove a customer
def remove_customer():
    conn = get_connection()
    cursor = conn.cursor()
    customer_id = int(input("Enter Customer ID to remove: ").strip())
    cursor.execute('DELETE FROM Customers WHERE customer_id = %s', (customer_id,))
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
    service_name = input("Enter service name (e.g., Car Wash, Oil Change): ").strip()
    cost = float(input("Enter service cost: "))
    try:
        cursor.execute(
            'INSERT INTO Services (service_name, cost) VALUES (%s, %s)',
            (service_name, cost)
        )
        conn.commit()
        print("Service added successfully.")
    except IntegrityError as e:
        print("Error: Service already exists.")
    finally:
        conn.close()

# Remove a service
def remove_service():
    conn = get_connection()
    cursor = conn.cursor()
    service_id = int(input("Enter Service ID to remove: ").strip())
    cursor.execute('DELETE FROM Services WHERE service_id = %s', (service_id,))
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
    vehicle_type_id = input("Enter vehicle type ID: ").strip()
    license_plate = input("Enter license plate: ").strip()
    customer_id = int(input("Enter customer ID: ").strip())
    service_ids = input("Enter service IDs (comma-separated): ").strip()
    try:
        cursor.execute(
            '''
            INSERT INTO VehicleRegistrations (vehicle_type_id, license_plate, customer_id, service_ids) 
            VALUES (%s, %s, %s, %s)
            ''', (vehicle_type_id, license_plate, customer_id, service_ids)
        )
        conn.commit()
        print("Vehicle registered successfully.")
    except IntegrityError as e:
        print("Error: Vehicle with this license plate already exists.")
    finally:
        conn.close()

# Update service status
def update_service_status():
    conn = get_connection()
    cursor = conn.cursor()
    registration_id = int(input("Enter Registration ID: ").strip())
    status = input("Enter new status (in_queue, ongoing, finished): ").strip()
    cursor.execute(
        'UPDATE VehicleRegistrations SET status = %s WHERE registration_id = %s',
        (status, registration_id)
    )
    conn.commit()
    if cursor.rowcount > 0:
        print("Service status updated successfully.")
    else:
        print("Registration ID not found.")
    conn.close()

def update_service_selected():
    conn = get_connection()
    cursor = conn.cursor()
    registration_id = int(input("Enter Registration ID: ").strip())
    service_ids = input("Enter service IDs (comma-separated): ").strip()
    cursor.execute(
        'UPDATE VehicleRegistrations SET service_ids = %s WHERE registration_id = %s',
        (service_ids, registration_id)
    )
    conn.commit()
    if cursor.rowcount > 0:
        print("Service  updated successfully.")
    else:
        print("Registration ID not found.")
    conn.close()
    

# View details by status
def view_details_by_status():
    conn = get_connection()
    cursor = conn.cursor()
    status = input("Enter status (in_queue, ongoing, finished): ").strip()
    cursor.execute('''
        SELECT vr.registration_id, vr.license_plate, c.customer_name, vt.vehicle_type_id, vr.status
        FROM VehicleRegistrations vr
        JOIN Customers c ON vr.customer_id = c.customer_id
        JOIN VehicleTypes vt ON vr.vehicle_type_id = vt.vehicle_type_id
        WHERE vr.status = %s
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
    registration_id = int(input("Enter Registration ID: ").strip())
    cursor.execute('''
        SELECT vr.service_ids, c.customer_name, c.address, vt.vehicle_type_id, vr.status
        FROM VehicleRegistrations vr
        JOIN Customers c ON vr.customer_id = c.customer_id
        JOIN VehicleTypes vt ON vr.vehicle_type_id = vt.vehicle_type_id
        WHERE vr.registration_id = %s
    ''', (registration_id,))
    result = cursor.fetchone()

    if result:
        service_ids, customer_name, address, vehicle_type_id, current_status = result
        ids = service_ids.split(',')
        total_cost = 0
        service_details = []

        # Fetch service names and costs
        for service_id in ids:
            cursor.execute('SELECT service_name, cost FROM Services WHERE service_id = %s', (service_id,))
            service = cursor.fetchone()
            if service:
                service_name, cost = service
                service_details.append((service_name, cost))
                total_cost += cost

        gst = 0.18 * total_cost
        total_bill = total_cost + gst

        # Prompt user to update the status
        if current_status != "finished":
            update_status = input("Do you want to update the status to 'finished'? (yes/no): ").strip().lower()
            if update_status == "yes":
                cursor.execute(
                    'UPDATE VehicleRegistrations SET status = %s WHERE registration_id = %s',
                    ("finished", registration_id)
                )
                conn.commit()
                print("Status updated to 'finished'.")

        # Print the bill
        print("\n--- Bill Details ---")
        print(f"Customer Name: {customer_name}")
        print(f"Address: {address}")
        print(f"Vehicle Type ID: {vehicle_type_id}")
        print("\nServices Selected:")
        for service_name, cost in service_details:
            print(f" - {service_name}: ₹{cost:.2f}")
        print(f"\nTotal Cost: ₹{total_cost:.2f}")
        print(f"GST (18%): ₹{gst:.2f}")
        print(f"Total Bill: ₹{total_bill:.2f}")

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
        print(f"(vehicle_type_id, vehicle_type_name) -> {vehicle_type}")

    print("\n--- Customers ---")
    cursor.execute('SELECT * FROM Customers')
    customers = cursor.fetchall()
    for customer in customers:
        print(f"(customer_id, customer_name, mobile_no, address) -> {customer}")
    
    print("\n--- Services ---")
    cursor.execute('SELECT * FROM Services')
    services = cursor.fetchall()
    for service in services:
        print(f"(service_id, service_name, cost) -> {service}")

    conn.close()

# Initialize database on first run
if __name__ == "__main__":
    initialize_db()
