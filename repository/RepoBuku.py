import psycopg2
from models.Buku import Buku


def db_conn():
    url = "postgresql://postgres:Irzamudin1@localhost:5432/Library"
    return psycopg2.connect(url)

# Function Ambil Semua Buku
def Semua_Buku():
    connection = None  # Default value for connection
    try:
        # Connect
        connection = db_conn()
        cursor = connection.cursor()
        
        # Query semua Buku dari the Buku_View
        cursor.execute('''SELECT * FROM public."Buku"''')
        data = cursor.fetchall()

        # Create object buku dari data
        bukus = [Buku(
            ID_Buku=buku[0],
            Nama_Buku=buku[1],
            PublishYear=buku[2],
            Pages=buku[3],
            ID_Publisher=buku[4],
            ID_Age=buku[5]
        ) for buku in data]

        
        return bukus, None
    except Exception as e:
        return [], str(e)
    finally:
        # Close connection
        if connection:
            cursor.close()
            connection.close()

# Function untuk ambil Buku berdasar author
def Buku_author(author):
    try:
        connection = db_conn()
        cursor = connection.cursor()

        # Query Buku berdasar author
        cursor.execute('''
            SELECT * FROM public."Buku"
            WHERE "ID_Buku" IN (
                SELECT DISTINCT "ID_Buku" 
                FROM public."Author_Book" 
                WHERE "ID_Author" IN (
					SELECT DISTINCT "ID_Author" 
                	FROM public."Author"
					WHERE "Nama_Author" = %s
				)
            );
        ''', (author,))
        data = cursor.fetchall()

        # Create Buku objects from the retrieved data
        bukus = [Buku(
            ID_Buku=buku[0],
            Nama_Buku=buku[1],
            PublishYear=buku[2],
            Pages=buku[3],
            ID_Publisher=buku[4],
            ID_Age=buku[5]
        ) for buku in data]


        if bukus:
            return bukus, None
        else:
            raise ValueError('Buku tidak ada')
    except Exception as e:
        return [], str(e)
    finally:
        # Close connection to database
        if connection:
            cursor.close()
            connection.close()

# Function to delete Buku by name
def delete_Buku(Nama_Buku):
    try: 
        connection = db_conn()
        cursor = connection.cursor()

        # Begin transaction
        cursor.execute('''BEGIN TRANSACTION''')

        # Query to get Buku ID from Buku name
        cursor.execute('''SELECT "ID_Buku" FROM public."Buku" WHERE "Nama_Buku" = %s''', (Nama_Buku,))
        ID_Buku = cursor.fetchone()

        # Check if the Buku exists
        if ID_Buku:
            ID_Buku = ID_Buku[0]

            # Delete related entries from other tables
            cursor.execute('''DELETE FROM public."GRB" WHERE "ID_Buku" = %s''', ((ID_Buku,)))
            cursor.execute('''DELETE FROM public."Genre_Book" WHERE "ID_Buku" = %s''', ((ID_Buku,)))
            cursor.execute('''DELETE FROM public."Buku_Author" WHERE "ID_Buku" = %s''', ((ID_Buku,)))
            cursor.execute('''DELETE FROM public."Wishlist" WHERE "ID_Buku" = %s''', ((ID_Buku,)))
            cursor.execute('''DELETE FROM public."Rating" WHERE "ID_Buku" = %s''', ((ID_Buku,)))
            cursor.execute('''DELETE FROM public."Buku" WHERE "ID_Buku" = %s''', ((ID_Buku,)))
        else:
            raise ValueError('Buku tidak ada')
        
        # Commit the transaction
        connection.commit()
        return True, None
    except Exception as e:
        if connection:
            connection.rollback() # Rollback the transaction if an exception occurs
        return False, str(e)
    finally:
        # Close connection to database
        if connection:
            cursor.close()
            connection.close()