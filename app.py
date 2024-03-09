import os
from flask import Flask, jsonify
from flaskext.mysql import MySQL

app = Flask(__name__)

# Initialize MySQL
mysql = MySQL()

# Get database credentials from environment variables or use defaults
mysql_database_host = os.environ.get('MYSQL_DATABASE_HOST', 'localhost')
mysql_database_user = os.environ.get('MYSQL_DATABASE_USER', 'db_user')
mysql_database_password = os.environ.get('MYSQL_DATABASE_PASSWORD', 'Passw0rd')
mysql_database_db = os.environ.get('MYSQL_DATABASE_DB', 'employee_db')

# MySQL configurations
app.config['MYSQL_DATABASE_USER'] = mysql_database_user
app.config['MYSQL_DATABASE_PASSWORD'] = mysql_database_password
app.config['MYSQL_DATABASE_DB'] = mysql_database_db
app.config['MYSQL_DATABASE_HOST'] = mysql_database_host

mysql.init_app(app)

@app.route("/")
def index():
    return "Welcome to the Employee Management System!"

@app.route('/health')
def health_check():
    try:
        conn = mysql.connect()
        conn.ping(reconnect=True)  # Check if connection is alive and reconnect if not
        return jsonify(status="ok"), 200
    except Exception as e:
        return jsonify(error=str(e)), 500
    finally:
        conn.close()

@app.route('/employees', methods=['GET'])
def get_employees():
    try:
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM employees")
        rows = cursor.fetchall()
        employees = [{'id': row[0], 'name': row[1], 'position': row[2]} for row in rows]
        return jsonify(employees), 200
    except Exception as e:
        return jsonify(error=str(e)), 500
    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    app.run(debug=True)
