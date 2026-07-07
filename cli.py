import sys
import requests

BASE_URL = "http://127.0.0.1:5000"

def display_menu():
    print("\n==========================================")
    print("   INVENTORY MANAGEMENT ADMIN PORTAL")
    print("==========================================")
    print("1. View all inventory")
    print("2. View single item")
    print("3. Add new item")
    print("4. Update item")
    print("5. Delete item")
    print("6. Search by barcode")
    print("0. Exit")
    print("==========================================")

def view_all_inventory():
    print("\n[Action] Fetching all inventory items...")
    try:
        response = requests.get(f"{BASE_URL}/inventory")
        if response.status_code == 200:
            items = response.json()
            for item in items:
                print(f"\nID: {item['id']} | {item['product_name']} | Price: {item['price']} | Stock: {item['stock']}")
        else:
            print("[Error] Could not fetch inventory.")
    except requests.exceptions.ConnectionError:
        print("[Error] Could not connect to the Flask server.")

def view_single_item():
    print("\n[Action] Fetching a single item...")
    pass

def add_new_item():
    print("\n[Action] Creating a new item...")
    pass

def update_item():
    print("\n[Action] Updating an item's details...")
    pass

def delete_item():
    print("\n[Action] Deleting an item from stock...")
    pass

def search_by_barcode():
    print("\n[Action] Querying product barcode details...")
    pass

def main():
    while True:
        display_menu()
        choice = input("Select an option (0-6): ").strip()

        if choice == "1":
            view_all_inventory()
        elif choice == "2":
            view_single_item()
        elif choice == "3":
            add_new_item()
        elif choice == "4":
            update_item()
        elif choice == "5":
            delete_item()
        elif choice == "6":
            search_by_barcode()
        elif choice == "0":
            print("\nExiting Administrative Portal. Goodbye!")
            sys.exit(0)
        else:
            print("\n[Error] Invalid choice! Please enter a number between 0 and 6.")

if __name__ == "__main__":
    main()