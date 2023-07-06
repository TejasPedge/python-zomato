
from dotenv import dotenv_values
env_vars = dotenv_values('.env')
import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from pymongo import MongoClient
import uuid

app = Flask(__name__)
CORS(app)

# MongoDB Atlas connection details
MONGO_URI = env_vars['MONGO_URI']
DB_NAME = 'ZappyAroma'
MENU_COLLECTION = 'menu'
ORDERS_COLLECTION = 'orders'

# MongoDB client
client = MongoClient(MONGO_URI)
db = client[DB_NAME]
menu_collection = db[MENU_COLLECTION]
orders_collection = db[ORDERS_COLLECTION]

# Routes for managing the menu
@app.route('/menu', methods=['GET'])
def get_menu():
    menu = list(menu_collection.find())
    print(menu)
    return jsonify(menu)

@app.route('/menu', methods=['POST'])
def add_dish():
    dish = request.get_json()
    dish['_id'] = str(uuid.uuid4())
    menu_collection.insert_one(dish)
    return jsonify({"message": "Dish added successfully"})

@app.route('/menu/<dish_id>', methods=['DELETE'])
def remove_dish(dish_id):
    try:
        print('id : ',dish_id)
        result = menu_collection.delete_one({'_id': dish_id})

        if result.deleted_count == 1:
            return jsonify({"message": "Dish removed successfully"})
        else:
            return jsonify({"message": "Dish not found"})

    except Exception as e:
        return jsonify({"message": "An error occurred", "error": str(e)})


@app.route('/menu/<dish_id>', methods=['PATCH'])
def update_dish_availability(dish_id):
    try:
        update_data = request.get_json()
        result = menu_collection.update_one({'_id': dish_id}, {'$set': update_data})

        if result.modified_count == 1:
            return jsonify({"message": "Dish availability updated"})
        elif result.matched_count == 1:
            return jsonify({"message": "No changes made to dish availability"})
        else:
            return jsonify({"message": "Dish not found"})

    except Exception as e:
        return jsonify({"message": "An error occurred", "error": str(e)})

# Routes for managing orders
@app.route('/orders', methods=['POST'])
def place_order():
    order = request.get_json()
    for dish_id in order['dish_ids']:
        dish = menu_collection.find_one({'_id': dish_id, 'availability': 'yes'})
        if dish:
            orders_collection.insert_one({
                'order_id': str(uuid.uuid4()),
                'customer_name': order['customer_name'],
                'dish_id': dish_id,
                'status': 'received'
            })
        else:
            return jsonify({"message": f"Dish {dish_id} is not available"})
    return jsonify({"message": "Order placed successfully"})

@app.route('/orders/<order_id>', methods=['PATCH'])
def update_order_status(order_id):
    status = request.get_json().get('status')
    orders_collection.update_one({'order_id': order_id}, {'$set': {'status': status}})
    return jsonify({"message": "Order status updated"})

# Start the Flask application
if __name__ == '__main__':
    app.run(debug=True)


















# from dotenv import dotenv_values
# env_vars = dotenv_values('.env')

# import os
# from flask import Flask, request, jsonify
# from flask_pymongo import PyMongo
# from bson.objectid import ObjectId
# import uuid
# from flask_cors import CORS

# app = Flask(__name__)
# CORS(app)

# # Configure the MongoDB connection
# app.config['MONGO_URI'] = 'mongodb+srv://<username>:<password>@<cluster-url>/<database>?retryWrites=true&w=majority'
# mongo = PyMongo(app)

# # Routes for managing the menu
# @app.route('/menu', methods=['GET'])
# def get_menu():
#     menu = mongo.db.menu.find()
#     return jsonify(list(menu))

# @app.route('/menu', methods=['POST'])
# def add_dish():
#     dish = request.get_json()
#     dish['_id'] = str(uuid.uuid4())
#     mongo.db.menu.insert_one(dish)
#     return jsonify({"message": "Dish added successfully"})

# @app.route('/menu/<dish_id>', methods=['DELETE'])
# def remove_dish(dish_id):
#     result = mongo.db.menu.delete_one({"_id": ObjectId(dish_id)})
#     if result.deleted_count > 0:
#         return jsonify({"message": "Dish removed successfully"})
#     else:
#         return jsonify({"message": "Dish not found"})

# @app.route('/menu/<dish_id>', methods=['PATCH'])
# def update_dish_availability(dish_id):
#     availability = request.get_json().get('availability')
#     img = request.get_json().get('img')
#     name = request.get_json().get('name')
#     price = request.get_json().get('price')

#     result = mongo.db.menu.update_one(
#         {"_id": ObjectId(dish_id)},
#         {"$set": {
#             "availability": availability,
#             "img": img,
#             "name": name,
#             "price": price
#         }}
#     )

#     if result.modified_count > 0:
#         return jsonify({"message": "Dish availability updated"})
#     else:
#         return jsonify({"message": "Dish not found"})

# # Routes for managing orders
# @app.route('/orders', methods=['POST'])
# def place_order():
#     order = request.get_json()
#     for dish_id in order['dish_ids']:
#         dish = mongo.db.menu.find_one({"_id": ObjectId(dish_id)})
#         if dish and dish['availability'] == 'yes':
#             mongo.db.orders.insert_one({
#                 'order_id': str(uuid.uuid4()),
#                 'customer_name': order['customer_name'],
#                 'dish_id': dish_id,
#                 'status': 'received'
#             })
#         else:
#             return jsonify({"message": f"Dish {dish_id} is not available"})
#     return jsonify({"message": "Order placed successfully"})

# @app.route('/orders/<order_id>', methods=['PATCH'])
# def update_order_status(order_id):
#     status = request.get_json().get('status')
#     result = mongo.db.orders.update_one(
#         {"order_id": order_id},
#         {"$set": {"status": status}}
#     )
#     if result.modified_count > 0:
#         return jsonify({"message": "Order status updated"})
#     else:
#         return jsonify({"message": "Order not found"})

# # Start the Flask application
# if __name__ == '__main__':
#     app.run(debug=True)












































# # import os

# # from flask import Flask, request, jsonify
# # import json
# # import uuid
# # from flask_cors import CORS

# # app = Flask(__name__)
# # CORS(app)

# # # File paths for menu and orders data
# # MENU_FILE = 'menu.json'
# # ORDERS_FILE = 'orders.json'

# # # Read initial menu data from JSON file
# # with open(MENU_FILE, 'r') as menu_file:
# #     menu = json.load(menu_file)

# # # Read initial orders data from JSON file
# # with open(ORDERS_FILE, 'r') as orders_file:
# #     orders = json.load(orders_file)

# # # Routes for managing the menu
# # @app.route('/menu', methods=['GET'])
# # def get_menu():
# #     return jsonify(menu)

# # @app.route('/menu', methods=['POST'])
# # def add_dish():
# #     dish = request.get_json()
# #     dish['dish_id'] = str(uuid.uuid4())
# #     print(dish);
# #     menu.append(dish)
# #     save_menu()
# #     return jsonify({"message": "Dish added successfully"})

# # @app.route('/menu/<dish_id>', methods=['DELETE'])
# # def remove_dish(dish_id):
# #     for dish in menu:
# #         if dish['dish_id'] == dish_id:
# #             menu.remove(dish)
# #             save_menu()
# #             return jsonify({"message": "Dish removed successfully"})
# #     return jsonify({"message": "Dish not found"})

# # @app.route('/menu/<dish_id>', methods=['PATCH'])
# # def update_dish_availability(dish_id):
# #     availability = request.get_json().get('availability')
# #     img = request.get_json().get('img')
# #     name = request.get_json().get('name')
# #     price = request.get_json().get('price')

# #     for dish in menu:
# #         if dish['dish_id'] == dish_id:
# #             dish['availability'] = availability
# #             dish['img'] = img
# #             dish['name'] = name
# #             dish['price'] = price
# #             print('updated dish',dish )
# #             save_menu()
# #             return jsonify({"message": "Dish availability updated"})
# #     return jsonify({"message": "Dish not found"})

# # # Routes for managing orders
# # @app.route('/orders', methods=['POST'])
# # def place_order():
# #     order = request.get_json()
# #     for dish_id in order['dish_ids']:
# #         dish = next((dish for dish in menu if dish['dish_id'] == dish_id), None)
# #         if dish and dish['availability'] == 'yes':
# #             orders.append({
# #                 'order_id': len(orders) + 1,
# #                 'customer_name': order['customer_name'],
# #                 'dish_id': dish_id,
# #                 'status': 'received'
# #             })
# #         else:
# #             return jsonify({"message": f"Dish {dish_id} is not available"})
# #     save_orders()
# #     return jsonify({"message": "Order placed successfully"})

# # @app.route('/orders/<order_id>', methods=['PATCH'])
# # def update_order_status(order_id):
# #     status = request.get_json().get('status')
# #     for order in orders:
# #         if order['order_id'] == int(order_id):
# #             order['status'] = status
# #             save_orders()
# #             return jsonify({"message": "Order status updated"})
# #     return jsonify({"message": "Order not found"})

# # # Adding chatbot Logic

# # @app.route('/zappybot', methods=['POST'])


# # # Helper functions to save menu and orders data to JSON files
# # def save_menu():
# #     with open(MENU_FILE, 'w') as menu_file:
# #         json.dump(menu, menu_file, indent=4)

# # def save_orders():
# #     with open(ORDERS_FILE, 'w') as orders_file:
# #         json.dump(orders, orders_file, indent=4)

# # # Start the Flask application
# # if __name__ == '__main__':
# #     app.run(debug=True)
