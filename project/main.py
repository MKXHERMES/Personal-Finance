from flask import Flask, render_template, url_for, request, session, redirect, jsonify
from flask_mysqldb import MySQL
import MySQLdb.cursors, re, hashlib
from werkzeug.security import generate_password_hash, check_password_hash
app = Flask(__name__)
app.secret_key = 'ACMirage'

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'KJIT@!2024it'
app.config['MYSQL_DB'] = 'finance'

mysql = MySQL(app)




@app.route("/")
@app.route("/login", methods=["GET", "POST"])
def login():
    msg = ''
    if request.method == "POST" and "username" in request.form and "password" in request.form:
        username = request.form["username"]
        password = request.form["password"]

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("SELECT * FROM accounts WHERE username = %s", (username,))
        account = cursor.fetchone()
        print(f"Account fetched for {username}: {account}")  # Debugging

        # Clear any existing session
        session.clear()
        print(f"Session after clearing: {session}")  # Debugging

        if account is None:
            print(f"No account found for username: {username}. Stopping login.")  # Debugging
            return render_template("login.html", msg='Incorrect username or password!')

        # Validate password
        print(f"Validating password for user {username}.")  # Debugging
        is_password_valid = check_password_hash(account["password"], password)
        print(f"Password validation result for {username}: {is_password_valid}")  # Debugging

        if is_password_valid:
            session["loggedin"] = True
            session["customer_id"] = account["customer_id"]
            session["username"] = account["username"]
            print(f"User {username} logged in successfully.")  # Debugging
            return redirect(url_for("home"))
        else:
            print("Password validation failed.")  # Debugging
            msg = 'Incorrect username or password!'

    print("Rendering login page.")  # Debugging
    return render_template("login.html", msg=msg)









@app.route("/logout")
def logout():
    session.pop("loggedin", None)
    session.pop("customer_id", None)
    session.pop("username", None)
    return redirect(url_for("login"))

@app.route("/income", methods=["GET", "POST"])
def income():
    if 'loggedin' not in session:
        return redirect(url_for('login'))

    customer_id = session.get('customer_id')
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

    if request.method == "POST":
        income_type = request.form.get('incomeType')

        if income_type == "Deposit":
            deposit_type = request.form.get('depositType')
            dep_amount = request.form.get('depAmount')
            start_date = request.form.get('startDate')
            maturity_date = request.form.get('maturityDate')

            if not all([deposit_type, dep_amount, start_date, maturity_date]):
                return jsonify({"success": False, "message": "All Deposit fields are required."})

            cursor.execute(
                "INSERT INTO deposit (deposit_type, dep_amount, start_date, maturity_date, customer_id) VALUES (%s, %s, %s, %s, %s)",
                (deposit_type, dep_amount, start_date, maturity_date, customer_id)
            )

        elif income_type == "SIP":
            sip_amount = request.form.get('sipAmount')
            sip_date = request.form.get('sipDate')
            fund_name = request.form.get('fundName')

            if not all([sip_amount, sip_date, fund_name]):
                return jsonify({"success": False, "message": "All SIP fields are required."})

            cursor.execute(
                "INSERT INTO sip (sip_amount, sip_date, fund_name, customer_id) VALUES (%s, %s, %s, %s)",
                (sip_amount, sip_date, fund_name, customer_id)
            )

        elif income_type == "Custom":
            custom_amount = request.form.get('customAmount')
            custom_category = request.form.get('customCategory')
            custom_date = request.form.get('customDate')

            print(f"Custom Amount: {custom_amount}")
            print(f"Custom Category: {custom_category}")
            print(f"Custom Date: {custom_date }")

            if not all([custom_amount, custom_category, custom_date]):
                return jsonify({"success": False, "message": "All Custom fields are required."})

            cursor.execute(
                "INSERT INTO savings (amount, description, custom_date, customer_id) VALUES (%s, %s, %s, %s)",
                (custom_amount, custom_category, custom_date, customer_id)
            )

        else:
            return jsonify({"success": False, "message": "Invalid income type."})

        mysql.connection.commit()
        return jsonify({"success": True})

    # Fetch all incomes for display
    cursor.execute(
        'SELECT id, "Deposit" as income_type, dep_amount as amount, start_date as date, deposit_type as details FROM deposit WHERE customer_id = %s',
        (customer_id,)
    )
    deposits = cursor.fetchall()

    cursor.execute(
        'SELECT id, "SIP" as income_type, sip_amount as amount, sip_date as date, fund_name as details FROM sip WHERE customer_id = %s',
        (customer_id,)
    )
    sips = cursor.fetchall()

    cursor.execute(
        'SELECT id, "Custom" as income_type, amount as amount, custom_date as date, description as details FROM savings WHERE customer_id = %s',
        (customer_id,)
    )
    custom_incomes = cursor.fetchall()

    # Combine all incomes and assign a unique ID
    incomes = []
    for idx, income in enumerate(deposits + sips + custom_incomes, start=1):
        income_dict = dict(income)  # Convert tuple to a dictionary
        income_dict['unique_id'] = idx  # Add unique ID
        incomes.append(income_dict)

    return render_template('income.html', incomes=incomes)


@app.route("/dashboard")
def home():
    if 'loggedin' not in session:
        return redirect(url_for('login'))
    customer_id = session.get('customer_id')
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

    # Calculate total income
    cursor.execute("SELECT SUM(dep_amount) AS total_deposit FROM deposit WHERE customer_id = %s", (customer_id,))
    total_deposit = cursor.fetchone()['total_deposit'] or 0

    cursor.execute("SELECT SUM(sip_amount) AS total_sip FROM sip WHERE customer_id = %s", (customer_id,))
    total_sip = cursor.fetchone()['total_sip'] or 0

    cursor.execute("SELECT SUM(amount) AS total_custom FROM savings WHERE customer_id = %s", (customer_id,))
    total_custom = cursor.fetchone()['total_custom'] or 0

    total_income = total_deposit + total_sip + total_custom

    return render_template("index.html", total_income=total_income)


@app.route("/register", methods=["GET", "POST"])
def register():
    msg = ''
    if request.method == 'POST':
        if 'username' in request.form and 'password' in request.form and'email' in request.form:
            username = request.form['username']
            password = request.form['password']
            email = request.form['email']

            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('SELECT * FROM accounts WHERE username = % s', (username,))
            account = cursor.fetchone()
            if account:
                msg = 'Account already exists !'
            elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
                msg = 'Invalid email address !'
            elif not re.match(r'[A-Za-z0-9]+', username):
                msg = 'name must contain only characters and numbers !'
            else:
                hashed_password = generate_password_hash(password)
                cursor.execute('INSERT INTO accounts VALUES \
                (NULL, % s, % s, % s)',
                       (username, hashed_password, email,))
                mysql.connection.commit()
                msg = 'You have successfully registered! '

    return render_template('register.html', msg=msg)

@app.route("/expense", methods=["GET", "POST"])
def expense():
    if 'loggedin' not in session:
        return redirect(url_for('login'))

    customer_id = session.get('customer_id')
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

    if request.method == "POST":
        action = request.form.get('action')  # Determine the action: add_category or add_expense

        # Add Category
        if action == "add_category":
            category_name = request.form.get('category_name')
            budget = request.form.get('budget')

            if not category_name:
                return jsonify({"success": False, "message": "Category name is required."})

            try:
                cursor.execute(
                    "INSERT INTO category (name, budget, customer_id) VALUES (%s, %s, %s)",
                    (category_name, budget, customer_id)
                )
                mysql.connection.commit()
                return jsonify({"success": True, "message": "Category added successfully."})
            except Exception as e:
                print(f"Error adding category: {e}")
                return jsonify({"success": False, "message": "Category already exists or invalid data."})

        # Add Expense
        elif action == "add_expense":
            amount = request.form.get('amount')
            description = request.form.get('description')
            category_id = request.form.get('category_id')
            expense_date = request.form.get('expense_date')

            if not all([amount, category_id, expense_date]):
                return jsonify({"success": False, "message": "All fields are required."})

            try:
                # Check if budget is exceeded
                cursor.execute(
                    "SELECT budget, (SELECT IFNULL(SUM(amount), 0) FROM expense WHERE category_id = %s AND customer_id = %s) AS total_expense "
                    "FROM category WHERE id = %s AND customer_id = %s",
                    (category_id, customer_id, category_id, customer_id)
                )
                category = cursor.fetchone()
                if category and category['budget'] is not None:
                    if category['total_expense'] + float(amount) > category['budget']:
                        return jsonify({"success": False, "message": "Budget exceeded for this category."})

                # Add expense
                cursor.execute(
                    "INSERT INTO expense (amount, description, category_id, expense_date, customer_id) VALUES (%s, %s, %s, %s, %s)",
                    (amount, description, category_id, expense_date, customer_id)
                )
                mysql.connection.commit()
                return jsonify({"success": True, "message": "Expense added successfully."})
            except Exception as e:
                print(f"Error adding expense: {e}")
                return jsonify({"success": False, "message": "Failed to add expense."})

    # Fetch categories and expenses for display
    cursor.execute("SELECT * FROM category WHERE customer_id = %s", (customer_id,))
    categories = cursor.fetchall()

    cursor.execute(
        "SELECT expense.id, expense.amount, expense.description, expense.expense_date, category.name AS category_name "
        "FROM expense INNER JOIN category ON expense.category_id = category.id "
        "WHERE expense.customer_id = %s", (customer_id,)
    )
    expenses = cursor.fetchall()

    return render_template("expense.html", categories=categories, expenses=expenses)

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)

    with app.app_context():
        try:
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute("SELECT 1")  # Simple query to test connection
            print("Connected to MySQL successfully.")
        except Exception as e:
            print(f"Error connecting to MySQL: {e}")