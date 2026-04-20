import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
import joblib

# Load cleaned data
df = pd.read_csv('cleaned_matches.csv')

# Handle missing winners (e.g., No Result)
df = df.dropna(subset=['match_won_by'])

# Label Encoding
le_team = LabelEncoder()
all_teams = pd.concat([df['team1'], df['team2'], df['match_won_by']]).unique()
le_team.fit(all_teams)

df['team1_enc'] = le_team.transform(df['team1'])
df['team2_enc'] = le_team.transform(df['team2'])
df['toss_winner_enc'] = le_team.transform(df['toss_winner'])
df['winner_enc'] = le_team.transform(df['match_won_by'])

le_venue = LabelEncoder()
df['venue_enc'] = le_venue.fit_transform(df['venue'])

le_toss_decision = LabelEncoder()
df['toss_decision_enc'] = le_toss_decision.fit_transform(df['toss_decision'])

# Simple Feature Engineering: Team Performance (Win Rate)
# Note: In a real scenario, this should be calculated chronologically
team_wins = df.groupby('match_won_by').size()
team_matches = df.groupby('team1').size() + df.groupby('team2').size()
win_rate = team_wins / team_matches
win_rate = win_rate.fillna(0)

df['team1_win_rate'] = df['team1'].map(win_rate)
df['team2_win_rate'] = df['team2'].map(win_rate)

# Train-Test Split (Train on past, Test on 2026)
train_df = df[df['year'] < 2026]
test_df = df[df['year'] == 2026]

features = ['team1_enc', 'team2_enc', 'toss_winner_enc', 'toss_decision_enc', 'venue_enc', 'team1_win_rate', 'team2_win_rate']
X_train = train_df[features]
y_train = train_df['winner_enc']

# Train Model
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Save model and encoders
joblib.dump(model, 'ipl_model.pkl')
joblib.dump(le_team, 'le_team.pkl')
joblib.dump(le_venue, 'le_venue.pkl')
joblib.dump(le_toss_decision, 'le_toss_decision.pkl')

print("Model trained and saved.")

# Predict for 2026 matches
if not test_df.empty:
    X_test = test_df[features]
    y_pred = model.predict(X_test)
    test_df['predicted_winner'] = le_team.inverse_transform(y_pred)
    
    print("\nPredictions for 2026 matches so far:")
    print(test_df[['team1', 'team2', 'match_won_by', 'predicted_winner']].head())
    
    accuracy = (test_df['match_won_by'] == test_df['predicted_winner']).mean()
    print(f"\nAccuracy for 2026 matches so far: {accuracy:.2f}")

# Predict the champion of 2026
# We can simulate probabilities for all teams
teams_2026 = test_df['team1'].unique()
team_probs = {}

for team in teams_2026:
    # Average probability of this team winning against everyone else
    probs = []
    team_enc = le_team.transform([team])[0]
    for opponent in teams_2026:
        if team == opponent: continue
        opp_enc = le_team.transform([opponent])[0]
        
        # Hypothetical match: neutral venue, random toss
        venue_mode = df['venue_enc'].mode()[0]
        toss_dec_mode = df['toss_decision_enc'].mode()[0]
        
        sample = pd.DataFrame([[team_enc, opp_enc, team_enc, toss_dec_mode, venue_mode, win_rate[team], win_rate[opponent]]], columns=features)
        prob = model.predict_proba(sample)
        # Find index for our team
        try:
            team_idx = np.where(model.classes_ == team_enc)[0][0]
            probs.append(prob[0][team_idx])
        except IndexError:
            probs.append(0)
    
    team_probs[team] = np.mean(probs)

sorted_teams = sorted(team_probs.items(), key=lambda x: x[1], reverse=True)
print("\nPredicted 2026 Champion Probability (Relative Strength):")
for team, prob in sorted_teams:
    print(f"{team}: {prob:.2%}")

champion = sorted_teams[0][0]
print(f"\nPredicted Winner of IPL 2026: {champion}")
