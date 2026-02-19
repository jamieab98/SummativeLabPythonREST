import argparse

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
        print(f'adding item with the barcode: {args.barcode} with a quantity of {args.quantity}.')
    
    if args.command == "view":
        print("now showing all items in the inventory")
    
    if args.command == "update":
        print(f'now updating the quantity of the item with ID: {args.id} to {args.quantity}')
    
    if args.command == "delete":
        print(f'deleting the item with the ID: {args.id}')
    
    if args.command == "search":
        print(f'searching item with the barcode : {args.barcode}')

if __name__ == "__main__":
    main()