import pandas as pd


data_path = './processed_data'
weather_data_path = './weather_data'
dump_path = './datasets_w_weather_data'
team_name = 'New York Giants'
initial_year = 2010
nickname = team_name.split(' ')[-1].lower()

attendance_df = pd.read_csv(data_path+'/attendance_w_team_perf.csv')
weather_df = pd.read_csv(weather_data_path+'/export_'+nickname+'.csv')
games_df = pd.read_csv(data_path+'/games.csv')

games_df_team = games_df[(games_df['home_team'] == team_name) & (games_df['year']>=initial_year)][['year', 'week', 'date']]
games_df_team = games_df_team.loc[~games_df_team['week'].isin(['WildCard','Division', 'ConfChamp', 'SuperBowl'])]
df_pats = attendance_df.loc[(attendance_df['year']>= initial_year) & (attendance_df['team_name'] == nickname) & (attendance_df['location'] == 'home')]
games_df_team['week'] = games_df_team['week'].astype(int)
# Merge on year and week
df_pats = df_pats.merge(games_df_team, on=['year', 'week'], how='left')
df_pats['year'] = df_pats['year'].astype(str)
df_pats['date'] = df_pats['date'].astype(str)
# Combine into full date string
df_pats['full_date'] = pd.to_datetime(df_pats['date'] + ' ' + df_pats['year'], format='%B %d %Y')

weather_df.rename(columns={'date': 'full_date'}, inplace=True)
weather_df['full_date'] = pd.to_datetime(weather_df['full_date'])

df_pats = df_pats.merge(weather_df, on=['full_date'], how='left')

df_pats.to_csv(dump_path+'/attendance_'+nickname+'.csv', index=False)

