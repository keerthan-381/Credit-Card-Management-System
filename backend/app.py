from flask import Flask, request, jsonify
from flask_cors import CORS
import mysql.connector
from mysql.connector import Error
import bcrypt

app = Flask(__name__)
CORS(app)  # Enable Cross-Origin Resource Sharing


def get_cust(customer_id):
    connection = get_db_connection()

    cursor = connection.cursor()

    cursor.execute("""
        SELECT first_name, email, password_ 
        FROM users 
        WHERE customer_id = %s
    """, (customer_id,))

    customer = cursor.fetchall()

    cursor.close()
    connection.close()

    return customer

def get_test_card(card_number):
    connection = get_db_connection()

    cursor = connection.cursor()

    cursor.execute("""
        SELECT card_holder, credit_limit, status 
        FROM credit_cards 
        WHERE  card_number = %s
    """, (card_number,))

    card = cursor.fetchall()

    cursor.close()
    connection.close()

    return card

# def get_test_transaction(card_number,transaction_id):
#     connection = get_db_connection()

#     cursor = connection.cursor()

#     cursor.execute("""
#         SELECT merchant_name, category, amount, 
#         FROM transactions 
#         WHERE transaction_id = %s and card_number = %s
#     """, (transaction_id,card_number,))

#     tr = cursor.fetchall()

#     cursor.close()
#     connection.close()

#     return tr

# Database connection configuration
def get_db_connection():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Sqlworkbench@123",
            database="credit_card_db"  # Ensure you're using the correct DB name
        )
        if connection.is_connected():
            print("Connected to the database successfully.")
        return connection
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None

# User registration endpoint
@app.route('/register', methods=['POST'])
def register_user():
    try:
        data = request.get_json()
        first_name = data.get("first_name")
        last_name = data.get("last_name")
        email = data.get("email")
        password = data.get("password")
        address = data.get("address")
        user_type = data.get("user_type", "user")  # Default to 'user' if not provided

        # Hash the password
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

        # Connect to DB
        connection = get_db_connection()
        if connection is None:
            return jsonify({"message": "Database connection failed"}), 500

        cursor = connection.cursor()

        # Insert new user into `users` table
        cursor.execute(""" 
            INSERT INTO users (first_name, last_name, email, password_, address_, user_type)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (first_name, last_name, email, hashed_password, address, user_type))

        # Commit the transaction
        connection.commit()

        # Confirm insertion
        print("User inserted successfully.")
        
        cursor.close()
        connection.close()
        return jsonify({"message": "User registered successfully!"}), 201

    except Exception as e:
        print(f"Error during user registration: {e}")
        return jsonify({"message": "Error during user registration"}), 400

# User login endpoint
@app.route('/login', methods=['POST'])
def login_user():
    try:
        data = request.get_json()
        email = data.get("email")
        password = data.get("password")

        # Connect to DB
        connection = get_db_connection()
        if connection is None:
            return jsonify({"message": "Database connection failed"}), 500

        cursor = connection.cursor()

        # Query the user by email
        cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
        user = cursor.fetchone()

        if user is None:
            return jsonify({"message": "User not found", "status": "fail"}), 404

        # Compare hashed passwords
        stored_password = user[4]
        if bcrypt.checkpw(password.encode('utf-8'), stored_password.encode('utf-8')):

            # Fetch customer_id from the credit_cards table
            cursor.execute(""" 
                SELECT customer_id 
                FROM credit_cards 
                WHERE customer_id = %s
                LIMIT 1
            """, (user[0],))  # Assuming user[0] is the customer_id from users table

            customer_id_result = cursor.fetchone()

            if customer_id_result:
                customer_id = customer_id_result[0]
            else:
                customer_id = None

            # Fetch card details for the user
            cursor.execute("""
                SELECT card_number, card_holder, credit_limit, status 
                FROM credit_cards 
                WHERE customer_id = %s
            """, (user[0],))  # Assuming user[0] is the customer_id

            card_details = cursor.fetchall()
            if card_details:
                card_info = card_details[0]
                card_number = card_info[0]

                # Query to get the sum of outstanding amounts for this card
                cursor.execute("""
                    SELECT SUM(outstanding) 
                    FROM transactions 
                    WHERE card_number = %s
                """, (card_number,))
                outstanding_result = cursor.fetchone()

                # If there are transactions, use the sum, otherwise set outstanding to 0
                outstanding_amount = outstanding_result[0] if outstanding_result[0] is not None else 0.0

                card_data = {
                    "card_number": card_info[0],
                    "card_holder": card_info[1],
                    "credit_limit": card_info[2],
                    "status": card_info[3],
                    "outstanding": outstanding_amount  # Add the fetched outstanding amount
                }
            else:
                card_data = None

            return jsonify({
                "message": "Login successful!",
                "status": "success",
                "user": {
                    "first_name": user[1],
                    "last_name": user[2],
                    "email": user[3],
                    "customer_id": customer_id  # Include customer_id here
                },
                "card": card_data
            }), 200
        else:
            return jsonify({"message": "Invalid credentials", "status": "fail"}), 401

    except Exception as e:
        print(f"Error during user login: {e}")
        return jsonify({"message": "Error during user login", "status": "fail"}), 400

@app.route('/add-card', methods=['POST'])
def add_card():
    try:
        data = request.get_json()
        customer_id = data.get("customer_id")
        card_number = data.get("card_number")
        card_holder = data.get("card_holder")
        expiry_date = data.get("expiry_date")
        credit_limit = data.get("credit_limit")

        # Connect to DB
        connection = get_db_connection()
        if connection is None:
            return jsonify({"message": "Database connection failed"}), 500

        cursor = connection.cursor()

        # Insert the new card into the `credit_cards` table
        cursor.execute("""
            INSERT INTO credit_cards (customer_id, card_number, card_holder, expiry_date, credit_limit)
            VALUES (%s, %s, %s, %s, %s)
        """, (customer_id, card_number, card_holder, expiry_date, credit_limit))

        # Commit the transaction
        connection.commit()

        cursor.close()
        connection.close()

        return jsonify({"message": "Card added successfully!", "status": "success"}), 201

    except Exception as e:
        print(f"Error during adding card: {e}")
        return jsonify({"message": "Error adding card", "status": "fail"}), 400



@app.route('/get-cards/<int:customer_id>', methods=['GET'])
def get_cards(customer_id):
    try:
        # Connect to DB
        connection = get_db_connection()
        if connection is None:
            return jsonify({"message": "Database connection failed"}), 500

        cursor = connection.cursor(dictionary=True)

        # Query to fetch card details along with outstanding amounts
        cursor.execute("""
            SELECT 
                c.card_number, 
                c.card_holder, 
                c.credit_limit, 
                c.status, 
                CAST(IFNULL(SUM(t.outstanding), 0) AS DECIMAL(10, 2)) AS outstanding
            FROM credit_cards c
            LEFT JOIN transactions t ON c.card_number = t.card_number
            WHERE c.customer_id = %s
            GROUP BY c.card_number, c.card_holder, c.credit_limit, c.status
        """, (customer_id,))


        cards = cursor.fetchall()
        return jsonify({"cards": cards}), 200

    except Exception as e:
        print(f"Error fetching cards: {e}")
        return jsonify({"message": "Error fetching cards"}), 400
    




@app.route('/get-transactions/<string:card_number>', methods=['GET'])
def get_transactions(card_number):
    try:
        # Connect to DB
        connection = get_db_connection()
        if connection is None:
            return jsonify({"message": "Database connection failed"}), 500

        cursor = connection.cursor(dictionary=True)

        # Query to fetch transaction details for the given card
        cursor.execute("""
            SELECT 
                transaction_id, 
                merchant_name, 
                category, 
                transaction_date, 
                amount, 
                outstanding
            FROM transactions
            WHERE card_number = %s
        """, (card_number,))

        transactions = cursor.fetchall()

        cursor.close()
        connection.close()

        return jsonify({"transactions": transactions}), 200
    except Exception as e:
        print(f"Error fetching transactions: {e}")
        return jsonify({"message": "Error fetching transactions"}), 400











if __name__ == '__main__':
    app.run(debug=True)
