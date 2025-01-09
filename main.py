# main.py
import utils

def main_menu():
    print("""
    1. Add Customer
    2. View Customers
    3. Add Vehicle
    4. View Vehicles
    5. Add Service Request
    6. View Services
    7. Exit
    """)

def main():
    # Connect to database
    connection = utils.connect_to_database(host="localhost", user="root", password="chill@hell", database="project")

    if not connection:
        return

    # Create tables if they don't exist
    utils.create_tables(connection)

    while True:
        main_menu()
        choice = input("Enter your choice: ")

        if choice == '1':
            name = input("Enter Name: ")
            contact = input("Enter Contact: ")
            email = input("Enter Email: ")
            address = input("Enter Address: ")
            utils.add_customer(connection, name, contact, email, address)

        elif choice == '2':
            customers = utils.view_customers(connection)
            if customers:
                for customer in customers:
                    print(customer)
            else:
                print("No customers found.")

        elif choice == '3':
            make = input("Enter Vehicle Make: ")
            model = input("Enter Vehicle Model: ")
            registration_number = input("Enter Registration Number: ")
            owner_id = input("Enter Owner ID: ")
            utils.add_vehicle(connection, make, model, registration_number, owner_id)

        elif choice == '4':
            vehicles = utils.view_vehicles(connection)
            if vehicles:
                for vehicle in vehicles:
                    print(vehicle)
            else:
                print("No vehicles found.")

        elif choice == '5':
            vehicle_id = input("Enter Vehicle ID: ")
            service_type = input("Enter Service Type: ")
            description = input("Enter Description: ")
            status = input("Enter Status: ")
            cost = input("Enter Cost: ")
            date = input("Enter Date (YYYY-MM-DD): ")
            utils.add_service(connection, vehicle_id, service_type, description, status, cost, date)

        elif choice == '6':
            services = utils.view_services(connection)
            if services:
                for service in services:
                    print(service)
            else:
                print("No services found.")

        elif choice == '7':
            print("Exiting program. Goodbye!")
            break

        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
