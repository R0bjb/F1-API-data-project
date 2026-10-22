from F1API import checkSession, store_dates, valid_team_list, team_validity_check, results, create_graph
from datacleaning_model import get_stored, clean_dataframes, merge_weatherandlap, merge_stints,drop_dupe_col, merge_track, remove_bad_columns, remove_bad_rows
from Model_training import define_x_y, test_train_split, build_model
import pandas as pd

machineLearning = True
teamComparisonCheck = False


def team_comparison():
    session = input("enter the year you want to check")
    meetings = checkSession(session)
    session_keys, dates, months = store_dates(meetings)#gets the months and dates
    valid_team_list(session_keys)
    team1, team2, teams = team_validity_check()
    team1_points, team2_points = results(teams,team1,team2)
    create_graph(team1_points, team2_points, team1, team2, session_keys)
def model_training():
    session_key = 9166  # example!!   could loop through with a time.sleep to change session name.
    sessions = get_stored("sessions", {"session_key": session_key})
    laps = get_stored("laps", {"session_key": session_key})
    weather = get_stored("weather", {"session_key": session_key})
    stints = get_stored("stints", {"session_key": session_key})

    laps_df = pd.DataFrame(laps)
    weather_df = pd.DataFrame(weather)
    stints_df = pd.DataFrame(stints)
    sessions = pd.DataFrame(sessions)




    for df in (laps_df, weather_df):#adds a date column to both laps and weather dataframe, making it a pandas datetime datatype to merge
        df["date"] = pd.to_datetime(df.get("date_start", df.get("date")), format = 'ISO8601')

    laps_df, weather_df = clean_dataframes(laps_df, weather_df)#clean lap and weather dataframe
    merged = merge_weatherandlap(laps_df, weather_df)   #merge weather and lap dataframe after cleaning
    merged = merge_stints(merged, stints_df) #merge the stint dataframe with the previously merged lap and weather dataframe
    merged = drop_dupe_col(merged)
    merged = merge_track(merged, sessions)

    cleaned = remove_bad_columns(merged)
    cleaned = remove_bad_rows(cleaned)
    print(cleaned.columns)
    print(cleaned.to_string())
    print(cleaned.shape)

    X, Y = define_x_y(cleaned)
    X_train, X_test, y_train, y_test = test_train_split(X, Y)
    y_pred = build_model(X_train, y_train, X_test)


if teamComparisonCheck:
    team_comparison()
if machineLearning:
    model_training()

