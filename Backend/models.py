from pymongo import MongoClient
from bson.objectid import ObjectId

client = MongoClient('mongodb://localhost:27017/')
db = client['inventory_db']

def add_item(name, stock_level, reorder_level):
    item = {
        'name': name,
        'stock_level': stock_level,
        'reorder_level': reorder_level
    }
    db.inventory.insert_one(item)
