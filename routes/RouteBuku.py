from flask import Blueprint, jsonify, request
from services.Service import Semua_Buku_Service, Buku_author_Service, delete_Buku_Service

Buku_bp = Blueprint('Buku', __name__)

@Buku_bp.route('/buku', methods=['GET'])
def Semua_Buku1():
    SBuku, error_msg = Semua_Buku_Service()

    if SBuku:
        SBuku_list = [{
            'ID_Buku': Buku.ID_Buku,
            'Nama_Buku': Buku.Nama_Buku,
            'PublishYear': Buku.PublishYear,
            'Pages': Buku.Pages,
            'publisher_id': Buku.ID_Publisher,
            'age_id': Buku.ID_Age
        } for Buku in SBuku]
        return jsonify({'SBuku': SBuku_list}), 200
    else: 
        return jsonify({'message': 'Failed to get SBuku', 'error': error_msg}), 404

@Buku_bp.route('/buku/author/<author>', methods=['GET'])
def Buku_author1(author):
    SBuku, error_msg = Buku_author_Service(author)

    if SBuku:
        SBuku_list = [{
            'ID_Buku': Buku.ID_Buku,
            'Nama_Buku': Buku.Nama_Buku,
            'PublishYear': Buku.PublishYear,
            'Pages': Buku.Pages,
            'publisher_id': Buku.ID_Publisher,
            'age_id': Buku.ID_Age
        } for Buku in SBuku]
        return jsonify({'SBuku': SBuku_list}), 200
    else:
        return jsonify({'message': 'Failed to get SBuku by author', 'error': error_msg}), 404
    
@Buku_bp.route('/buku/<ID_Buku>', methods=['DELETE'])
def delete_Buku1(ID_Buku):
    success, error_msg = delete_Buku_Service(ID_Buku)
    if success:
        return jsonify({'message': 'Buku deleted successfully'}), 200
    else:
        return jsonify({'message': 'Error deleting Buku', 'error': error_msg}), 500
