from flask import Flask
from inventory_data import inventory

app = Flask(__name__)

@app.route("/")
def default():
    return "Welcome to the inventory!"

@app.route("/inventory")
def view_inventory():
    for item in inventory:
        print(f"Product: {item['product_name']}")
        print(f"Quantity: {item['quantity']}")

view_inventory()