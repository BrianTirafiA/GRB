from flask import Blueprint, jsonify, request
from services.Service import add_wishlist_Service

wishlist_bp = Blueprint('wishlist', __name__)

@wishlist_bp.route('/add_wishlist', methods=['POST'])
def add_wishlist1():
    data = request.get_json()

    if not data:
        return jsonify({'error': 'Customer name, Book name, and Store name is required'})
    
    customer_name = data.get('Nama_Customer')
    book_name = data.get('Nama_Buku')
    store_id = data.get('ID_GRB')
    success, error_msg = add_wishlist_Service(customer_name, book_name, store_id)
    if success:
        return jsonify({'message': 'Wishlist added successfully'}), 200
    else:
        return jsonify({'message': 'Error adding wishlist book', 'error': error_msg}), 500