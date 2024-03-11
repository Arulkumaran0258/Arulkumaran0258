from flask import Flask, render_template, request, redirect, url_for, jsonify
import mysql.connector
import requests
from math import radians, sin, cos, sqrt, atan2

app = Flask(__name__)

# Database connection details
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'Kirup#a1',
    'database': 'epsm1',
    'auth_plugin': 'mysql_native_password'  # Specify the authentication plugin
}

# Function to calculate distance between two coordinates using Haversine formula
def calculate_distance(lat1, lon1, lat2, lon2):
    R = 6371.0
    lat1_rad = radians(lat1)
    lon1_rad = radians(lon1)
    lat2_rad = radians(lat2)
    lon2_rad = radians(lon2)
    dlon = lon2_rad - lon1_rad
    dlat = lat2_rad - lat1_rad
    a = sin(dlat / 2)**2 + cos(lat1_rad) * cos(lat2_rad) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    distance = R * c
    return distance

# Function to find nearby cities
def find_nearby_cities(location):
    osm_api_url = f"https://nominatim.openstreetmap.org/search?format=json&q={location}"
    response = requests.get(osm_api_url)
    cities_data = response.json()
    nearby_cities = [city['display_name'] for city in cities_data]
    return nearby_cities

@app.route('/')
def main_index():
    return render_template('MainIndex.html')

@app.route('/home')
def home():
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM park_owners")
    parking_places = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('home.html', parking_places=parking_places)

@app.route('/userlogin', methods=['GET', 'POST'])
def userlogin():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        select_query = "SELECT * FROM users WHERE username = %s AND password = %s"
        cursor.execute(select_query, (username, password))
        user = cursor.fetchone()
        cursor.close()
        conn.close()
        if user:
            return redirect(url_for('home'))
        else:
            error = "Invalid username or password"
            return render_template('userlogin.html', error=error)
    else:
        return render_template('userlogin.html')

@app.route('/userregistration', methods=['GET', 'POST'])
def userregistration():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        current_password = request.form['current_password']
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        insert_query = "INSERT INTO users (username, email, password, current_password) VALUES (%s, %s, %s, %s)"
        cursor.execute(insert_query, (username, email, password, current_password))
        conn.commit()
        cursor.close()
        conn.close()
        return redirect(url_for('main_index'))
    else:
        return render_template('userregistration.html')

@app.route('/registration', methods=['GET', 'POST'])
def registration():
    if request.method == 'POST':
        parking_name = request.form['parkingName']
        location = request.form['location']
        owner_name = request.form['ownerName']
        contact_number = request.form['contactNumber']
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        insert_query = "INSERT INTO park_owners (parking_slot_name, location, owner_name, contact_number) VALUES (%s, %s, %s, %s)"
        cursor.execute(insert_query, (parking_name, location, owner_name, contact_number))
        conn.commit()
        cursor.close()
        conn.close()
        return redirect(url_for('main_index'))
    else:
        return render_template('registration.html')

@app.route('/parking_slots')
def parking_slots():
    return render_template('parking_slot.html')

@app.route('/find_nearby_cities', methods=['POST'])
def find_nearby_cities_route():
    location = request.json.get('location')
    if location:
        nearby_cities = find_nearby_cities(location)
        matched_places = []
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor(dictionary=True)
        for city in nearby_cities:
            cursor.execute("SELECT * FROM park_owners WHERE location LIKE %s", ('%' + city + '%',))
            matching_places = cursor.fetchall()
            if matching_places:
                for place in matching_places:
                    place['available_in_database'] = True
            matched_places.extend(matching_places)
        cursor.close()
        conn.close()
        return jsonify({'nearbyCities': nearby_cities, 'matchedPlaces': matched_places})
    else:
        return jsonify({'error': 'Location parameter missing'})


@app.route('/about')
def about():
    return render_template('about.html')

if __name__ == '__main__':
    app.run(debug=True)