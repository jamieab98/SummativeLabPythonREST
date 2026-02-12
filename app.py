from flask import Flask, jsonify
from inventory_data import inventory

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

view_item(2)