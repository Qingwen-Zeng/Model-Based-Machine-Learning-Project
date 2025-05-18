# %%
import pandas as pd
import os

# Specify the destination folder
destination_folder = "./downloaded_csv_files"

# Read each CSV file into a separate DataFrame
attendance_df = pd.read_csv(os.path.join(destination_folder, 'attendance.csv'))
games_df = pd.read_csv(os.path.join(destination_folder, 'games.csv'))
standings_df = pd.read_csv(os.path.join(destination_folder, 'standings.csv'))

# %% [markdown]
# ## I am using team_name as the key across dfs, therefore, I drop the others

# %%
attendance_df["team_full"] = attendance_df["team"] + " " + attendance_df["team_name"]
attendance_df = attendance_df.drop(columns=["team", "team_name"])

# Same on standings_df
standings_df["team_full"] = standings_df["team"] + " " + standings_df["team_name"]
standings_df = standings_df.drop(columns=["team", "team_name"])

# Drop this columns from scores_df 
games_df = games_df.drop(columns=["home_team_name", "away_team_name", "away_team_city"])


# %%
# Count unique values by team and year on attendance df on total, home, away columns
attendance_df.groupby(["team_full", "year"]).nunique(dropna=False)[["total", "home", "away", "weekly_attendance"]].reset_index().head(20)

# %% [markdown]
# This is telling us that total, home, away are always the same values, thus they dont give any info, we actually care only on weekly attendance, that we see it has 17 different values for the 17 games of the year. Therefore, we can drop it.

# %%
attendance_df = attendance_df.drop(columns=["total","home", "away"])
# Resort columns
attendance_df = attendance_df[["year", "team_full", "week", "weekly_attendance"]]

# %% 
# In games_df week, there are the 17 weeks, but also 'WildCard' 'Division' 'ConfChamp' 'SuperBowl'
print(games_df['week'].unique())

# We create a new df with this values called spetial games
special_games_df = games_df[games_df['week'].isin(['WildCard', 'Division', 'ConfChamp', 'SuperBowl'])].copy()

# We drop the special games from the original df
games_df = games_df[~games_df['week'].isin(['WildCard', 'Division', 'ConfChamp', 'SuperBowl'])].copy()
# %%
# Specify column types for attendance_df
attendance_df[["year", "week", "weekly_attendance"]] = attendance_df[["year", "week", "weekly_attendance"]].astype("Int16", errors="ignore")
attendance_df["team_full"] = attendance_df["team_full"].astype("string")

# Specify column types for games_df
games_df[["year", "week", "pts_win", "pts_loss", "yds_win", "yds_loss", "turnovers_win", "turnovers_loss"]] = games_df[["year", "week", "pts_win", "pts_loss", "yds_win", "yds_loss", "turnovers_win", "turnovers_loss"]].astype("Int16", errors="ignore")
games_df[["home_team", "away_team", "home_team_city"]] = games_df[["home_team", "away_team", "home_team_city"]].astype("string")

# Specify column types for standings_df
standings_df[["year", "wins", "loss", "points_for", "points_against", "points_differential"]] = standings_df[["year", "wins", "loss", "points_for", "points_against", "points_differential"]].astype("Int16", errors="ignore")
standings_df[["margin_of_victory", "strength_of_schedule", "simple_rating", "offensive_ranking", "defensive_ranking"]] = standings_df[["margin_of_victory", "strength_of_schedule", "simple_rating", "offensive_ranking", "defensive_ranking"]].astype("float")
standings_df[["playoffs", "team_full", "sb_winner"]] = standings_df[["playoffs", "team_full", "sb_winner"]].astype("string")

# Specify column types for special_games_df
special_games_df[["year", "pts_win", "pts_loss", "yds_win", "yds_loss", "turnovers_win", "turnovers_loss"]] = special_games_df[["year", "pts_win", "pts_loss", "yds_win", "yds_loss", "turnovers_win", "turnovers_loss"]].astype("Int16", errors="ignore")
special_games_df[["week", "home_team", "away_team", "home_team_city"]] = special_games_df[["week", "home_team", "away_team", "home_team_city"]].astype("string")


# Print the data types of each DataFrame

print("Attendance DataFrame dtypes:")
print(attendance_df.dtypes)
print("\nGames DataFrame dtypes:")
print(games_df.dtypes)
print("\nStandings DataFrame dtypes:")
print(standings_df.dtypes)
print("\nSpecial Games DataFrame dtypes:")
print(special_games_df.dtypes)


# %% 
# Adding home and away teams to attendance_df
# Step 1: Create a DataFrame for home teams
home_df = games_df[['year', 'week', 'home_team']].copy()
home_df['home'] = True
home_df.rename(columns={'home_team': 'team_full'}, inplace=True)

# Step 2: Create a DataFrame for away teams
away_df = games_df[['year', 'week', 'away_team']].copy()
away_df['home'] = False
away_df.rename(columns={'away_team': 'team_full'}, inplace=True)

# Step 3: Combine both home and away into one DataFrame
teams_df = pd.concat([home_df, away_df], ignore_index=True)

# Step 4: Merge with attendance_df on year, week, and team name
attendance_df = attendance_df.merge(
    teams_df,
    on=['year', 'week', 'team_full'],
    how='left'
)

# %%
# Save the cleaned DataFrames to new CSV files
destination_folder = "./cleaned_csv_files"
os.makedirs(destination_folder, exist_ok=True)

attendance_df.to_csv(os.path.join(destination_folder, 'attendance.csv'), index=False)
games_df.to_csv(os.path.join(destination_folder, 'games.csv'), index=False)
standings_df.to_csv(os.path.join(destination_folder, 'standings.csv'), index=False)
special_games_df.to_csv(os.path.join(destination_folder, 'special_games.csv'), index=False)


