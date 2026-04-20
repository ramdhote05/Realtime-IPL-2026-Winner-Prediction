import pandas as pd
import numpy as np

# Load the dataset
file_path = 'c:/Users/ROG/Downloads/archive (16)/IPL.csv'
df = pd.read_csv(file_path, low_memory=False)

# Identify unique matches and their results
# Each match is repeated for every ball, so we drop duplicates based on match_id
matches_df = df.drop_duplicates(subset=['match_id']).copy()

# Select relevant columns for match-level analysis
match_cols = [
    'match_id', 'date', 'batting_team', 'bowling_team', 'match_won_by', 
    'venue', 'toss_winner', 'toss_decision', 'year', 'season'
]

# Note: batting_team/bowling_team in the ball-by-ball data refers to the first innings usually or depends on the row.
# Let's verify how to get Team A and Team B for each match correctly.
# A better way is to find the two teams for each match_id.

match_teams = df.groupby('match_id')['batting_team'].unique().reset_index()
match_teams['team1'] = match_teams['batting_team'].apply(lambda x: x[0] if len(x) > 0 else None)
match_teams['team2'] = match_teams['batting_team'].apply(lambda x: x[1] if len(x) > 1 else None)

# Join back to get more info
matches_cleaned = pd.merge(match_teams[['match_id', 'team1', 'team2']], matches_df, on='match_id')

# We need the actual winner column. 'match_won_by' is what we want to predict.
# Let's clean team names
team_mapping = {
    'Kings XI Punjab': 'Punjab Kings',
    'Delhi Daredevils': 'Delhi Capitals',
    'Rising Pune Supergiants': 'Rising Pune Supergiant',
    'Deccan Chargers': 'Sunrisers Hyderabad', # Arguable, but often grouped for simplicity or kept separate. Let's keep separate but consistent.
}

def clean_team_name(name):
    if pd.isna(name): return name
    return team_mapping.get(name, name)

matches_cleaned['team1'] = matches_cleaned['team1'].apply(clean_team_name)
matches_cleaned['team2'] = matches_cleaned['team2'].apply(clean_team_name)
matches_cleaned['match_won_by'] = matches_cleaned['match_won_by'].apply(clean_team_name)
matches_cleaned['toss_winner'] = matches_cleaned['toss_winner'].apply(clean_team_name)

# Saving the cleaned match-level data
matches_cleaned.to_csv('cleaned_matches.csv', index=False)
print("Cleaned match-level data saved to cleaned_matches.csv")
print(f"Total matches: {len(matches_cleaned)}")
