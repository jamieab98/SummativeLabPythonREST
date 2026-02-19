import argparse
import requests

URL = "http://127.0.0.1:5000/"
def main():
    parser = argparse.ArgumentParser(description = "Program to help user manage their inventory")
    
    subparsers = parser.add_subparsers(dest = "command", required = True)

    add = subparsers.add_parser("add", help = "Add a new item to the inventory")
    add.add_argument("barcode", type=str)
    add.add_argument("quantity", type=int)

    view = subparsers.add_parser("view", help = "View all items in the inventory")

    update = subparsers.add_parser("update", help = "Update the quantity of a specific item")
    update.add_argument("id", type=int)
    update.add_argument("quantity", type=int)

    delete = subparsers.add_parser("delete", help = "remove an item from the inventory")
    delete.add_argument("id", type=int)

    search = subparsers.add_parser("search", help = "search an item based on it's barcode")
    search.add_argument("barcode", type=str)

    args = parser.parse_args()
    
    if args.command == "add":
        payload = {"barcode":args.barcode, "quantity":args.quantity}
        response = requests.post(f'{URL}/inventory', json=payload)
        data = response.json()
        if response.status_code != 201:
            print(data["message"])
        else:
            print(f'Successfully added {data["product_name"]}')
    
    if args.command == "view":
        response = requests.get(f'{URL}/inventory')
        data = response.json()
        for i in data:
            print(f'ID:{i["id"]} | {i["product"]}: {i["quantity"]}')
    
    if args.command == "update":
        print(f'now updating the quantity of the item with ID: {args.id} to {args.quantity}')
    
    if args.command == "delete":
        print(f'deleting the item with the ID: {args.id}')
    
    if args.command == "search":
        print(f'searching item with the barcode : {args.barcode}')

if __name__ == "__main__":
    main()