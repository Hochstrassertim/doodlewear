from flask import Flask, request, render_template, redirect, session, jsonify, url_for
from flask_session import Session
from manage_account import *
from admin import *
from socket import *
from psycopg2 import *

server_hostname = "srv-cn5lbkgl5elc73e7hus0-hibernate-689d6995f9-v54tm"

app = Flask(__name__)

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)



@app.route('/')
def hello_world():
    return render_template("index.html")

@app.route('/about')
def about():
    return render_template("about.html")

@app.route('/color')
def color():
    return render_template("color.html")

@app.route('/shop')
def shop():
    return render_template("shop.html")

@app.route('/story')
def story():
    return render_template("story.html")

@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        connection = connect_to_database()
        cursor = create_cursor(connection)
        user_info_list = get_user_info(cursor, username)
        cursor.close()
        connection.close()
        if user_info_list:
            for user_info in user_info_list:
                print("User Info:", user_info)  # Print user information for debugging
                if password == user_info['password']:
                    session["name"] = username
                    session['role'] = user_info['role']
                    return redirect("/profile")
            response_data = {}
            return render_template("profile/index.html", response_data=response_data)
        response_data = {'message': 'Invalid username or password'}
        return render_template("profile/index.html", response_data=response_data)
    elif request.method == "GET":
        message = request.args.get("message", default="", type=str)
        response_data = {'message': message}
        return render_template("profile/index.html", response_data=response_data)

@app.route("/register", methods=["POST", "GET"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        first_name = request.form.get("first_name")
        last_name = request.form.get("last_name")
        email = request.form.get("email")
        phone = request.form.get("phone")
        street_house_number = request.form.get("street")
        city = request.form.get("city")
        postal_code = request.form.get("postal_code")
        password = request.form.get("password")
        birth_date = request.form.get("birth_date")

        address = street_house_number.split(" ")
        street = address[0]
        house_number = address[1]

        try:
            connection = connect_to_database()
            cursor = create_cursor(connection)

            # Call the register_user function with case-insensitive username
            register_user(cursor, username, first_name, last_name, email, phone, street, house_number, city,
                          postal_code, 'switzerland', password, birth_date)
            connection.commit()
            cursor.close()
            connection.close()

            # Set the session for the newly registered user
            session["name"] = username

            response_data = {'success': True, 'message': 'Registration successful. You will be redirected in a few seconds.'}
            return render_template("profile/login_redirect.html", response_data=response_data)

        except Exception as e:
            return jsonify({'success': False, 'message': 'Error registering user: {}'.format(str(e))})

        return render_template("profile/index.html")

@app.route("/profile")
def profile():
    if not session.get("name"):
        return redirect("/login")
    response_data = {'username': session["name"]}
    return render_template('profile/profile.html', response_data=response_data)

@app.route("/profile/settings")
def settings():
    if not session.get("name"):
        return redirect("/login")
    response_data = {'username': session["name"]}
    return render_template('profile/settings.html', response_data=response_data)

@app.route("/profile/settings/change_password", methods=['GET', 'POST'])
def change_password_route():
    if not session.get("name"):
        return redirect("/login")

    if request.method == "POST":
        old_password = request.form.get("old_password")
        new_password = request.form.get('new_password')
        confirm_password = request.form.get('confirm_password')
        if new_password == confirm_password:
            if new_password != old_password:
                conn = connect_to_database()
                cursor = create_cursor(conn)
                change_password(cursor, session["name"], old_password, new_password)
                conn.commit()
                cursor.close()
                conn.close()
        session["name"] = None
        response_data = {'message': 'Password changed successfully. Please login again.'}
        return render_template('profile/index.html', response_data=response_data)
    else:
        response_data = {'message': ''}
        return render_template('profile/index.html', response_data=response_data)

@app.route("/profile/settings/change_username", methods=['GET', 'POST'])
def change_username_route():
    if not session.get("name"):
        return redirect("/login")

    if request.method == "POST":
        username = request.form.get('new_username')
        conn = connect_to_database()
        cursor = create_cursor(conn)
        change_username(cursor, session["name"], username)
        conn.commit()
        cursor.close()
        conn.close()
        session["name"] = None

    return redirect("/profile/settings")

@app.route("/profile/settings/change_address", methods=['GET', 'POST'])
def change_address_route():
    if not session.get("name"):
        return redirect("/login")

    if request.method == "POST":
        street = request.form.get('street')
        house_number = request.form.get('house_number')
        postal_code = request.form.get('postal_code')
        city = request.form.get('city')
        country = request.form.get('country')
        conn = connect_to_database()
        cursor = create_cursor(conn)
        change_address(cursor, session["name"], street, house_number, postal_code, city, country)
        conn.commit()
        cursor.close()
        conn.close()

    return redirect("/profile/settings")

@app.route("/profile/settings/delete_account", methods=['GET'])
def delete_account_route():
    if not session.get("name"):
        return redirect("/login")

    return render_template('profile/confirm_delete.html')

@app.route("/logout")
def logout():
    session["name"] = None
    return redirect("/login")

@app.route("/profile/settings/delete_account/confirm", methods=['GET'])
def delete_account_confirm_route():
    if not session.get("name"):
        return redirect("/login")
    conn = connect_to_database()
    cursor = create_cursor(conn)
    delete_user(cursor, session["name"])
    conn.commit()
    cursor.close()
    conn.close()
    session["name"] = None
    return redirect("/")

@app.route("/admin")
def admin_route():

    if not session.get("role") == "admin":
        if not session.get("name"):
            return redirect(url_for('login', message="Please login to continue"))
        return redirect(url_for('login', message="You do not have permission to perform this action"))
    return render_template("profile/admin/index.html", response_data={})

@app.route('/admin/view_products')
def view_products():
    conn = connect_to_database()
    cursor = conn.cursor()
    data = list_products(cursor)
    cursor.close()
    conn.close()
    return render_template('profile/admin/view_products.html', data=data, response_data={'username': session.get('name')})

@app.route('/admin/edit_product', methods=['GET'])
def edit_product():
    productId = int(request.args.get("productId"))
    conn = connect_to_database()
    cursor = conn.cursor()
    data = view_single_product(cursor, productId)
    cursor.close()
    conn.close()
    return render_template('profile/admin/edit_product.html', data=data, response_data={'username': session.get('name')})


@app.route('/admin/edit_product/save', methods=['POST'])
def save_edit_product():
    try:
        data = request.get_json()
        productId = int(data.get("productId"))
        name = data.get("name")
        description = data.get('description')
        price = float(data.get('price'))
        available = int(data.get('available'))
        story = data.get('story')
        picture = data.get('picture')
        discount = data.get('discount')

        conn = connect_to_database()
        cursor = conn.cursor()
        update_product(cursor, productId, name, description, price, available, story, picture, discount)
        data = view_single_product(cursor, productId)
        conn.commit()
        cursor.close()
        conn.close()

        return jsonify({'success': True, 'message': 'Product updated successfully', 'data': data})

    except Exception as e:
        return jsonify({'success': False, 'message': f'Error updating product: {str(e)}'})


@app.route('/shirts/productpage', methods=['GET'])
def productpage():
    product_id = request.args.get("productid", default=0, type=int)
    print(product_id)
    return render_template('shirts/productpage.html')

if __name__ == '__main__':
    app.run(debug=True)
