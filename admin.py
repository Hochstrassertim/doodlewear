from app import *
def list_products(cursor):
    query = "SELECT * FROM products"
    cursor.execute(query)

    # Fetch all the rows as a list of dictionaries
    columns = [desc[0] for desc in cursor.description]
    data = [dict(zip(columns, row)) for row in cursor.fetchall()]

    return data

def view_single_product(cursor, productid):
    query = "SELECT * FROM products WHERE id = %s"
    cursor.execute(query, (productid,))  # Wrap productid in a tuple

    # Fetch all the rows as a list of dictionaries
    columns = [desc[0] for desc in cursor.description]
    data = [dict(zip(columns, row)) for row in cursor.fetchall()]

    return data
def update_product(cursor, id, name, description, price, available, story, picture, discount):
    update_query = """
        UPDATE products SET name = %s, description = %s, price = %s, available = %s, story = %s, picture = %s, discount = %s WHERE id = %s
    """
    print(name, description, price, available, story, picture, discount)
    cursor.execute(update_query, (name, description, price, available, story, picture, discount, id,))
