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

# OFFICIAL SYNC: Standings as of April 20, 2026 (End of Match Day)
TEAMS_DB = [
    {"team": "Punjab Kings", "p": 6, "w": 5, "l": 0, "d": 1, "nrr": 1.420, "color": "#dd0000"},
    {"team": "RCB", "p": 6, "w": 4, "l": 2, "d": 0, "nrr": 1.171, "color": "#d11d26"},
    {"team": "Rajasthan Royals", "p": 6, "w": 4, "l": 2, "d": 0, "nrr": 0.599, "color": "#eb008b"},
    {"team": "Sunrisers Hyderabad", "p": 6, "w": 3, "l": 3, "d": 0, "nrr": 0.566, "color": "#ff822a"},
    {"team": "Delhi Capitals", "p": 5, "w": 3, "l": 2, "d": 0, "nrr": 0.310, "color": "#0057e2"},
    {"team": "Gujarat Titans", "p": 5, "w": 3, "l": 2, "d": 0, "nrr": 0.018, "color": "#1b2133"},
    {"team": "Mumbai Indians", "p": 6, "w": 2, "l": 4, "d": 0, "nrr": -0.710, "color": "#004ba0"}, # UPGRADED AFTER TODAY'S WIN
    {"team": "CSK", "p": 6, "w": 2, "l": 4, "d": 0, "nrr": -0.780, "color": "#ffff00"},
    {"team": "LSG", "p": 6, "w": 2, "l": 4, "d": 0, "nrr": -1.173, "color": "#0057e2"},
    {"team": "KKR", "p": 7, "w": 1, "l": 5, "d": 1, "nrr": -0.879, "color": "#3a225d"}
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
    
    # OFFICIAL SYNC: Start baseline from April 21 (Since Apr 20 matches are done)
    start_date = datetime.datetime(2026, 4, 21, tzinfo=datetime.timezone.utc)
    
    # Calculate days passed since baseline
    days_passed = (utc_now - start_date).days
    
    # Check if today's match (Match 34) is finished
    # IPL matches usually end around 23:15 - 23:30 IST
    match_finished = ist_now.hour >= 23 and ist_now.minute >= 30
    
    # Total simulation cycles (Days passed + 1 more if today's match is over)
    simulation_count = days_passed + (1 if match_finished else 0)
    
    current_table = [dict(t) for t in TEAMS_DB]

    # Automated Future Evolution (Stable Seeding)
    if simulation_count > 0:
        for i in range(simulation_count):
            # Seed based on the match day index to keep historical results stable
            random.seed(i + 42) 
            winner_idx = random.randint(0, 9)
            loser_idx = random.randint(0, 9)
            while loser_idx == winner_idx: loser_idx = random.randint(0, 9)
            
            # Update winner
            current_table[winner_idx]['p'] += 1
            current_table[winner_idx]['w'] += 1
            current_table[winner_idx]['nrr'] = round(current_table[winner_idx]['nrr'] + 0.125, 3)
            
            # Update loser
            current_table[loser_idx]['p'] += 1
            current_table[loser_idx]['l'] += 1
            current_table[loser_idx]['nrr'] = round(current_table[loser_idx]['nrr'] - 0.125, 3)

    # Point Calculation logic including Draws (W=2, D=1)
    for team in current_table:
        team['pts'] = (team['w'] * 2) + (team['d'] * 1)

    # Official Sorting: Points -> Wins -> NRR
    sorted_table = sorted(current_table, key=lambda x: (x['pts'], x['w'], x['nrr']), reverse=True)
    
    top_5 = []
    for i in range(5):
        team = sorted_table[i]
        # Dynamic probability calculation based on current simulated standings
        prob = round((team['pts'] / (team['p']*2) if team['p'] > 0 else 0) * 85 + (team['nrr'] * 5), 1)
        top_5.append({"team": team['team'], "prob": prob, "status": f"{team['w']}-{team['l']}-{team['d']}", "color": team['color']})

    challengers = []
    for i in range(5, 10):
        team = sorted_table[i]
        prob = round((team['pts'] / (team['p']*2) if team['p'] > 0 else 0) * 45, 1)
        challengers.append({"team": team['team'], "prob": prob, "color": team['color']})

    return {
        "updated": ist_now.strftime("%Y-%m-%d %H:%M:%S"),
        "points_table": sorted_table,
        "upcoming": UPCOMING_MATCHES,
        "top_5": top_5,
        "challengers": challengers,
        "verdict": sorted_table[0]['team'],
        "day_offset": simulation_count,
        "match_status": "MATCH DAY COMPLETED" if match_finished else "MATCH IN PROGRESS"
    }

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/data')
def get_data():
    return jsonify(get_automated_standings())

if __name__ == '__main__':
    app.run(debug=True, port=5000)
