from flask import Blueprint, jsonify, request
from services.Service import add_rating_Service, update_rating_Service

rating_bp = Blueprint('reviews', __name__)

@rating_bp.route('/add_rating', methods=['POST'])
def add_review1():
    data = request.get_json()

    if not data:
        return jsonify({'error': 'Customer name, Book name, and rating is required'})
    
    customer_name = data.get('customer_name')
    book_name = data.get('book_name')
    rating = data.get('rating')
    success, error_msg = add_rating_Service(customer_name, book_name, rating)
    if success:
        return jsonify({'message': 'Review added successfully'}), 200
    else:
        return jsonify({'message': 'Error adding review book', 'error': error_msg}), 500
    
@rating_bp.route('/update_rating', methods=['PUT'])
def update_review1():
    data = request.get_json()

    if not data:
        return jsonify({'error': 'Customer name, Book name, and rating is required'})
    
    customer_name = data.get('customer_name')
    book_name = data.get('book_name')
    rating = data.get('rating')
    success, error_msg = update_rating_Service(customer_name, book_name, rating)
    if success:
        return jsonify({'message': 'Review updated successfully'}), 200
    else:
        return jsonify({'message': 'Error updating review book', 'error': error_msg}), 500
