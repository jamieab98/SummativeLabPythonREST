from flask import Flask, jsonify, request

from inventory_data import inventory
from api_service import fetchAPIData

app = Flask(__name__)

@app.route("/")
def default():
    return "Welcome to the inventory!"

#GET all items
@app.route("/inventory")
def view_inventory():
    response = []
    for item in inventory:
        response.append({"product": item['product_name'], "quantity": item['quantity']})
        #print(f"Product: {item['product_name']}")
        #print(f"Quantity: {item['quantity']}")
    return jsonify(response), 200

#GET specific item
@app.route("/inventory/<int:id>")
def view_item(id):
    item = next((i for i in inventory if i['id'] == id), None)
    if item == None:
        return jsonify({"message":"item not found"}), 404
    #print(item)
    return jsonify(item), 200

#POST new item
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
    #print(new_item)
    return jsonify(new_item), 201

#PATCH update item
@app.route("/inventory/<int:id>", methods = ["PATCH"])
def update_item(id):
    item = request.get_json()
    if not item:
        return jsonify({"message":"item not found in the inventory"}), 400
    if id not in [i["id"] for i in inventory]:
        return jsonify({"message":"item not found in inventory"}), 404
    item_new_quantity = item.get("updated_quantity")
    updated_item = next((i for i in inventory if i["id"] == id), None)
    if updated_item == None:
        return jsonify({"message": "item not found in the inventory"}), 404
    updated_item["quantity"] = item_new_quantity
    return jsonify({"message":"successfully updated the inventory"}), 200

#DELETE item
@app.route("/inventory/<int:id>", methods = ["DELETE"])
def delete_item(id):
    if id not in [i["id"] for i in inventory]:
        return jsonify({"message":"item not found in inventory"}), 404
    inventory[:] = [i for i in inventory if i["id"] != id]
    #print(inventory)
    return jsonify({"message":"successfully deleted item from inventory"})

