from repository.RepoBuku import Semua_Buku, Buku_author, delete_Buku
from repository.RepoWishlist import add_wishlist
from repository.RepoRating import add_rating, update_rating

def Semua_Buku_Service():
    return Semua_Buku()

def Buku_author_Service(author):
    return Buku_author(author)

def delete_Buku_Service(Nama_Buku):
    return delete_Buku(Nama_Buku)

def add_wishlist_Service(Nama_Customer, Nama_Buku, ID_GRB):
    return add_wishlist(Nama_Customer, Nama_Buku, ID_GRB)

def add_rating_Service(Nama_Customer, Nama_Buku, rating):
    return add_rating(Nama_Customer, Nama_Buku, rating)

def update_rating_Service(Nama_Customer, Nama_Buku, rating):
    return update_rating(Nama_Customer, Nama_Buku, rating)