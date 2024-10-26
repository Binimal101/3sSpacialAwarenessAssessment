from flask import Flask, jsonify, render_template, request, url_for
from flask_cors import CORS
# flask app
app = Flask(__name__)
CORS(app)
#app route
@app.route('/')
def home():
    return render_template('home.html'); #make dynamic later

@app.route('/regular')
def regular():
    return render_template('regular.html')

@app.route('/TimeSeriesResults')
def timeseries_results():
    return render_template('timeseries_results.html')

@app.route('/FinalResults')
def final_results():
    return render_template('final_results.html')

if __name__ == '__main__':
    app.run(debug=True)