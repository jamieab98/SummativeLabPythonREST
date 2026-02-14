from flask import Flask, jsonify, request

from inventory_data import inventory
from api_service import fetchAPIData

app = Flask(__name__)

@app.route("/")
def default():
    return "Welcome to the inventory!"

@app.route("/inventory")
def view_inventory():
    response = []
    for item in inventory:
        response.append({"product": item['product_name'], "quantity": item['quantity']})
        print(f"Product: {item['product_name']}")
        print(f"Quantity: {item['quantity']}")
    return jsonify(response), 200

@app.route("/inventory/<int:id>")
def view_item(id):
    item = next((i for i in inventory if i['id'] == id), None)
    print(item)
    return jsonify(item), 200

@app.route("/inventory", methods = ["POST"])
def add_item():
    item = request.get_json()
    item_barcode = item["barcode"]
    item_quantity = item["quantity"]
    item_data = fetchAPIData(item_barcode)
    if item_data["status_verbose"] != "product found":
        print("item not found")
        return jsonify({"message": "Item not found"}), 404
    if str(item_barcode) in [item["barcode_number"] for item in inventory]:
        return jsonify({"message": "Item is already in the inventory"}), 405
    product = item_data["product"]
    item_name = product.get("product_name", "Unknown Product")
    categories = product.get("categories_hierarchy", [])
    item_category = categories[0][3:] if categories else "Unknown Category"
    brands = product.get("brands_tags", [])
    item_brand = brands[0] if brands else "Unknown Brand"
    next_id = max((i["id"] for i in inventory), default = 0) + 1
    new_item = {"product_name": item_name, "quantity": item_quantity, "barcode_number": item_barcode, "category": item_category, "brand": item_brand, "id": next_id}
    inventory.append(new_item)
    return jsonify(new_item), 201

