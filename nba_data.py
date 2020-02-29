# importing requests library
import requests
from datetime import date
from datetime import datetime
# from datetime import timedelta

import time
from os import path
import json

import os

import pandas as pd

# API data stored under directory './data/'
local_dir = "./data/"


# nba_teams.json --> ./data/TEAMS
def get_teams():
    teams_url = "http://data.nba.net/json/cms/noseason/sportsmeta/nba_teams.json"
    teams_names = "nba_teams"
    teams_folder = "TEAMS/"

    file_path = local_dir + teams_folder + teams_names
    check_flag = False
    if path.exists(file_path):
        check_flag = True
        with open(file_path, 'r') as in_file:
            json_file = in_file.read()
            teams_data = json.loads(json_file)

    if not check_flag:
        teams_req = requests.get(teams_url)

        teams_data = teams_req.json()
        with open(file_path, 'w') as out_file:
            json.dump(teams_data, out_file)

    teams = teams_data["sports_content"]["teams"]["team"]
    teams_df = pd.DataFrame(teams)
    # strip off pre-season/ non-league teams
    nba_team_df = teams_df[(teams_df.is_nba_team == True) & (teams_df.team_name != "Home")]

    return nba_team_df


# today.json --> ./data/TODAY
def daily_summary():
    today_url = "http://data.nba.net/json/cms/today.json"
    today_name = "today_summary"
    today_folder = "TODAY/"
    universe_date = date.today().strftime("%Y%m%d")

    file_path = local_dir + today_folder + today_name
    check_flag = False
    # check if local today 1. exists; 2. up-to-date
    if path.exists(file_path):
        last_modification_time = os.stat(file_path).st_mtime
        last_modification_date = datetime.fromtimestamp(last_modification_time).strftime("%Y%m%d")
        if last_modification_date == universe_date:
            check_flag = True
            # print("today file up-to-date")
            with open(file_path, 'r') as in_file:
                json_file = in_file.read()
                today_data = json.loads(json_file)
        # print(check_flag)

    if not check_flag:
        today_req = requests.get(url=today_url)

        today_data = today_req.json()
        with open(file_path, 'w') as out_file:
            json.dump(today_data, out_file)

    today_summary = today_data["sports_content"]["sports_meta"]['season_meta']
    today_season = today_summary["display_season"]
    today_year = today_summary["display_year"]

    hello_message: str = "Welcome to NBA {} {}".format(today_season, today_year)
    return hello_message
    # print("Welcome to NBA {} {}".format(today_season, today_year))


# team daily schedule --> ./data/GAMES
def get_schedule(team_name):
    team_param = team_name.lower()
# api-endpoint
# URL template http://data.nba.net/json/cms/[year]/team/[team_name]/schedule.json
    api_url = "http://data.nba.net/json/cms/2019/team/%s/schedule.json" % team_param
    game_folder = "GAMES/"

    # check if local cache exists
    filename = local_dir + game_folder + team_param
    has_read = False
    if path.exists(filename):
        print("file exists")
        with open(filename, 'r') as in_file:
            json_file = in_file.read()
            if len(json_file) > 0:
                start_read = time.time()
                has_read = True
                game_data = json.loads(json_file)
                print("READ took: " + str(time.time() - start_read))

    if not has_read:
        start_get = time.time()
        game_req = requests.get(url=api_url)
        print("GET took: " + str(time.time() - start_get))

        game_data = game_req.json()
        with open(filename, 'w') as out_file:
            json.dump(game_data, out_file)

    games = game_data["sports_content"]["game"]

    today_date = date.today().strftime("%Y%m%d")

    has_game = False
    for game in games:
        if today_date == game["date"]:
            visitor = game["visitor"]["city"] + " " + game["visitor"]["nickname"]
            home = game["home"]["city"] + " " + game["home"]["nickname"]
            game_city = game["city"]
            game_time = game["home_start_date"] + game["home_start_time"]
            game_time = datetime.strptime(game_time, "%Y%m%d%H%M").strftime("%Y/%m/%d %I:%M %p")
            has_game = True

            schedule_message = "{} at {}\n:basketball: {} Local Time {}".format(visitor, home, game_city, game_time)
            # print("{} - {}. Date {}. by VW".format(visitor, home, today_date))
        elif today_date < game["date"]:
            break

    if not has_game:
        today_date = date.today().strftime("%Y/%m/%d")
        schedule_message = "{} is not playing today. :v:  Date {}.".format(team_name.title(), today_date)

    return schedule_message




