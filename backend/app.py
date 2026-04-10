from flask import Flask, request, jsonify
from flask_cors import CORS
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
            password="",
            database="clothing_store"
        )
        return connection
    except mysql.connector.Error as err:
        print(f"Database connection error: {err}")
        return None


@app.route("/")
def home():
    return "THREAD Clothing Store API Running"


# ============================================================
# PRODUCTS
# ============================================================

# Query 1 -- GET /products
@app.route("/products", methods=["GET"])
def get_products():
    connection = get_db_connection()
    if connection is None:
        return jsonify({"error": "Could not connect to database"}), 500
    try:
        cursor = connection.cursor(dictionary=True)
        cursor.execute("""
            SELECT id, name, category, base_price, stock_quantity
            FROM products
            ORDER BY category, name
        """)
        return jsonify(cursor.fetchall()), 200
    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 500
    finally:
        cursor.close()
        connection.close()


# GET /products/<id>
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


# POST /products
@app.route("/products", methods=["POST"])
def add_product():
    data = request.get_json()
    if not data:
        return jsonify({"error": "Request body must be JSON"}), 400

    name           = data.get("name")
    category       = data.get("category", "Uncategorized")
    price          = data.get("base_price")
    stock_quantity = data.get("stock_quantity", 0)

    if not name or price is None:
        return jsonify({"error": "name and base_price are required"}), 400
    if price < 0:
        return jsonify({"error": "base_price cannot be negative"}), 400

    connection = get_db_connection()
    if connection is None:
        return jsonify({"error": "Could not connect to database"}), 500
    try:
        cursor = connection.cursor()
        cursor.execute("""
            INSERT INTO products (name, category, base_price, stock_quantity)
            VALUES (%s, %s, %s, %s)
        """, (name, category, price, stock_quantity))
        connection.commit()
        return jsonify({"message": "Product added", "id": cursor.lastrowid}), 201
    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 500
    finally:
        cursor.close()
        connection.close()


# PUT /products/<id>
@app.route("/products/<int:id>", methods=["PUT"])
def update_product(id):
    data = request.get_json()
    if not data:
        return jsonify({"error": "Request body must be JSON"}), 400

    name           = data.get("name")
    category       = data.get("category")
    price          = data.get("base_price")
    stock_quantity = data.get("stock_quantity")

    if not name or price is None or stock_quantity is None:
        return jsonify({"error": "name, base_price, and stock_quantity are required"}), 400

    connection = get_db_connection()
    if connection is None:
        return jsonify({"error": "Could not connect to database"}), 500
    try:
        cursor = connection.cursor()
        cursor.execute("""
            UPDATE products
            SET name = %s, category = %s, base_price = %s, stock_quantity = %s
            WHERE id = %s
        """, (name, category, price, stock_quantity, id))
        connection.commit()
        if cursor.rowcount == 0:
            return jsonify({"error": "Product not found"}), 404
        return jsonify({"message": "Product updated"}), 200
    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 500
    finally:
        cursor.close()
        connection.close()


# DELETE /products/<id>
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
        return jsonify({"message": "Product deleted"}), 200
    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 500
    finally:
        cursor.close()
        connection.close()


# Query 6 -- GET /products/low-stock  (subquery)
@app.route("/products/low-stock", methods=["GET"])
def get_low_stock():
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


# POST /customers
@app.route("/customers", methods=["POST"])
def add_customer():
    data = request.get_json()
    if not data:
        return jsonify({"error": "Request body must be JSON"}), 400

    first_name = data.get("first_name", "").strip()
    last_name  = data.get("last_name", "").strip()
    email      = data.get("email", "").strip()
    address    = data.get("address", None)
    member     = 1 if data.get("member") else 0

    if not first_name or not last_name or not email:
        return jsonify({"error": "first_name, last_name, and email are required"}), 400

    connection = get_db_connection()
    if connection is None:
        return jsonify({"error": "Could not connect to database"}), 500
    try:
        cursor = connection.cursor()
        cursor.execute("""
            INSERT INTO customers (first_name, last_name, email, address, member)
            VALUES (%s, %s, %s, %s, %s)
        """, (first_name, last_name, email, address, member))
        connection.commit()
        return jsonify({"message": "Customer added", "id": cursor.lastrowid}), 201
    except mysql.connector.IntegrityError:
        return jsonify({"error": "Email already registered"}), 409
    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 500
    finally:
        cursor.close()
        connection.close()


# Query 5 -- GET /customers/stats  (aggregate)
@app.route("/customers/stats", methods=["GET"])
def get_customer_stats():
    connection = get_db_connection()
    if connection is None:
        return jsonify({"error": "Could not connect to database"}), 500
    try:
        cursor = connection.cursor(dictionary=True)
        cursor.execute("""
            SELECT
                c.id,
                CONCAT(c.first_name, ' ', c.last_name) AS customer_name,
                c.email,
                COUNT(DISTINCT o.id)              AS total_orders,
                COALESCE(SUM(o.total_amount), 0)  AS total_spent
            FROM customers c
            LEFT JOIN orders o ON o.customer_id = c.id
            GROUP BY c.id, c.first_name, c.last_name, c.email
            ORDER BY total_spent DESC
        """)
        return jsonify(cursor.fetchall()), 200
    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 500
    finally:
        cursor.close()
        connection.close()


# ============================================================
# ORDERS
# ============================================================

# Query 3 -- GET /orders  (JOIN)
@app.route("/orders", methods=["GET"])
def get_orders():
    connection = get_db_connection()
    if connection is None:
        return jsonify({"error": "Could not connect to database"}), 500
    try:
        cursor = connection.cursor(dictionary=True)
        cursor.execute("""
            SELECT
                o.id            AS order_id,
                CONCAT(c.first_name, ' ', c.last_name) AS customer_name,
                c.email,
                o.order_date,
                o.status,
                o.shipping_address,
                o.total_amount
            FROM orders o
            JOIN customers c ON c.id = o.customer_id
            ORDER BY o.order_date DESC
        """)
        return jsonify(cursor.fetchall()), 200
    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 500
    finally:
        cursor.close()
        connection.close()


# Query 4 -- GET /orders/<id>  (multi-table JOIN)
@app.route("/orders/<int:id>", methods=["GET"])
def get_order_by_id(id):
    connection = get_db_connection()
    if connection is None:
        return jsonify({"error": "Could not connect to database"}), 500
    try:
        cursor = connection.cursor(dictionary=True)
        cursor.execute("""
            SELECT
                o.id            AS order_id,
                o.order_date,
                o.status,
                o.shipping_address,
                o.total_amount,
                c.first_name,
                c.last_name,
                c.email,
                p.name          AS product_name,
                oi.quantity,
                oi.unit_price,
                (oi.quantity * oi.unit_price) AS line_total
            FROM orders o
            JOIN customers   c  ON c.id        = o.customer_id
            JOIN order_items oi ON oi.order_id = o.id
            JOIN products    p  ON p.id        = oi.product_id
            WHERE o.id = %s
        """, (id,))
        rows = cursor.fetchall()
        if not rows:
            return jsonify({"error": "Order not found"}), 404
        return jsonify(rows), 200
    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 500
    finally:
        cursor.close()
        connection.close()


# Query 7 -- GET /orders/summary  (VIEW)
@app.route("/orders/summary", methods=["GET"])
def get_order_summary():
    connection = get_db_connection()
    if connection is None:
        return jsonify({"error": "Could not connect to database"}), 500
    try:
        cursor = connection.cursor(dictionary=True)
        cursor.execute("""
            SELECT order_id, customer_name, customer_email,
                   order_date, status, item_count, calculated_total
            FROM order_summary
            ORDER BY order_date DESC
        """)
        return jsonify(cursor.fetchall()), 200
    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 500
    finally:
        cursor.close()
        connection.close()


# Query 8 -- PUT /orders/<id>/status  (UPDATE)
@app.route("/orders/<int:id>/status", methods=["PUT"])
def update_order_status(id):
    data = request.get_json()
    if not data:
        return jsonify({"error": "Request body must be JSON"}), 400

    status = data.get("status")
    valid_statuses = ("pending", "shipped", "delivered", "cancelled")
    if status not in valid_statuses:
        return jsonify({"error": f"status must be one of {valid_statuses}"}), 400

    connection = get_db_connection()
    if connection is None:
        return jsonify({"error": "Could not connect to database"}), 500
    try:
        cursor = connection.cursor()
        cursor.execute("UPDATE orders SET status = %s WHERE id = %s", (status, id))
        connection.commit()
        if cursor.rowcount == 0:
            return jsonify({"error": "Order not found"}), 404
        return jsonify({"message": "Order status updated"}), 200
    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 500
    finally:
        cursor.close()
        connection.close()


# POST /orders  -- transaction-wrapped: inserts order + all items atomically
# The trigger (trg_update_order_total) fires on each order_items insert
# and keeps orders.total_amount in sync automatically.
@app.route("/orders", methods=["POST"])
def add_order():
    data = request.get_json()
    if not data:
        return jsonify({"error": "Request body must be JSON"}), 400

    customer_id      = data.get("customer_id")
    shipping_address = data.get("shipping_address")
    items            = data.get("items", [])

    if not customer_id or not items:
        return jsonify({"error": "customer_id and items are required"}), 400

    connection = get_db_connection()
    if connection is None:
        return jsonify({"error": "Could not connect to database"}), 500

    try:
        connection.start_transaction()
        cursor = connection.cursor()

        # Insert the order row (total_amount starts at 0; trigger updates it)
        cursor.execute("""
            INSERT INTO orders (customer_id, order_date, status, shipping_address)
            VALUES (%s, CURRENT_DATE, 'pending', %s)
        """, (customer_id, shipping_address))
        order_id = cursor.lastrowid

        # Insert each item -- trigger fires after each INSERT
        for item in items:
            product_id = item.get("product_id")
            quantity   = item.get("quantity")
            unit_price = item.get("unit_price")
            if not product_id or not quantity or unit_price is None:
                raise ValueError("Each item needs product_id, quantity, and unit_price")
            cursor.execute("""
                INSERT INTO order_items (order_id, product_id, quantity, unit_price)
                VALUES (%s, %s, %s, %s)
            """, (order_id, product_id, quantity, unit_price))

        connection.commit()
        return jsonify({"message": "Order created", "order_id": order_id}), 201

    except (mysql.connector.Error, ValueError) as err:
        connection.rollback()
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
