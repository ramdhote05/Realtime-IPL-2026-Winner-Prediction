from flask import Flask, jsonify, render_template
from flask_cors import CORS
import datetime
import random
import os

# Now templates and static are INSIDE the api folder
base_dir = os.path.dirname(os.path.abspath(__file__))
template_dir = os.path.join(base_dir, 'templates')
static_dir = os.path.join(base_dir, 'static')

app = Flask(__name__, template_folder=template_dir, static_folder=static_dir)
CORS(app)

def get_live_forecast():
    # Dynamic 2026 Season Mock Data
    teams = [
        {"team": "Punjab Kings", "prob": 62.4, "status": "5-1", "color": "#dd0000"},
        {"team": "RCB", "prob": 58.2, "status": "4-2", "color": "#d11d26"},
        {"team": "Rajasthan Royals", "prob": 55.1, "status": "4-2", "color": "#eb008b"},
        {"team": "Sunrisers Hyderabad", "prob": 51.3, "status": "3-3", "color": "#ff822a"},
        {"team": "Gujarat Titans", "prob": 48.7, "status": "3-3", "color": "#1b2133"}
    ]
    
    challengers = [
        {"team": "CSK", "prob": 42.1, "color": "#ffff00"},
        {"team": "LSG", "prob": 39.5, "color": "#0057e2"},
        {"team": "DC", "prob": 35.2, "color": "#0057e2"},
        {"team": "KKR", "prob": 28.9, "color": "#3a225d"},
        {"team": "MI", "prob": 15.4, "color": "#004ba0"}
    ]
    
    # Tiny variation to simulate live processing
    date_seed = datetime.datetime.now().strftime("%Y%m%d%H")
    random.seed(date_seed)
    for t in teams:
        t['prob'] = round(t['prob'] + (random.random() * 0.4 - 0.2), 1)
        
    return {
        "updated": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "top_5": teams,
        "challengers": challengers,
        "verdict": "Punjab Kings"
    }

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/data')
def get_data():
    return jsonify(get_live_forecast())

# Expose 'app' for Vercel
if __name__ == '__main__':
    app.run(debug=True, port=5000)
