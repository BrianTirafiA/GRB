import psycopg2
from models.Wishlist import Wishlist  # Assuming Wishlist model is defined in models/Wishlist.py

# Function to establish a database connection
def db_conn():
    url = "postgresql://postgres:Irzamudin1@localhost:5432/Library"
    return psycopg2.connect(url)

# Function to add a book to a customer's wishlist
def add_wishlist(Nama_Customer, Nama_Buku, ID_GRB):
    connection = None  # Default value for connection
    try:
        connection = db_conn()
        cursor = connection.cursor()

        # Begin transaction
        cursor.execute('''BEGIN TRANSACTION''')

        # Retrieve ID_Customer based on Nama_Customer
        cursor.execute('''SELECT "ID_Customer" FROM public."Customer" WHERE "Nama_Customer" = %s''', (Nama_Customer,))
        ID_Customer = cursor.fetchone()

        if ID_Customer:
            ID_Customer = ID_Customer[0]  # Extract the ID_Customer from the result
        else:
            raise ValueError("Customer tidak ada")

        # Retrieve BookID based on Nama_Buku
        cursor.execute('''SELECT "ID_Buku" FROM public."Buku" WHERE "Nama_Buku" = %s''', (Nama_Buku,))
        ID_Buku = cursor.fetchone()

        if ID_Buku:
            ID_Buku = ID_Buku[0]  # Extract the BookID from the result
        else:
            raise ValueError("Buku tidak ada")

        # Retrieve ID_GRB based on store_name
        cursor.execute('''SELECT "ID_GRB" FROM public."GRB" WHERE "ID_GRB" = %s''', (ID_GRB,))
        ID_GRB = cursor.fetchone()

        if ID_GRB:
            ID_GRB = ID_GRB[0]  # Extract the ID_GRB from the result
        else:
            raise ValueError("GRB tidak ada")

        # Generate a new WishlistID
        cursor.execute('''SELECT MAX("ID_WIshlist") FROM public."Wishlist"''')
        ID_WIshlist = cursor.fetchone()[0] + 1  # Increment the maximum WishlistID

        # Check if the book is available in the specified store
        cursor.execute('''SELECT * FROM public."Stok" WHERE "ID_Buku" = %s AND "ID_GRB" = %s''', (ID_Buku, ID_GRB))
        Stok = cursor.fetchone()

        if Stok:
            # Insert the book into the customer's wishlist
            cursor.execute('''INSERT INTO public."Wishlist"("ID_WIshlist", "ID_Customer", "ID_Buku", "ID_GRB", "ID_Status") 
                              VALUES (%s, %s, %s, %s, 0);''', (ID_WIshlist, ID_Customer, ID_Buku, ID_GRB))
        else:
            raise ValueError("Buku tidak ada pada GRB")

        # Commit the transaction
        connection.commit()
        return True, None
    except Exception as e:
        if connection:
            connection.rollback()  # Rollback the transaction if an exception occurs
        return False, str(e)
    finally:
        # Close cursor and connection
        if connection:
            cursor.close()
            connection.close()
