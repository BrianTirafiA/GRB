from flask import Flask
from routes.RouteBuku import Buku_bp
from routes.RoutesWishlist import wishlist_bp
from routes.RoutesRating import rating_bp

app = Flask(__name__)
app.register_blueprint(Buku_bp)
app.register_blueprint(wishlist_bp)
app.register_blueprint(rating_bp)