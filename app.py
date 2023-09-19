from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def root():
    markers = [{
            #'lat': 39,
            #'lon': -77,
            #'popup': 'This is the middle of the map.'
             }]
    return render_template('index.html', markers=markers)


if __name__ == '__main__':
    app.run(host="localhost", port=8080, debug=True)
