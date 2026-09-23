import requests

from datetime import datetime
import json
import matplotlib.pyplot as plt
import numpy as np

debug = False

errordict = {
    "400": "Bad Request - The request could not be understood or was missing required parameters.",
    "401": "Unauthorized - Authentication failed or user does not have permissions for the desired action",
    "403": "Forbidden - Authentication succeeded but authenticated user does not have access to the resource.",
    "404": "Not Found - The requested resource could not be found.",
    "408": "Request Timeout - The server timed out waiting for the request.",
    "500": "Internal Server Error - An error occurred on the server.",
    "502": "Bad Gateway - The server was acting as a gateway or proxy and received an invalid session from the upstream server.",
    "503": "Service Unavailable - The server is currently unavailable (overloaded or down).",
}

base_URL = 'https://api.openf1.org/v1'
session_keys = []
dates = []
months = []

URL = 'https://api.openf1.org/v1/sessions?country_name=Belgium&session_name=Sprint%20Qualifying&year=2023'


class customError(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


session = requests.get(f"{base_URL}/sessions", params={"year": 2026, "session_name": "Race"})

print("THIS IS THE STATUS CODE_______________", session.status_code)



def checkSession(season):#get the meetings details for each race session throughout the specified season
    meetings = requests.get(f"{base_URL}/sessions", params={"year": season, "session_name": "Race"})
    if debug:
        print("the status code is: ", meetings.status_code)
    meetings = meetings.json()
    return meetings


def store_dates(meetings):
    for i in meetings:#for each meeting throughout the year
        session_keys.append(i['session_key'])#add the session key to a list
        dates.append(i['date_end'])#add the date of the race to a list

    for i in range(len(dates)):#loop for all races
        formatted = datetime.fromisoformat(dates[i])
        months.append(formatted.month)#add the specific month to a list
    return session_keys, dates, months



valid_teams = []

def valid_team_list(session_keys):
    championship_teams = (requests.get(f"{base_URL}/championship_teams", params={"session_key": session_keys})).json()
    for i in championship_teams:
        valid_teams.append(i['team_name'])
    return valid_teams





def team_validity_check():
    valid1 = False
    while valid1 == False:
        team1 = input("enter the 1st team name")
        if team1 in valid_teams:
            valid1 = True
        else:
            print("you might have misplet something, try again")
            valid1 = False

    valid2 = False
    while valid2 == False:
        team2 = input("enter the 2nd team name")
        if team2 in valid_teams:
            valid2 = True
        else:
            print("that isn't a team, try again")
            valid2 = False

    teams = [team1, team2]
    return team1, team2, teams




def results(teams, team1, team2):
    team1_points = []
    team2_points = []
    points = requests.get(f"{base_URL}/championship_teams", params={"team_name": teams,
                                                                    "session_key": session_keys})  # this gets results from the api containing items from the endpoint containing only items from the entered teams and specified season
    points = points.json()
    for i in points:  # loops through the request response, appending team1 points after each race, as well as team2's
        if i["team_name"] == team1:
            team1_points.append(i["points_current"])
        elif i["team_name"] == team2:
            team2_points.append(i["points_current"])

    return team1_points, team2_points



def create_graph(team1_points, team2_points, team1, team2, session_keys):
    ypoints = np.array(team1_points)

    plt.plot(team1_points, label=team1)
    plt.plot(team2_points, label=team2)
    plt.title(f" {team1} vs {team2} scores compared")
    plt.xlabel("races")
    plt.ylabel("team points")
    plt.xlim(0, len(session_keys))
    plt.legend()
    plt.show()

### update the log. i have got it to add points after each race to a list for both teams. need to figure out how to plot a graph then done.
# possible improvements could be to add circuit names for each plot, and add a verification layer as mentioned at some point below.


# at this point, inputs are taken but not verified in any mannor. find a way to store team names from the api. possibly using team champs section.
# the above section prints the information for each Race session in the specified season, with track and session key.
""" the session key gained from above can be seperated for use next to loop through. looping by the session key. searching for the team and the points at each stage
, doing this with both teams

if there is a way to add joint queries to search for 2 teams within 1 api query that would be useful. otherwise a query will have to be made with team 1 and team 2 seperately."""


##idk how but i want to create a graph of the points for each team across the season.

# i'll need to get the points for each team acrosss the season. probably just add each point to a list to plot?

# use the parameters in the query for this. create a variable for the year and the team name, loop through each session for the points


""" I'll put a little dev blog here because why not:

i'm starting this once i've developed a vague understanding of APIs and have decided to create a system that takes 2 team inputs and a year,
then plots the score progress between the teams throughout the season.
at this point the code takes the inputs but does not verify either, then grabs the session keys from the session API using the year as the main indicator.

The hurdle at this point is the question of whether the api has been designed to store the session keys in appending order, or a completely random order
as the list of session keys is currently quite random. the first idea to solve this is to get the dates, along with the session_keys, to aligm the two in chronological order
instead of the possible random order it is currently in.

following the ordering of these, a loop can be created, using an api query with the session key and team names to develop a library of points throughout the season for both teams.
following this the array of scores from each team can be compared using a library like matplotlib to show the final graph throughout each race.


WHILST WRITING THIS I HAVE ALSO REMEMBERED THAT A STORAGE OF TRACKS NEEDS TO BE MADE ALONGSIDE THE SESSION KEY TO USE WITHIN THE GRAPH.



update 2:
i have got the month of each event seperated from the date, the list of months created are in oreder ascending from march through to december,
with this it can be assumed that the session keys are also in order, as the values have been gained from the results of the same API query.
next on the plan is to look at the other api endpoint to store the score of both teams from the session keys"""