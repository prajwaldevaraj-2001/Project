from flask import Flask, jsonify, request
from flask_socketio import SocketIO, emit
from mongita import MongitaClientDisk
import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

app = Flask(__name__)
app.config['SECRET_KEY'] = 'inventory_secret'
socketio = SocketIO(app, cors_allowed_origins="*")

# Database setup
client = MongitaClientDisk()
db = client['inventory_db']
products_collection = db['products']

# Helper to send email alerts
def send_email_alert(product_name, stock_level):
    email = Mail(
        from_email='your-email@example.com',
        to_emails='admin@example.com',
        subject=f"Stock Alert: {product_name}",
        html_content=f"<strong>{product_name}</strong> stock is critically low at {stock_level}. Please restock."
    )
    try:
        sg = SendGridAPIClient(os.getenv('SENDGRID_API_KEY'))
        response = sg.send(email)
        print(f"Email sent with status code {response.status_code}")
    except Exception as e:
        print(f"Error sending email: {e}")

# API endpoints
@app.route('/products', methods=['GET'])
def get_products():
    products = list(products_collection.find())
    for product in products:
        product['_id'] = str(product['_id'])
    return jsonify(products)

@app.route('/products', methods=['POST'])
def add_product():
    data = request.json
    products_collection.insert_one(data)
    return jsonify({"message": "Product added successfully!"}), 201

@app.route('/products/<product_id>', methods=['PATCH'])
def update_product(product_id):
    data = request.json
    product = products_collection.find_one_and_update(
        {'_id': product_id},
        {'$set': data},
        return_document=True
    )
    if product:
        socketio.emit('update', {"id": str(product['_id']), "stock_level": product['stock_level']})
        if product['stock_level'] < product['reorder_level']:
            send_email_alert(product['name'], product['stock_level'])
        return jsonify({"message": "Product updated!"}), 200
    return jsonify({"error": "Product not found"}), 404

if __name__ == '__main__':
    socketio.run(app, debug=True)
