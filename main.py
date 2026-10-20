from F1API import checkSession, store_dates, valid_team_list, team_validity_check, results, create_graph
from PredictionModel import get_stored, clean_dataframes, merge_weatherandlap, merge_stints
import pandas as pd

machineLearning = True
teamComparisonCheck = False


def teamComparison():
    teams = []
    session = input("enter the year you want to check")
    meetings = checkSession(session)
    session_keys, dates, months = store_dates(meetings)#gets the months and dates
    valid_teams = valid_team_list(session_keys)
    team1, team2, teams = team_validity_check()
    team1_points, team2_points = results(teams,team1,team2)
    create_graph(team1_points, team2_points, team1, team2, session_keys)
def modeltraining():
    session_key = 9166  # example!!   could loop through with a time.sleep to change session name.
    laps = get_stored("laps", {"session_key": session_key})
    weather = get_stored("weather", {"session_key": session_key})
    stints = get_stored("stints", {"session_key": session_key})

    laps_df = pd.DataFrame(laps)
    weather_df = pd.DataFrame(weather)
    stints_df = pd.DataFrame(stints)


    for df in (laps_df, weather_df):#adds a date column to both laps and weather dataframe, making it a pandas datetime datatype to merge
        df["date"] = pd.to_datetime(df.get("date_start", df.get("date")), format = 'ISO8601')

    laps_df, weather_df = clean_dataframes(laps_df, weather_df)#clean lap and weather dataframe
    merged = merge_weatherandlap(laps_df, weather_df)   #merge weather and lap dataframe after cleaning
    merged = merge_stints(merged, stints_df) #merge the stint dataframe with the previously merged lap and weather dataframe

    print(merged.to_string())

    #todo clean the most recent dataframe, there are a number of repeated columns such as meeting_key, session_key, and driver_number

    #todo add a track column, using the session endpoint. the trackID, or "circuit_short_name" would be good to have, then the model can differentiate tracks


if teamComparisonCheck:
    teamComparison()
if machineLearning:
    modeltraining()

