from F1API import checkSession, store_dates, valid_team_list, team_validity_check, results, create_graph
from PredictionModel import get_stored
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
    session_key = 9160  # example!!   could loop through with a time.sleep to change session name.
    laps = get_stored("laps", {"session_key": session_key})
    weather = get_stored("weather", {"session_key": session_key})
    stints = get_stored("stints", {"session_key": session_key})

    laps_df = pd.DataFrame(laps)
    weather_df = pd.DataFrame(weather)

    for df in (laps_df, weather_df):
        df["date"] = pd.to_datetime(df.get("date_start", df.get("date")))

    laps_df = laps_df.sort_values("date")
    weather_df = weather_df.sort_values("date")

    merged = pd.merge_asof(
        laps_df, weather_df,
        on = "date", direction="nearest",
        tolerance = pd.Timedelta("2min")
    )



    #dataframe = pd.read_json('laps_session_key=9158.json')
    #print (dataframe.to_string())





if teamComparisonCheck:
    teamComparison()
if machineLearning:
    modeltraining()




"""
what's happened:

originally I set the program up on one file to just understand APIs, creating a simple graph comparing two teams points across a season.
after this, I decided to continue exploring APIs and stuff so set up a main in which all other functions were imported into.
    Whilst doing this I discovered that importing items doesn't mean they only run when they are called, but instead run upon execution of the program. so
    when some functions in another .py file is imported into main, if it has a print statement, this runs at the start, before it is intended to with the function call"""
