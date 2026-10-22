import pandas as pd
import json
import requests
import os
import time

base_URL = 'https://api.openf1.org/v1'






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


#todo remove bad rows of data. Removed out laps. Might need to remove cancelled races? This would probably be done in the main loop
#each track might need to be seperated.


def remove_bad_columns(dataset):
    dataset = dataset.drop(columns=['date', 'meeting_key_x', 'date_start_y', 'date_end',
                                    'country_key', 'gmt_offset', 'location', 'country_name', 'country_code'])
    return dataset
def remove_bad_rows(dataset):
    dataset = dataset[~dataset['is_pit_out_lap'].isin([True])]
    return dataset
