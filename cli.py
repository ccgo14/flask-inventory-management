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
    item_id = input("Enter Item ID: ").strip()

    if not item_id.isdigit():
        print("[Error] Item ID must be a number.")
        return

    try:
        response = requests.get(f"{BASE_URL}/inventory/{item_id}")
        if response.status_code == 200:
            item = response.json()
            print(f"\nID: {item['id']} | {item['product_name']} | Brand: {item['brands']} | Price: {item['price']} | Stock: {item['stock']}")
        else:
            print("[Error] Item not found.")
    except requests.exceptions.ConnectionError:
        print("[Error] Could not connect to the Flask server.")

def add_new_item():
    print("\n[Action] Creating a new item...")
    product_name = input("Enter product name: ").strip()
    price = input("Enter price: ").strip()
    stock = input("Enter stock: ").strip()

    try:
        payload = {
            "product_name": product_name,
            "price": float(price),
            "stock": int(stock)
        }
    except ValueError:
        print("[Error] Invalid input types for price or stock.")
        return

    try:
        response = requests.post(f"{BASE_URL}/inventory", json=payload)
        if response.status_code == 201:
            item = response.json()
            print(f"\n[Success] Created ID: {item['id']} | {item['product_name']}")
        else:
            print("[Error] Could not create item.")
    except requests.exceptions.ConnectionError:
        print("[Error] Could not connect to the Flask server.")

def update_item():
    print("\n[Action] Updating an item's details...")
    item_id = input("Enter Item ID to modify: ").strip()

    if not item_id.isdigit():
        print("[Error] Item ID must be a number.")
        return

    print("Leave field blank to skip changing it.")
    price_input = input("New Price: ").strip()
    stock_input = input("New Stock: ").strip()
    name_input = input("New Product Name: ").strip()

    payload = {}
    if price_input:
        try:
            payload["price"] = float(price_input)
        except ValueError:
            print("[Error] Price must be a decimal.")
            return
    if stock_input:
        try:
            payload["stock"] = int(stock_input)
        except ValueError:
            print("[Error] Stock must be an integer.")
            return
    if name_input:
        payload["product_name"] = name_input

    if not payload:
        print("No updates provided. Aborting request.")
        return

    try:
        response = requests.patch(f"{BASE_URL}/inventory/{item_id}", json=payload)
        if response.status_code == 200:
            item = response.json()
            print(f"\n[Success] Updated item: ID {item['id']} | Name: {item['product_name']} | Price: {item['price']} | Stock: {item['stock']}")
        else:
            print("[Error] Could not update item.")
    except requests.exceptions.ConnectionError:
        print("[Error] Could not connect to the Flask server.")

def delete_item():
    print("\n[Action] Deleting an item from stock...")
    item_id = input("Enter Item ID to remove: ").strip()

    if not item_id.isdigit():
        print("[Error] Item ID must be a number.")
        return

    try:
        response = requests.delete(f"{BASE_URL}/inventory/{item_id}")
        if response.status_code == 200:
            print(f"\n[Success] {response.json().get('message')}")
        else:
            print("[Error] Item not found or could not be deleted.")
    except requests.exceptions.ConnectionError:
        print("[Error] Could not connect to the Flask server.")

def search_by_barcode():
    print("\n[Action] Querying product barcode details...")
    barcode = input("Enter Barcode: ").strip()
    price = input("Assign Price: ").strip()
    stock = input("Assign Stock: ").strip()

    try:
        payload = {
            "barcode": barcode,
            "price": float(price),
            "stock": int(stock)
        }
    except ValueError:
        print("[Error] Invalid input types for price or stock.")
        return

    try:
        response = requests.post(f"{BASE_URL}/inventory", json=payload)
        if response.status_code == 201:
            item = response.json()
            print(f"\n[Success] Imported via Barcode -> ID: {item['id']} | {item['product_name']} ({item['brands']})")
        else:
            print("[Error] Failed to process barcode payload.")
    except requests.exceptions.ConnectionError:
        print("[Error] Could not connect to the Flask server.")

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