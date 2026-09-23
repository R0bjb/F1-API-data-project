import pandas as pd
import json
import requests


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
session = requests.get(f"{base_URL}/sessions", params={"year": 2026, "session_name": "Race"})


def fetch_laps(session_key)


def datahandling():
    #the session key is the session type(race, qualifying 1,2,3 etc...)
    #i will need the session key to understand if it's qualifying or race. get the weather and the track. will also need track times, possibly each segment?
    laps = pd.DataFrame(requests.get(f"{base_URL}/laps", params=))

    weather = requests.get(f"{base_url}/weather", params=)

#   weather(air temp, track temp, pressure, rainfall, wind_D, wind_S,
#   Stints (Compound, Driver_number, session_key)
#   Laps (lap_duration
#   session(circuit_key, session_type)

    # track, session_key, air temp, track temp, pressure, rainfall, wind_direction, wind_speed, compound, tyre_age, lap_duration, Driver Number
    # some items will be stable for a lot of the data, but some things will change lap by lap, driver by driver. so creating the dataset with the drive number and
    # start time will be useful to get to align it with the right weather and laptime data. then remove it before feeding to model


    #todo: find what data points i need to get. lap time, track temp, etc....

"""so the weather is tracked each minute across the track. This means that the minute that the lap is started can be found to then search for the
weather at that specific minute.

"""



This is a test!!!