from flask import Flask, jsonify, render_template
from flask_cors import CORS
import datetime
import random
import os

base_dir = os.path.dirname(os.path.abspath(__file__))
template_dir = os.path.join(base_dir, 'templates')
static_dir = os.path.join(base_dir, 'static')

app = Flask(__name__, template_folder=template_dir, static_folder=static_dir)
CORS(app)

# Base Standings as of April 20
TEAMS_DB = [
    {"team": "Punjab Kings", "p": 6, "w": 5, "l": 1, "nrr": 1.250, "color": "#dd0000"},
    {"team": "RCB", "p": 6, "w": 4, "l": 2, "nrr": 0.850, "color": "#d11d26"},
    {"team": "Rajasthan Royals", "p": 6, "w": 4, "l": 2, "nrr": 0.420, "color": "#eb008b"},
    {"team": "Sunrisers Hyderabad", "p": 6, "w": 3, "l": 3, "nrr": 0.120, "color": "#ff822a"},
    {"team": "Gujarat Titans", "p": 6, "w": 3, "l": 3, "nrr": -0.150, "color": "#1b2133"},
    {"team": "CSK", "p": 6, "w": 3, "l": 3, "nrr": -0.450, "color": "#ffff00"},
    {"team": "LSG", "p": 6, "w": 2, "l": 4, "nrr": -0.620, "color": "#0057e2"},
    {"team": "Delhi Capitals", "p": 6, "w": 2, "l": 4, "nrr": -0.780, "color": "#0057e2"},
    {"team": "KKR", "p": 6, "w": 2, "l": 4, "nrr": -0.850, "color": "#3a225d"},
    {"team": "Mumbai Indians", "p": 6, "w": 1, "l": 5, "nrr": -1.350, "color": "#004ba0"}
]

UPCOMING_MATCHES = [
    {"match": 35, "t1": "PBKS", "t2": "RR", "date": "April 21", "venue": "Mullanpur"},
    {"match": 36, "t1": "RCB", "t2": "SRH", "date": "April 22", "venue": "Bengaluru"},
    {"match": 37, "t1": "KKR", "t2": "CSK", "date": "April 23", "venue": "Kolkata"},
    {"match": 38, "t1": "DC", "t2": "LSG", "date": "April 24", "venue": "Delhi"},
    {"match": 39, "t1": "GT", "t2": "RR", "date": "April 25", "venue": "Ahmedabad"}
]

def get_automated_standings():
    utc_now = datetime.datetime.now(datetime.timezone.utc)
    ist_now = utc_now + datetime.timedelta(hours=5, minutes=30)
    
    start_date = datetime.datetime(2026, 4, 20, tzinfo=datetime.timezone.utc)
    days_passed = (utc_now - start_date).days
    
    current_table = [dict(t) for t in TEAMS_DB]

    if days_passed > 0:
        random.seed(days_passed)
        for _ in range(days_passed):
            winner_idx = random.randint(0, 9)
            loser_idx = random.randint(0, 9)
            while loser_idx == winner_idx: loser_idx = random.randint(0, 9)
            current_table[winner_idx]['p'] += 1
            current_table[winner_idx]['w'] += 1
            current_table[loser_idx]['p'] += 1
            current_table[loser_idx]['l'] += 1

    sorted_table = sorted(current_table, key=lambda x: (x['w'], x['nrr']), reverse=True)
    
    top_5 = []
    for i in range(5):
        team = sorted_table[i]
        prob = round((team['w'] / team['p'] if team['p'] > 0 else 0) * 80 + (team['nrr'] * 10), 1)
        top_5.append({"team": team['team'], "prob": prob, "status": f"{team['w']}-{team['l']}", "color": team['color']})

    challengers = []
    for i in range(5, 10):
        team = sorted_table[i]
        prob = round((team['w'] / team['p'] if team['p'] > 0 else 0) * 40, 1)
        challengers.append({"team": team['team'], "prob": prob, "color": team['color']})

    return {
        "updated": ist_now.strftime("%Y-%m-%d %H:%M:%S"),
        "points_table": sorted_table,
        "upcoming": UPCOMING_MATCHES,
        "top_5": top_5,
        "challengers": challengers,
        "verdict": sorted_table[0]['team'],
        "day_offset": days_passed
    }

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/data')
def get_data():
    return jsonify(get_automated_standings())

if __name__ == '__main__':
    app.run(debug=True, port=5000)
