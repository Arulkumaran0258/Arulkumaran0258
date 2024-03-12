from flask import Flask, request, render_template

app = Flask(__name__)

# Dummy data for nearby places
places_data = {
    "perundurai": ["Place 1", "Place 2", "Place 3"],
    # Add more places with their nearby locations here
}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_nearby_places', methods=['POST'])
def get_nearby_places():
    location = request.form['location'].lower()
    if location in places_data:
        nearby_places = places_data[location]
    else:
        nearby_places = []

    return render_template('index.html', location=location, nearby_places=nearby_places)

if __name__ == '__main__':
    app.run(debug=True)
