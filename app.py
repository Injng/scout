from flask import Flask, render_template, request

app = Flask(__name__)


@app.route('/')
def root():
    loc_data = location()
    if loc_data == None:
        lat = 39
        lon = -77
    else:
        lat = loc_data["lat"]
        lon = loc_data["lon"]
    markers = [{
            'lat': lat,
            'lon': lon,
            'popup': 'This is a marker'
             }]
    return render_template('index.html', markers=markers)

@app.route('/location', methods=['POST'])
def location():
    loc_data = request.get_json()
    try:
        return loc_data
    except:
        return {}

if __name__ == '__main__':
    app.run(host="localhost", port=8080, debug=True)
