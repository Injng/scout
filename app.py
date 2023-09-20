from flask import Flask, render_template, request
import csv

app = Flask(__name__,template_folder="templates")

@app.route("/")
def hello():
    return render_template('index.html')

@app.route('/location', methods=['POST'])
def location():
    lat = request.form.get("data")
    lon = request.form.get("data2")
    with open('data/ubers.csv', 'w') as file:
        writer = csv.writer(file)
        writer.writerow(["uber_id", "lat", "lon"])
        writer.writerow([1, lat, lon]) 
    return lat + lon

def write_ubers(ubers):
    with open('data/ubers.csv', 'w') as file:
        writer = csv.writer(file)
        writer.writerow(["uber_id","lat", "lon"])
        for i in range(len(ubers)):
            writer.writerow([i, ubers[i]])

if __name__ == '__main__':
    app.run(debug=True)
