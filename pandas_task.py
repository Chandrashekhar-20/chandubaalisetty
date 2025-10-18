import pandas as pd

# Load dataset
url = "https://raw.githubusercontent.com/MainakRepositor/Datasets/refs/heads/master/IPL/matches.csv"
df = pd.read_csv(url)

# Total matches
print("Total Matches:", len(df))

# Column names
print("\nColumns:")
print(df.columns.tolist())

# First 5 rows
print("\nFirst 5 rows:")
print(df.head())

# Describe the data
print("\nData Description:")
print(df.describe(include='all'))

# Filter matches decided by 1 run or 1 wicket
close_matches = df[(df['win_by_runs'] == 1) | (df['win_by_wickets'] == 1)]

# Count Player of the Match awards
player_counts = close_matches['player_of_match'].value_counts()
#!question2
# Player with most awards
top_player = player_counts.idxmax()
count = player_counts.max()

print("Top Player:", top_player)
print("Awards:", count)
#!question3


wankhede = df[df['venue'] == 'Wankhede Stadium']

# Count number of wins by runs vs wickets
by_runs = wankhede[wankhede['win_by_runs'] > 0].shape[0]
by_wickets = wankhede[wankhede['win_by_wickets'] > 0].shape[0]

if by_runs > by_wickets:
    result = "More wins by batting first (runs)"
else:
    result = "More wins by batting second (wickets)"

print(f"Wankhede: Runs = {by_runs}, Wickets = {by_wickets}")
print(result)

big_wins = df[df['win_by_runs'] > 50]
top_team = big_wins['winner'].value_counts().idxmax()
count = big_wins['winner'].value_counts().max()

print("Team with most 50+ run wins:", top_team)
print("Count:", count)
#!question4

# Team that won toss AND chose to bat AND won the match
bat_and_win = df[(df['toss_winner'] == df['winner']) & (df['toss_decision'] == 'bat')]

print("Count:", len(bat_and_win))
#!question6
# Filter matches involving Kolkata Knight Riders
kkr_matches = df[(df['team1'] == 'Kolkata Knight Riders') | (df['team2'] == 'Kolkata Knight Riders')]

umpires = pd.concat([kkr_matches['umpire1'], kkr_matches['umpire2']])
umpire_counts = umpires.value_counts()

top_umpire = umpire_counts.idxmax()
count = umpire_counts.max()

print("Top Umpire:", top_umpire)
print("Matches Officiated:", count)
