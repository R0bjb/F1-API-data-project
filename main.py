from F1API import checkSession, store_dates, valid_team_list, team_validity_check, results, create_graph

machineLearning = False
teamComparisonCheck = True


def teamComparison():
    teams = []
    session = input("enter the year you want to check")
    meetings = checkSession(session)
    session_keys, dates, months = store_dates(meetings)#gets the months and dates
    valid_teams = valid_team_list(session_keys)
    team1, team2, teams = team_validity_check()
    team1_points, team2_points = results(teams,team1,team2)
    create_graph(team1_points, team2_points, team1, team2, session_keys)



if teamComparisonCheck:
    teamComparison()



"""
what's happened:

originally I set the program up on one file to just understand APIs, creating a simple graph comparing two teams points across a season.
after this, I decided to continue exploring APIs and stuff so set up a main in which all other functions were imported into.
    Whilst doing this I discovered that importing items doesn't mean they only run when they are called, but instead run upon execution of the program. so
    when some functions in another .py file is imported into main, if it has a print statement, this runs at the start, before it is intended to with the function call"""
