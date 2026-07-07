from flask import Flask, request, jsonify
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)

# Task 2: Mock database array resembling OpenFoodFacts data structure
INVENTORY = [
    {
        "id": 1,
        "product_name": "Organic Almond Milk",
        "brands": "Silk",
        "ingredients_text": "Filtered water, almonds, cane sugar...",
        "price": 3.99,
        "stock": 45
    },
    {
        "id": 2,
        "product_name": "Whole Wheat Bread",
        "brands": "Baker's Choice",
        "ingredients_text": "Whole wheat flour, water, yeast...",
        "price": 2.49,
        "stock": 20
    }
]

# ==========================================
# EXTRA CRITERIA: EXTERNAL API INTEGRATION
# ==========================================
def fetch_from_openfoodfacts(barcode):
    """Queries the external OpenFoodFacts API to supplement product data"""
    url = f"https://world.openfoodfacts.org/api/v0/product/{barcode}.json"
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            data = response.json()
            if data.get("status") == 1:
                product_data = data.get("product", {})
                return {
                    "product_name": product_data.get("product_name", "Unknown Product"),
                    "brands": product_data.get("brands", "Unknown Brand"),
                    "ingredients_text": product_data.get("ingredients_text", "No ingredients provided.")
                }
    except requests.exceptions.RequestException:
        pass
    return None

# ==========================================
# RESTFUL ENDPOINTS (CRUD OPERATIONS)
# ==========================================

# 1. GET /inventory -> Fetch all items
@app.route('/inventory', methods=['GET'])
def get_all_items():
    return jsonify(INVENTORY), 200

# 2. GET /inventory/<id> -> Fetch a single item
@app.route('/inventory/<int:item_id>', methods=['GET'])
def get_single_item(item_id):
    item = next((i for i in INVENTORY if i["id"] == item_id), None)
    if not item:
        return jsonify({"error": "Item not found in inventory"}), 404
    return jsonify(item), 200

# 3. POST /inventory -> Add a new item (Handles manual or barcode lookups)
@app.route('/inventory', methods=['POST'])
def add_item():
    data = request.get_json()

    # Fix 2: Safety check for missing or invalid JSON body payloads
    if not data:
        return jsonify({"error": "Invalid JSON"}), 400

    barcode = data.get("barcode")

    # If a barcode is passed, fetch details externally to supplement data
    if barcode:
        external_details = fetch_from_openfoodfacts(barcode)
        if external_details:
            data.update(external_details)

    if "product_name" not in data or "price" not in data or "stock" not in data:
        return jsonify({"error": "Missing required fields (product_name, price, stock)"}), 400

    # Fix 1: Safeguard ID assignment logic to evaluate dynamic arrays safely
    new_item = {
        "id": max(item["id"] for item in INVENTORY) + 1 if INVENTORY else 1,
        "product_name": data["product_name"],
        "brands": data.get("brands", "Generic"),
        "ingredients_text": data.get("ingredients_text", "N/A"),
        "price": float(data["price"]),
        "stock": int(data["stock"])
    }
    INVENTORY.append(new_item)
    return jsonify(new_item), 201

# 4. PATCH /inventory/<id> -> Update an item partially
@app.route('/inventory/<int:item_id>', methods=['PATCH'])
def update_item(item_id):
    item = next((i for i in INVENTORY if i["id"] == item_id), None)
    if not item:
        return jsonify({"error": "Item not found"}), 404

    data = request.get_json()

    # Fix 3: Safety check for empty or broken update payloads
    if not data:
        return jsonify({"error": "Invalid JSON"}), 400

    if "price" in data:
        item["price"] = float(data["price"])
    if "stock" in data:
        item["stock"] = int(data["stock"])
    if "product_name" in data:
        item["product_name"] = data["product_name"]

    return jsonify(item), 200

# 5. DELETE /inventory/<id> -> Remove an item
@app.route('/inventory/<int:item_id>', methods=['DELETE'])
def delete_item(item_id):
    global INVENTORY
    item = next((i for i in INVENTORY if i["id"] == item_id), None)
    if not item:
        return jsonify({"error": "Item not found"}), 404

    INVENTORY = [i for i in INVENTORY if i["id"] != item_id]
    return jsonify({"message": f"Successfully removed item {item_id}"}), 200

if __name__ == "__main__":
    app.run(port=5000, debug=True)