from app import *
def list_products(cursor):
    query = "SELECT * FROM products"
    cursor.execute(query)

    # Fetch all the rows as a list of dictionaries
    columns = [desc[0] for desc in cursor.description]
    data = [dict(zip(columns, row)) for row in cursor.fetchall()]

    return data

def view_single_product(cursor, procuctid):
    query = "SELECT * FROM products WHERE id = %s"
    cursor.execute(query, (procuctid,))

    # Fetch all the rows as a list of dictionaries
    columns = [desc[0] for desc in cursor.description]
    data = [dict(zip(columns, row)) for row in cursor.fetchall()]

    return data