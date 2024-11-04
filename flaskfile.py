from flask import Flask, request, jsonify
import json

app = Flask(__name__)

# Fungsi untuk membaca data dari file JSON
def load_data():
    with open("db.json", "r") as file:
        return json.load(file)

# Fungsi untuk menyimpan data ke file JSON
def save_data(data):
    with open("db.json", "w") as file:
        json.dump(data, file)

# Endpoint untuk menampilkan semua item
@app.route('/items', methods=['GET'])
def list_items():
    items = load_data()
    return jsonify(items), 200

# Endpoint untuk menambahkan item baru
@app.route('/items', methods=['POST'])
def add_item():
    items = load_data()
    new_item = request.get_json()
    new_item["id"] = max([item["id"] for item in items] + [0]) + 1
    items.append(new_item)
    save_data(items)
    return jsonify(new_item), 201

# Endpoint untuk menampilkan item berdasarkan ID
@app.route('/items/<int:item_id>', methods=['GET'])
def fetch_item(item_id):
    items = load_data()
    item = next((i for i in items if i["id"] == item_id), None)
    if item:
        return jsonify(item), 200
    return jsonify({"error": "Item tidak ditemukan"}), 404

# Endpoint untuk memperbarui item berdasarkan ID
@app.route('/items/<int:item_id>', methods=['PUT'])
def modify_item(item_id):
    items = load_data()
    item = next((i for i in items if i["id"] == item_id), None)
    if item:
        updated_data = request.get_json()
        item.update(updated_data)
        save_data(items)
        return jsonify(item), 200
    return jsonify({"error": "Item tidak ditemukan"}), 404

# Endpoint untuk menghapus item berdasarkan ID
@app.route('/items/<int:item_id>', methods=['DELETE'])
def remove_item(item_id):
    items = load_data()
    item = next((i for i in items if i["id"] == item_id), None)
    if item:
        items.remove(item)
        save_data(items)
        return jsonify({"message": "Item berhasil dihapus"}), 200
    return jsonify({"error": "Item tidak ditemukan"}), 404

if __name__ == '__main__':
    app.run(debug=True)
