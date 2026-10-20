import pandas as pd
import json
import requests
import os
import time

base_URL = 'https://api.openf1.org/v1'

"""within this file, the prediction model will be developed.

--- random thought, it might be good to look at specific tracks. if using  metrics like wind direction and speed, they might be misleading
with northerly winds greatly benefiting times in one track, and hindering times in another.

todo create a dataframe from the API to feed into the training algorithm.
todo once dataset is created, set up the test/train splits and all of that jazz
todo after the test/train and dataset is all set up, set the model up with parameters etc.
todo following that, pass the data through the model and actually train it."""

#I think it will be a regression problem to predict all the times so find a good model for that, then get enough
#data points to make the weather notable to the model so it actually looks at it when predicting.
#session = requests.get(f"{base_URL}/sessions", params={"year": 2026, "session_name": "Race"})


#makes a directory and stores data based on the endpoint chosen(sessions, laps etc...
def get_stored(endpoint, params, cache_dir="cache"):
    os.makedirs(cache_dir, exist_ok=True)#makes a directory, ignores error if directory exists
    key = endpoint + "_" + "_".join(f"{k}={v}" for k, v in sorted(params.items()))
    path = os.path.join(cache_dir, key + ".json")#creates a path name to store data
    if os.path.exists(path):#if that path exists, don't request from the API
        return json.load(open(path))
    r = requests.get(f"{base_URL}/{endpoint}", params = params)
    r.raise_for_status()
    data = r.json()
    #dataframe = pd.read_json('C:\CV Programming\F1 api programming folder\cache\laps_session_key=9158.json')
    #print(dataframe.to_string())
    json.dump(data, open(path, "w"))
    time.sleep(0.4)
    #data_df = pd.dataframe(data)
    return data

def clean_dataframes(laps, weather):#sorts both dataframes based on dates, then removes null values
    laps_df = laps.sort_values("date")
    weather_df = weather.sort_values("date")
    laps_df = laps_df.dropna()
    weather_df = weather_df.dropna()
    return laps_df, weather_df

def merge_weatherandlap(laps, weather):
    merged = pd.merge_asof(  # merge both laps and weather dataframe, using the date column.
        laps, weather,
        on="date", direction="nearest",
        tolerance=pd.Timedelta("2min")
    )
    return merged
def merge_stints(merged, stints):
    #merge the latests df and stint df together, driver number and a lap column can be used. something will need to be done with the laps though
    #because the master file uses specific lap number, whilst stint declares start lap and end lap of that stint. maybe do if lap_number is > start and < end.

    merge = pd.merge_asof(
        merged.sort_values("lap_number"), stints.sort_values("lap_start"),
        by="driver_number", left_on="lap_number", right_on="lap_start",
        direction = "backward" # the lap needs to be either an added column to each df. or an if statement checking for laps between lap start and end in stints
    )
    return merge

def drop_dupe_col(merged):
    columns_toberemoved = ["meeting_key_x", "meeting_key_y", "session_key_x", "session_key_y"]
    merged = merged.drop(columns_toberemoved, axis='columns')
    return merged


def merge_track(merged, sessions):
    merge = pd.merge_asof(
        merged, sessions,
        on="session_key", direction = "nearest"
    )
    return merge