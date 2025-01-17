import utils

def main():
    # Initialize the database
    utils.initialize_db()

    while True:
        print("\n--- Vehicle Service Center Management ---")
        print("1. Add Vehicle Type")
        print("2. Remove Vehicle Type")
        print("3. Add Customer")
        print("4. Remove Customer")
        print("5. Add Service")
        print("6. Remove Service")
        print("7. Register Vehicle")
        print("8. Update Service Status")
        print("9. Update Services Of Registered Vehicle")
        print("10. View Details by Status")
        print("11. View All Tables (Vehicle Types & Customers)")
        print("12. Generate Bill/Invoice")
        print("13. Exit")

        choice = input("Enter your choice (1-13): ")

        if choice == "1":
            utils.add_vehicle_type()
        elif choice == "2":
            utils.remove_vehicle_type()
        elif choice == "3":
            utils.add_customer()
        elif choice == "4":
            utils.remove_customer()
        elif choice == "5":
            utils.add_service()
        elif choice == "6":
            utils.remove_service()
        elif choice == "7":
            utils.register_vehicle()
        elif choice == "8":
            utils.update_service_status()
        elif choice == "9":
            utils.update_service_selected()    
        elif choice == "10":
            utils.view_details_by_status()
        elif choice == "11":
            utils.display_tables()
        elif choice == "12":
            utils.generate_bill()
        elif choice == "13":
            print("Exiting... Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()


