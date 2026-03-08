from flask import Flask, request, jsonify
import mysql.connector

app = Flask(__name__)

# Database Connection Function
def get_db_connection():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",   # put your mysql password here if you have one
            database="clothing_store"
        )
        return connection
    except mysql.connector.Error as err:
        print(f"Database connection error: {err}")
        return None


# Test Route
@app.route("/")
def home():
    return "Clothing Store App Running"


# GET PRODUCTS
@app.route("/products", methods=["GET"])
def get_products():

    connection = get_db_connection()

    if connection is None:
        return jsonify({"error": "Could not connect to database"}), 500

    try:
        cursor = connection.cursor(dictionary=True)

        query = "SELECT * FROM products"
        cursor.execute(query)

        products = cursor.fetchall()

        return jsonify(products)

    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 500

    finally:
        cursor.close()
        connection.close()


# ADD CUSTOMER
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

        values = (first_name, last_name, email)

        cursor.execute(query, values)

        connection.commit()

        return jsonify({"message": "Customer added successfully"}), 201

    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 500

    finally:
        cursor.close()
        connection.close()


# RUN SERVER
if __name__ == "__main__":
    app.run(debug=True)