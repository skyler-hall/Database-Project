from flask import Flask, request, jsonify
from flask_cors import CORS
import mysql.connector

app = Flask(__name__)
CORS(app)

def get_db_connection():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="clothing_store"
        )
        return connection
    except mysql.connector.Error as err:
        print(f"Database connection error: {err}")
        return None


@app.route("/")
def home():
    return "Clothing Store App Running"


# 1) GET /products
@app.route("/products", methods=["GET"])
def get_products():
    connection = get_db_connection()
    if connection is None:
        return jsonify({"error": "Could not connect to database"}), 500

    try:
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM products")
        products = cursor.fetchall()
        return jsonify(products), 200

    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 500

    finally:
        cursor.close()
        connection.close()


# 2) GET /products/<id>
@app.route("/products/<int:id>", methods=["GET"])
def get_product_by_id(id):
    connection = get_db_connection()
    if connection is None:
        return jsonify({"error": "Could not connect to database"}), 500

    try:
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM products WHERE id = %s", (id,))
        product = cursor.fetchone()

        if not product:
            return jsonify({"error": "Product not found"}), 404

        return jsonify(product), 200

    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 500

    finally:
        cursor.close()
        connection.close()


# 3) POST /products
@app.route("/products", methods=["POST"])
def add_product():
    data = request.get_json()

    if not data:
        return jsonify({"error": "Request body must be JSON"}), 400

    name = data.get("name")
    price = data.get("price")
    stock_quantity = data.get("stock_quantity")

    if not name or price is None or stock_quantity is None:
        return jsonify({"error": "Name, price, and stock_quantity are required"}), 400

    connection = get_db_connection()
    if connection is None:
        return jsonify({"error": "Could not connect to database"}), 500

    try:
        cursor = connection.cursor()
        query = """
        INSERT INTO products (name, price, stock_quantity)
        VALUES (%s, %s, %s)
        """
        cursor.execute(query, (name, price, stock_quantity))
        connection.commit()

        return jsonify({"message": "Product added successfully"}), 201

    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 500

    finally:
        cursor.close()
        connection.close()


# 4) PUT /products/<id>
@app.route("/products/<int:id>", methods=["PUT"])
def update_product(id):
    data = request.get_json()

    if not data:
        return jsonify({"error": "Request body must be JSON"}), 400

    name = data.get("name")
    price = data.get("price")
    stock_quantity = data.get("stock_quantity")

    if not name or price is None or stock_quantity is None:
        return jsonify({"error": "Name, price, and stock_quantity are required"}), 400

    connection = get_db_connection()
    if connection is None:
        return jsonify({"error": "Could not connect to database"}), 500

    try:
        cursor = connection.cursor()
        query = """
        UPDATE products
        SET name = %s, price = %s, stock_quantity = %s
        WHERE id = %s
        """
        cursor.execute(query, (name, price, stock_quantity, id))
        connection.commit()

        if cursor.rowcount == 0:
            return jsonify({"error": "Product not found"}), 404

        return jsonify({"message": "Product updated successfully"}), 200

    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 500

    finally:
        cursor.close()
        connection.close()


# 5) DELETE /products/<id>
@app.route("/products/<int:id>", methods=["DELETE"])
def delete_product(id):
    connection = get_db_connection()
    if connection is None:
        return jsonify({"error": "Could not connect to database"}), 500

    try:
        cursor = connection.cursor()
        cursor.execute("DELETE FROM products WHERE id = %s", (id,))
        connection.commit()

        if cursor.rowcount == 0:
            return jsonify({"error": "Product not found"}), 404

        return jsonify({"message": "Product deleted successfully"}), 200

    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 500

    finally:
        cursor.close()
        connection.close()


# 6) GET /customers
@app.route("/customers", methods=["GET"])
def get_customers():
    connection = get_db_connection()
    if connection is None:
        return jsonify({"error": "Could not connect to database"}), 500

    try:
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM customers")
        customers = cursor.fetchall()
        return jsonify(customers), 200

    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 500

    finally:
        cursor.close()
        connection.close()


# 7) POST /customers
@app.route("/customers", methods=["POST"])
def add_customer():
    data = request.get_json()

    if not data:
        return jsonify({"error": "Request body must be JSON"}), 400

    first_name = data.get("first_name")
    last_name = data.get("last_name")
    email = data.get("email")

    if not first_name or not last_name or not email:
        return jsonify({"error": "First name, last name, and email are required"}), 400

    connection = get_db_connection()
    if connection is None:
        return jsonify({"error": "Could not connect to database"}), 500

    try:
        cursor = connection.cursor()
        query = """
        INSERT INTO customers (first_name, last_name, email)
        VALUES (%s, %s, %s)
        """
        cursor.execute(query, (first_name, last_name, email))
        connection.commit()

        return jsonify({"message": "Customer added successfully"}), 201

    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 500

    finally:
        cursor.close()
        connection.close()


# 8) GET /orders
@app.route("/orders", methods=["GET"])
def get_orders():
    connection = get_db_connection()
    if connection is None:
        return jsonify({"error": "Could not connect to database"}), 500

    try:
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM orders")
        orders = cursor.fetchall()
        return jsonify(orders), 200

    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 500

    finally:
        cursor.close()
        connection.close()


# 9) GET /orders/<id>
@app.route("/orders/<int:id>", methods=["GET"])
def get_order_by_id(id):
    connection = get_db_connection()
    if connection is None:
        return jsonify({"error": "Could not connect to database"}), 500

    try:
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM orders WHERE id = %s", (id,))
        order = cursor.fetchone()

        if not order:
            return jsonify({"error": "Order not found"}), 404

        return jsonify(order), 200

    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 500

    finally:
        cursor.close()
        connection.close()


if __name__ == "__main__":
    app.run(debug=True)