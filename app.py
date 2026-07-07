from flask import Flask, jsonify, request

app = Flask(__name__)

inventory = [
    {"id": 1, "name": "Water Bottle", "price": 50, "quantity": 100},
    {"id": 2, "name": "Juice", "price": 80, "quantity": 50}
]

@app.route('/inventory', methods=['GET'])
def get_all():
    return jsonify(inventory), 200

@app.route('/inventory/<int:id>', methods=['GET'])
def get_one(id):
    item = next((i for i in inventory if i['id'] == id), None)
    return jsonify(item), 200 if item else (jsonify({"error": "Not found"}), 404)

@app.route('/inventory', methods=['POST'])
def add_item():
    data = request.get_json()
    data['id'] = len(inventory) + 1
    inventory.append(data)
    return jsonify(data), 201

@app.route('/inventory/<int:id>', methods=['PATCH'])
def update_item(id):
    item = next((i for i in inventory if i['id'] == id), None)
    if not item:
        return jsonify({"error": "Not found"}), 404
    data = request.get_json()
    item.update(data)
    return jsonify(item), 200

@app.route('/inventory/<int:id>', methods=['DELETE'])
def delete_item(id):
    global inventory
    item = next((i for i in inventory if i['id'] == id), None)
    if not item:
        return jsonify({"error": "Not found"}), 404
    inventory = [i for i in inventory if i['id'] != id]
    return jsonify({"message": "Deleted"}), 200

if __name__ == '__main__':
    app.run(debug=True)