
"""
Fruit Store Console Application
Follows PEP8, uses functions, modules-like separation, dictionary storage,
file handling for logs, validation, and menu-driven interaction.
"""

import json
import os
from datetime import datetime

DATA_FILE = "fruit_store_data.json"
LOG_FILE = "transactions.log"


# -------------------- Utility / Persistence --------------------
def load_data():
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r") as f:
                return json.load(f)
        except Exception:
            return {}
    return {}


def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)


def log_transaction(message):
    with open(LOG_FILE, "a") as f:
        f.write(f"{datetime.now()} - {message}\n")


def input_int(prompt):
    while True:
        val = input(prompt)
        if val.isdigit():
            return int(val)
        print("Invalid input. Please enter a valid number.")


def input_float(prompt):
    while True:
        val = input(prompt)
        try:
            return float(val)
        except ValueError:
            print("Invalid input. Please enter a valid number.")


# -------------------- Fruit Manager --------------------
def add_fruit_stock(data):
    print("\nADD FRUIT STOCK")
    name = input("Enter fruit name: ").strip().title()
    qty = input_int("Enter quantity (kg): ")
    price = input_float("Enter price per kg: ")

    if name in data:
        data[name]["qty"] += qty
        data[name]["price"] = price
    else:
        data[name] = {"qty": qty, "price": price}

    save_data(data)
    log_transaction(f"Added/Updated stock: {name}, Qty: {qty}, Price: {price}")
    print("Stock updated successfully.")


def view_fruit_stock(data):
    print("\nVIEW FRUIT STOCK")
    if not data:
        print("No stock available.")
        return

    for fruit, details in data.items():
        print(f"{fruit} -> Qty: {details['qty']} kg, Price: {details['price']}")

    log_transaction("Viewed fruit stock.")


def update_fruit_stock(data):
    print("\nUPDATE FRUIT STOCK")
    name = input("Enter fruit name to update: ").strip().title()

    if name not in data:
        print("Fruit not found.")
        return

    qty = input_int("Enter new quantity (kg): ")
    price = input_float("Enter new price per kg: ")

    data[name] = {"qty": qty, "price": price}
    save_data(data)
    log_transaction(f"Updated stock: {name}, Qty: {qty}, Price: {price}")
    print("Stock updated successfully.")


def manager_menu(data):
    while True:
        print("\nFruit Market Manager")
        print("1) Add Fruit Stock")
        print("2) View Fruit Stock")
        print("3) Update Fruit Stock")
        print("4) Back to Main Menu")

        choice = input("Enter your choice: ")

        if choice == "1":
            add_fruit_stock(data)
        elif choice == "2":
            view_fruit_stock(data)
        elif choice == "3":
            update_fruit_stock(data)
        elif choice == "4":
            break
        else:
            print("Invalid choice. Try again.")


# -------------------- Customer --------------------
def purchase_fruit(data):
    print("\nPURCHASE FRUIT")
    name = input("Enter fruit name: ").strip().title()

    if name not in data:
        print("Fruit not available.")
        return

    qty = input_int("Enter quantity (kg): ")

    if qty > data[name]["qty"]:
        print("Not enough stock available.")
        return

    total = qty * data[name]["price"]
    data[name]["qty"] -= qty

    save_data(data)
    log_transaction(f"Purchased: {name}, Qty: {qty}, Total: {total}")
    print(f"Purchase successful. Total cost: {total}")


def customer_menu(data):
    while True:
        print("\nCustomer Menu")
        print("1) View Fruits")
        print("2) Purchase Fruit")
        print("3) Back to Main Menu")

        choice = input("Enter your choice: ")

        if choice == "1":
            view_fruit_stock(data)
        elif choice == "2":
            purchase_fruit(data)
        elif choice == "3":
            break
        else:
            print("Invalid choice. Try again.")


# -------------------- Main Controller --------------------
def main():
    data = load_data()

    while True:
        print("\nWELCOME TO FRUIT MARKET")
        print("1) Manager")
        print("2) Customer")
        print("3) Exit")

        choice = input("Select your role: ")

        if choice == "1":
            manager_menu(data)
        elif choice == "2":
            customer_menu(data)
        elif choice == "3":
            print("Exiting... Thank you!")
            break
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print("An unexpected error occurred. Returning to menu.")
        log_transaction(f"Error: {str(e)}")
