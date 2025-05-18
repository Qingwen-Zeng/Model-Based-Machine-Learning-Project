import pandas as pd

path_folder = './original_data'
att_df = pd.read_csv(path_folder+'/attendance.csv')
games_df = pd.read_csv(path_folder+'/games.csv')
stands_df = pd.read_csv(path_folder+'/standings.csv')
attendance_proc_df = pd.read_csv('./processed_data/attendance_capacity_rate.csv')

games_df.loc[:, 'Winner Name'] = games_df['winner'].apply(lambda x: x.split(' ')[-1])


games_league_df = games_df.loc[~games_df['week'].isin(['WildCard','Division', 'ConfChamp', 'SuperBowl'])]
games_league_df.loc[:,'week'] = games_league_df['week'].astype(int)
att_df.loc[:, 'week'] = att_df['week'].astype(int)

# Number of wins in last 5 games
att_df.loc[:, 'Wins_last_5_games'] = att_df.apply(lambda x: games_league_df.loc[(games_league_df['year'] == x['year']) & (games_league_df['week'] < x['week']) & ((games_league_df['home_team_name'] == x['team_name']) | (games_league_df['away_team_name'] == x['team_name']))].iloc[-6:-1].loc[games_league_df['Winner Name'] == x['team_name']].shape[0], axis=1)
att_df.loc[:, 'Bad_streak'] = att_df['Wins_last_5_games'] <= 1
att_df.loc[:, 'Medium_streak'] = (att_df['Wins_last_5_games'] <= 3) & (att_df['Wins_last_5_games'] >= 2)
att_df.loc[:, 'Good_streak'] = att_df['Wins_last_5_games'] >= 4
# Performance previous seasons: Superbowl wins and playoffs finishes

superbowl_winners = stands_df.loc[stands_df['sb_winner'] == 'Won Superbowl']
playoffs_finishers = stands_df.loc[(stands_df['playoffs'] == 'Playoffs')]

# True if they won the superbowl last year
att_df.loc[:, 'Superbowl winners last year'] = att_df.apply(lambda x: superbowl_winners.loc[(superbowl_winners['year'] == x['year']-1) & (superbowl_winners['team_name'] == x['team_name'])].shape[0]==1, axis=1)
# True if they won the superbowl 2 or 3 years before
att_df.loc[:, 'Superbowl winners prev years'] = att_df.apply(lambda x: superbowl_winners.loc[((superbowl_winners['year'] == x['year']-2) | (superbowl_winners['year'] == x['year']-3)) & (superbowl_winners['team_name'] == x['team_name'])].shape[0]>0, axis=1)
# True if they finished in playoffs during the last 2 years
att_df.loc[:, 'Playoff finishers prev years'] = att_df.apply(lambda x: playoffs_finishers.loc[(playoffs_finishers['year'] < x['year']) & (playoffs_finishers['year'] >= x['year']-2) & (playoffs_finishers['team_name'] == x['team_name'])].shape[0]>0, axis=1)


attendance_proc_df.loc[:, ['Sb_winners', 'Sb_winners_prev_years', 'Playoff_prev_years', 'Bad_streak', 'Medium_streak', 'Good_streak']] = att_df.loc[:, ['Superbowl winners last year', 'Superbowl winners prev years', 'Playoff finishers prev years', 'Bad_streak', 'Medium_streak', 'Good_streak']].values
attendance_proc_df.to_csv('./processed_data/attendance_w_team_perf.csv', index=False)