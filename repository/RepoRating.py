import psycopg2
from models.Rating import Rating  # Assuming Rating model is defined in models/Rating.py


# Function to establish a database connection
def db_conn():
    url = "postgresql://postgres:Irzamudin1@localhost:5432/Library"
    return psycopg2.connect(url)

# Function to add a new review to the database
def add_rating(Nama_Customer, Nama_Buku, rating):
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

        # Retrieve ID_Buku based on Nama_Buku
        cursor.execute('''SELECT "ID_Buku" FROM public."Book" WHERE "Nama_Buku" = %s''', (Nama_Buku,))
        ID_Buku = cursor.fetchone()

        if ID_Buku:
            ID_Buku = ID_Buku[0]  # Extract the ID_Buku from the result
        else:
            raise ValueError("Buku tidak ada")

        # Generate a new ID_Rating
        cursor.execute('''SELECT MAX("ID_Rating") FROM public."Rating"''')
        ID_Rating = cursor.fetchone()[0] + 1  # Increment the maximum ID_Rating

        # Insert the new review into the Rating table
        cursor.execute('''INSERT INTO public."Rating"("ID_Rating", "ID_Customer", "ID_Buku", "Rate") 
                          VALUES (%s, %s, %s, %s, )''', (ID_Rating, ID_Customer, ID_Buku, rating))

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

def update_rating(Nama_Customer, Nama_Buku, rating):
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

        # Retrieve ID_Buku based on Nama_Buku
        cursor.execute('''SELECT "ID_Buku" FROM public."Buku" WHERE "Nama_Buku" = %s''', (Nama_Buku,))
        ID_Buku = cursor.fetchone()

        if ID_Buku:
            ID_Buku = ID_Buku[0]  # Extract the ID_Buku from the result
        else:
            raise ValueError("Buku tidak ada")

         # Check if review exist between the customer and the book
        cursor.execute('''SELECT "ID_Rating" FROM public."Rating" WHERE "ID_Customer" = %s AND "ID_Buku" = %s''', (ID_Customer, ID_Buku))
        review_id = cursor.fetchone()

        if review_id:
            # Update the review
            review_id = review_id[0]
            cursor.execute('''UPDATE public."Rating" 
                          SET "Rate" = %s 
                          WHERE "ID_Rating" = %s''', (rating, review_id))
        else:
            raise ValueError("Rating customer tidak ada")
        
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