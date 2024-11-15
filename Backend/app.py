from flask import Flask, jsonify, request
from flask_pymongo import PyMongo
from flask_socketio import SocketIO, emit
from config import Config
import models

app = Flask(__name__)
app.config.from_object(Config)

# MongoDB setup
mongo = PyMongo(app)

# WebSocket setup
socketio = SocketIO(app, cors_allowed_origins="*")

@app.route('/inventory', methods=['GET'])
def get_inventory():
    inventory = list(mongo.db.inventory.find())
    return jsonify(inventory)

@app.route('/inventory', methods=['POST'])
def add_inventory():
    item = request.json
    mongo.db.inventory.insert_one(item)
    socketio.emit('inventory_update', item)  # Real-time update
    return jsonify(item), 201

@app.route('/inventory/<id>', methods=['PUT'])
def update_inventory(id):
    item = request.json
    mongo.db.inventory.update_one({"_id": id}, {"$set": item})
    socketio.emit('inventory_update', item)  # Real-time update
    return jsonify(item), 200

if __name__ == '__main__':
    socketio.run(app, debug=True)
