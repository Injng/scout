from flask import Flask, render_template, request
import csv
from converter import update_one

app = Flask(__name__,template_folder="templates")

@app.route("/")
def hello():
    return render_template('index.html')

@app.route('/location', methods=['POST'])
def location():
    lat = request.form.get("data")
    lon = request.form.get("data2")
    print("call")
    optimal = update_one(lat, lon, 'wednesday', 'PM Peak (3pm-7pm)', 10)[3]
    print(optimal)
    return str(optimal[0]) + ':' + str(optimal[1])

if __name__ == '__main__':
    app.run(debug=True)
