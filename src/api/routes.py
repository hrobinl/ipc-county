from flask import Flask, request, jsonify, render_template, json
from flask_cors import CORS
import sys, os
sys.path.append("C:\\Users\\benny\\Github\\ipc-county\\src\\db")
from data import get_map_data, get_bar_data, get_scatter_data

app = Flask(__name__)

CORS(app, support_credentials=True)


# Render Homepage
@app.route("/")
def home():
    print("Server received request for 'Home' page...")
    return render_template('index.html')

# Render About Page
@app.route("/about")
def about():
    print("Server received request for 'About' page...")
    return render_template('about.html')

# Map configuration endpoint
@app.route('/config', methods=['GET'])
def get_map_config():
    SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
    json_url = os.path.join(SITE_ROOT, "/Users/benny/Github/ipc-county/src/api/static/lib/us-counties-10m.json")
    data = json.load(open(json_url))
    return jsonify(data)

# Visualization data endpoint
@app.route('/visuals', methods=['POST'])
def get_visual_data():
    data = request.get_json()
    sqlVar = data.get('data')
    map = get_map_data(sqlVar)
    bar = get_bar_data(sqlVar)
    scatter = get_scatter_data(sqlVar)

    return jsonify({"bar":bar, "map":map, "scatter": scatter})

if __name__ == '__main__':
    app.run(debug=True)