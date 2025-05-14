"""
import json

with open("Sandbox/players.json","r") as players_file:
    players_json = json.load(players_file)
    insert_query = ""
    for player in players_json:
        insert_query += '(\'' + str(player['telegram_first_name']) + "\'" if player['telegram_first_name'] is not None else ", NULL"
        insert_query += ', \'' + str(player['telegram_last_name'] + "\'") if player['telegram_last_name'] is not None else ", NULL"
        insert_query += ', \'' + str(player['telegram_login']) + "\'" if player['telegram_login'] is not None else ", NULL"
        insert_query += ', \'' + str(player['telegram_id']) + "\'" if player['telegram_id'] is not None else ", NULL"
        insert_query += ', \'' + str(player['friendly_first_name']) + "\'" if player['friendly_first_name'] is not None else ", NULL"
        insert_query += ', \'' + str(player['friendly_last_name']) + "\'" if player['friendly_last_name'] is not None else ", NULL"
        insert_query += ', \'' + str(player['informal_friendly_first_name']) + "\'" if player['informal_friendly_first_name'] is not None else ", NULL"
        insert_query += '),\n'

insert_query = "INSERT INTO Players (telegram_first_name, telegram_last_name, telegram_login, telegram_id, friendly_first_name, friendly_last_name, informal_friendly_first_name) VALUES " + insert_query
print(insert_query)
"""
