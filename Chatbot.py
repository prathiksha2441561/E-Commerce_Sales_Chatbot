from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ecommerce.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Product Model
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    category = db.Column(db.String(50))
    price = db.Column(db.Float)
    stock = db.Column(db.Integer)
    rating = db.Column(db.Float)
    description = db.Column(db.String(200))

# Initialize Database
@app.before_first_request
def create_tables():
    db.create_all()
    # Populate with mock data
    if not Product.query.first():
        mock_data = [
            Product(name="Smartphone", category="Electronics", price=299.99, stock=50, rating=4.5, description="A great smartphone."),
            Product(name="Laptop", category="Electronics", price=999.99, stock=30, rating=4.8, description="High-performance laptop."),
            Product(name="T-shirt", category="Clothing", price=19.99, stock=100, rating=4.2, description="Comfortable cotton t-shirt.")
        ]
        db.session.bulk_save_objects(mock_data)
        db.session.commit()

# Search Endpoint
@app.route('/search', methods=['GET'])
def search_products():
    query = request.args.get('query', '').lower()
    products = Product.query.filter(Product.name.ilike(f'%{query}%')).all()
    if products:
        result = [{"id": p.id, "name": p.name, "price": p.price, "rating": p.rating, "description": p.description} for p in products]
        return jsonify(result)
    return jsonify({"message": "No products found."}), 404

# Run the server
if __name__ == '__main__':
    app.run(debug=True)
