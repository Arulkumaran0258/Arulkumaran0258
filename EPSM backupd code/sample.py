from flask import Flask, render_template, request, redirect, url_for
import mysql.connector

app = Flask(__name__)

# Database connection details
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'Kirup#a1',
    'database': 'epsm1'
}

@app.route('/')
def main_index():
    return render_template('MainIndex.html')

@app.route('/userlogin', methods=['GET', 'POST'])
def userlogin():
    if request.method == 'POST':
        # Handle login form submission
        username = request.form['username']
        password = request.form['password']
        # Validate username and password against database records
        # Implement your logic here
        return redirect(url_for('main_index'))
    else:
        return render_template('userlogin.html')

@app.route('/userregistration', methods=['GET', 'POST'])
def userregistration():
    if request.method == 'POST':
        # Handle registration form submission
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        current_password = request.form['current_password']  # Add this line
        # Insert data into the database
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        insert_query = "INSERT INTO users (username, email, password, current_password) VALUES (%s, %s, %s, %s)"
        cursor.execute(insert_query, (username, email, password, current_password))
        conn.commit()
        cursor.close()
        conn.close()
        return redirect(url_for('main_index'))  # Change 'MainIndex' to 'main_index'
    else:
        return render_template('userregistration.html')

if __name__ == '__main__':
    app.run(debug=True)
