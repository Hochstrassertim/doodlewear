def list_cart_products(cursor, username):
    query = "SELECT * FROM products WHERE username = %s"
    cursor.execute(query, (username,))

    # Fetch all the rows as a list of dictionaries
    columns = [desc[0] for desc in cursor.description]
    data = [dict(zip(columns, row)) for row in cursor.fetchall()]

    return data