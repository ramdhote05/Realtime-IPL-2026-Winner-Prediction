from flask import Flask, jsonify, render_template
from flask_cors import CORS
import datetime
import random
import os

base_dir = os.path.dirname(os.path.abspath(__file__))
# Note: In api-folder structure, templates/static are inside 'api/'
template_dir = os.path.join(base_dir, 'templates')
static_dir = os.path.join(base_dir, 'static')

app = Flask(__name__, template_folder=template_dir, static_folder=static_dir)
CORS(app)

# All 10 Teams for the Real-Time Points Table
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

def get_automated_standings():
    now = datetime.datetime.now()
    # Baseline: April 20, 2026. Finale: May 24, 2026.
    start_date = datetime.datetime(2026, 4, 20)
    days_passed = (now - start_date).days
    
    # Deep Copy to prevent mutating the baseline
    current_table = [dict(t) for t in TEAMS_DB]

    # SEASON EVOLUTION LOGIC
    # For every day that passes, we simulate matches being played
    if days_passed > 0:
        for _ in range(days_passed):
            # Randomly pick 1-2 teams to "win" a match today to simulate table movement
            # In a real environment, we'd replace this with a Daily API Fetch
            winner_idx = random.randint(0, len(current_table)-1)
            current_table[winner_idx]['p'] += 1
            current_table[winner_idx]['w'] += 1
            
            loser_idx = random.randint(0, len(current_table)-1)
            while loser_idx == winner_idx: loser_idx = random.randint(0, len(current_table)-1)
            current_table[loser_idx]['p'] += 1
            current_table[loser_idx]['l'] += 1

    # Sort Table by Wins then NRR
    sorted_table = sorted(current_table, key=lambda x: (x['w'], x['nrr']), reverse=True)
    
    # Calculate Win Probability for Top 5
    top_5 = []
    for i in range(5):
        team = sorted_table[i]
        # Weighted prob: Wins + 10% of NRR
        prob = round((team['w'] / team['p'] if team['p'] > 0 else 0) * 80 + (team['nrr'] * 10), 1)
        top_5.append({
            "team": team['team'],
            "prob": prob,
            "status": f"{team['w']}-{team['l']}",
            "color": team['color']
        })

    # Challengers (Rank 6-10)
    challengers = []
    for i in range(5, 10):
        team = sorted_table[i]
        prob = round((team['w'] / team['p'] if team['p'] > 0 else 0) * 40, 1)
        challengers.append({
            "team": team['team'],
            "prob": prob,
            "color": team['color']
        })

    return {
        "updated": now.strftime("%Y-%m-%d %H:%M:%S"),
        "points_table": sorted_table,
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
