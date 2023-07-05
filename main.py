import os

from flask import Flask, request, jsonify
import json
import uuid
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# File paths for menu and orders data
MENU_FILE = 'menu.json'
ORDERS_FILE = 'orders.json'

# Read initial menu data from JSON file
with open(MENU_FILE, 'r') as menu_file:
    menu = json.load(menu_file)

# Read initial orders data from JSON file
with open(ORDERS_FILE, 'r') as orders_file:
    orders = json.load(orders_file)

# Routes for managing the menu
@app.route('/menu', methods=['GET'])
def get_menu():
    return jsonify(menu)

@app.route('/menu', methods=['POST'])
def add_dish():
    dish = request.get_json()
    dish['dish_id'] = str(uuid.uuid4())
    print(dish);
    menu.append(dish)
    save_menu()
    return jsonify({"message": "Dish added successfully"})

@app.route('/menu/<dish_id>', methods=['DELETE'])
def remove_dish(dish_id):
    for dish in menu:
        if dish['dish_id'] == dish_id:
            menu.remove(dish)
            save_menu()
            return jsonify({"message": "Dish removed successfully"})
    return jsonify({"message": "Dish not found"})

@app.route('/menu/<dish_id>', methods=['PATCH'])
def update_dish_availability(dish_id):
    availability = request.get_json().get('availability')
    img = request.get_json().get('img')
    name = request.get_json().get('name')
    price = request.get_json().get('price')

    for dish in menu:
        if dish['dish_id'] == dish_id:
            dish['availability'] = availability
            dish['img'] = img
            dish['name'] = name
            dish['price'] = price
            print('updated dish',dish )
            save_menu()
            return jsonify({"message": "Dish availability updated"})
    return jsonify({"message": "Dish not found"})

# Routes for managing orders
@app.route('/orders', methods=['POST'])
def place_order():
    order = request.get_json()
    for dish_id in order['dish_ids']:
        dish = next((dish for dish in menu if dish['dish_id'] == dish_id), None)
        if dish and dish['availability'] == 'yes':
            orders.append({
                'order_id': len(orders) + 1,
                'customer_name': order['customer_name'],
                'dish_id': dish_id,
                'status': 'received'
            })
        else:
            return jsonify({"message": f"Dish {dish_id} is not available"})
    save_orders()
    return jsonify({"message": "Order placed successfully"})

@app.route('/orders/<order_id>', methods=['PATCH'])
def update_order_status(order_id):
    status = request.get_json().get('status')
    for order in orders:
        if order['order_id'] == int(order_id):
            order['status'] = status
            save_orders()
            return jsonify({"message": "Order status updated"})
    return jsonify({"message": "Order not found"})

# Adding chatbot Logic

@app.route('/zappybot', methods=['POST'])


# Helper functions to save menu and orders data to JSON files
def save_menu():
    with open(MENU_FILE, 'w') as menu_file:
        json.dump(menu, menu_file, indent=4)

def save_orders():
    with open(ORDERS_FILE, 'w') as orders_file:
        json.dump(orders, orders_file, indent=4)

# Start the Flask application
if __name__ == '__main__':
    app.run(debug=True)
