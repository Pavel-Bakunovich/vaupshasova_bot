import os
from psycopg2 import pool
from dotenv import load_dotenv
from helpers import fill_template, get_today_minsk_time
from logger import log, log_error
import constants

load_dotenv()
connection_string = os.getenv('DATABASE_URL')

def create_connection_pool():
    connection_pool = pool.SimpleConnectionPool(1, 10, connection_string)
    if not connection_pool:
        log_error("Connection pool not created successfully")
    conn = connection_pool.getconn()
    cur = conn.cursor()

    return connection_pool

def close_connection_pool(pool):
    conn = pool.getconn()
    conn.close()
    pool.putconn(conn)
    pool.closeall()

def add_game_stats(player_id, game_id, goals, assists, own_goals):
    connection_pool = create_connection_pool()
    connection = connection_pool.getconn()
    cursor = connection.cursor()
    cursor.execute(f"UPDATE Matchday SET Goals={goals}, Assists={assists}, Own_Goals={own_goals} WHERE Player_ID = {player_id} AND Game_ID = {game_id}")
    connection.commit()
    close_connection_pool(connection_pool)

def get_season_stats(year):
    connection_pool = create_connection_pool()
    connection = connection_pool.getconn()
    cursor = connection.cursor()

    cursor.execute(f'''
    SELECT Players.Friendly_First_Name, Players.Friendly_Last_Name,
      COUNT(Matchday.Player_ID) as Games_Played,
      SUM(Goals) as Goals_Sum,
      SUM(Assists) as Assists_Sum,
      SUM(Own_Goals) as Own_Goals_Sum
  FROM Matchday INNER JOIN Players ON Players.id = Matchday.Player_ID
                INNER JOIN Games on Games.id = Matchday.Game_ID
  WHERE Matchday.type like 'add'
          and Games.game_date <= '{year}-12-31'
          and Games.game_date >= '{year}-01-01'
          and Games.game_date <= current_date
          and Games.Played = TRUE
GROUP BY Players.Friendly_First_Name, Players.Friendly_Last_Name
ORDER BY Goals_Sum DESC
LIMIT 25
    ''')
    stats = cursor.fetchall()
    
    connection.commit()
    return stats


def add_matchday_money(player_id, game_id, money_given, balance_change, comment):
    connection_pool = create_connection_pool()
    connection = connection_pool.getconn()
    cursor = connection.cursor()
    cursor.execute(f"UPDATE Matchday SET Money_Given={money_given}, Balance_Change={balance_change}, Comment='{comment}' WHERE Player_ID = {player_id} AND Game_ID = {game_id}")
    connection.commit()
    close_connection_pool(connection_pool)


def add_money_without_matchday(player_id, money_given, balance_change, comment):
    connection_pool = create_connection_pool()
    connection = connection_pool.getconn()
    cursor = connection.cursor()
    cursor.execute(f"INSERT INTO Matchday (Type, Player_ID, Time_Stamp, Money_Given, Balance_Change, Comment) VALUES ('{constants.TYPE_JUST_MONEY}', {player_id}, '{get_today_minsk_time()}', {money_given}, {balance_change}, '{comment}')")
    connection.commit()
    close_connection_pool(connection_pool)

def get_game_id(matchday_date):
    connection_pool = create_connection_pool()
    connection = connection_pool.getconn()
    cursor = connection.cursor()

    cursor.execute(f"SELECT id FROM Games WHERE Game_Date = '{matchday_date}'")
    game_day = cursor.fetchone()
    if game_day is None:
        cursor.execute(f"INSERT INTO Games (Game_Date) VALUES ('{matchday_date}')")
    
    connection.commit()
    return game_day[0]

def get_game_id_without_adding_new(matchday_date):
    connection_pool = create_connection_pool()
    connection = connection_pool.getconn()
    cursor = connection.cursor()
    cursor.execute(f"SELECT id FROM Games WHERE Game_Date = '{matchday_date}'")
    game_day = cursor.fetchone()
    if game_day is None:
        return None
    connection.commit()
    return game_day[0]

def remove_player(telegram_id):
    connection_pool = create_connection_pool()
    connection = connection_pool.getconn()
    cursor = connection.cursor()

    cursor.execute(
        fill_template(
            'DELETE FROM Players WHERE Telegram_ID = {telegram_id}',
            telegram_id=telegram_id))
    connection.commit()

    close_connection_pool(connection_pool)


def update_player(id, first_name, last_name, login, telegram_id):
    connection_pool = create_connection_pool()
    connection = connection_pool.getconn()
    cursor = connection.cursor()

    cursor.execute(
        fill_template(
            'UPDATE Players SET Telegram_First_Name = \'{first_name}\', Telegram_Last_Name = \'{last_name}\', Telegram_Login = \'{login}\', Telegram_ID = \'{telegram_id}\' WHERE id = \'{playerID}\'',
            first_name=first_name,
            last_name=last_name,
            login=login,
            telegram_id=telegram_id,
            playerID=id))
    connection.commit()

    close_connection_pool(connection_pool)


def create_player(first_name, last_name, username, telegram_id):
    connection_pool = create_connection_pool()
    connection = connection_pool.getconn()
    cursor = connection.cursor()

    cursor.execute(
        fill_template(
            'INSERT INTO Players (Telegram_First_Name, Telegram_Last_Name, Telegram_Login, Telegram_ID) VALUES (\'{first_name}\', \'{last_name}\', \'{username}\', \'{telegram_id}\')',
            first_name=first_name,
            last_name=last_name,
            username=username,
            telegram_id=telegram_id))
    connection.commit()

    close_connection_pool(connection_pool)
    return find_player(telegram_id)


def find_player(telegram_id):
    connection_pool = create_connection_pool()
    connection = connection_pool.getconn()
    cursor = connection.cursor()
    cursor.execute(f'SELECT Telegram_First_Name, Telegram_Last_Name, Telegram_Login, Telegram_ID, Friendly_First_Name, Friendly_Last_Name, Informal_Friendly_First_Name, id FROM Players WHERE Telegram_ID = {telegram_id}')
    player = cursor.fetchone()
    close_connection_pool(connection_pool)
    return player


def find_player_by_name(first_name, last_name):
    connection_pool = create_connection_pool()
    connection = connection_pool.getconn()
    cursor = connection.cursor()
    if (first_name is not None) and (last_name is not None):
        cursor.execute(f"SELECT Telegram_First_Name, Telegram_Last_Name, Telegram_Login, Telegram_ID, Friendly_First_Name, Friendly_Last_Name, Informal_Friendly_First_Name, id FROM Players WHERE Friendly_First_Name = '{first_name}' AND Friendly_Last_Name = '{last_name}'")
    else:
        if last_name is not None:
            cursor.execute(f"SELECT Telegram_First_Name, Telegram_Last_Name, Telegram_Login, Telegram_ID, Friendly_First_Name, Friendly_Last_Name, Informal_Friendly_First_Name, id FROM Players WHERE Friendly_Last_Name = '{last_name}'")
        else:
            cursor.execute(f"SELECT Telegram_First_Name, Telegram_Last_Name, Telegram_Login, Telegram_ID, Friendly_First_Name, Friendly_Last_Name, Informal_Friendly_First_Name, id FROM Players WHERE Friendly_First_Name = '{first_name}'")
    player = cursor.fetchall()
    result = None
    if len(player) == 1:
        result = player[0]
    close_connection_pool(connection_pool)

    return result

def register_player_matchday(matchday_date, type, player_id):
    connection_pool = create_connection_pool()
    connection = connection_pool.getconn()
    cursor = connection.cursor()
    game_id = get_game_id(matchday_date)
    cursor.execute(f'INSERT INTO Matchday (Game_ID, Type, Player_ID, Time_Stamp) VALUES (\'{game_id}\', \'{type}\', \'{player_id}\', \'{get_today_minsk_time()}\')')
    connection.commit()
    close_connection_pool(connection_pool)

def update_player_squad_for_matchday(player_id, squad, matchday_date):
    connection_pool = create_connection_pool()
    connection = connection_pool.getconn()
    cursor = connection.cursor()
    game_id = get_game_id(matchday_date)
    cursor.execute(f"UPDATE Matchday SET Squad = \'{squad}\', Time_Stamp = \'{get_today_minsk_time()}\' WHERE Player_ID = \'{player_id}\' AND Game_ID = {game_id}")

    connection.commit()

    close_connection_pool(connection_pool)    

def find_registraion_player_matchday(matchday_date, telegram_id):
    connection_pool = create_connection_pool()
    connection = connection_pool.getconn()
    cursor = connection.cursor()
    game_id = get_game_id(matchday_date)
    cursor.execute(f'SELECT Players.id, Matchday.Type, Matchday.Wokeup, Players.Telegram_First_Name, Players.Telegram_Last_Name, Players.Telegram_Login, Players.Telegram_ID, Players.Friendly_First_Name, Players.Friendly_Last_Name, Players.Informal_Friendly_First_Name, Matchday.Squad FROM Matchday INNER JOIN Players ON Matchday.Player_ID=Players.id WHERE Players.Telegram_ID = \'{telegram_id}\' AND Matchday.Game_ID = \'{game_id}\'')
    matchday = cursor.fetchone()

    close_connection_pool(connection_pool)

    return matchday

def update_registraion_player_matchday(matchday_date, type, player_id):
    connection_pool = create_connection_pool()
    connection = connection_pool.getconn()
    cursor = connection.cursor()
    game_id = get_game_id(matchday_date)
    cursor.execute(f'UPDATE Matchday SET Type = \'{type}\', Time_Stamp = \'{get_today_minsk_time()}\' WHERE Player_ID = \'{player_id}\' AND Game_ID = \'{game_id}\'')
    connection.commit()

    close_connection_pool(connection_pool)

def get_matchday_players_count(matchday_date):
    connection_pool = create_connection_pool()
    connection = connection_pool.getconn()
    cursor = connection.cursor()
    game_id = get_game_id(matchday_date)
    cursor.execute(f'SELECT COUNT(*) FROM Matchday INNER JOIN Players ON Matchday.Player_ID=Players.id WHERE Matchday.Game_ID = {game_id} AND Matchday.Type=\'add\'')
    matchday_players_count = cursor.fetchone()
    close_connection_pool(connection_pool)
    return matchday_players_count[0]

def get_squad(matchday_date):
    connection_pool = create_connection_pool()
    connection = connection_pool.getconn()
    cursor = connection.cursor()
    game_id = get_game_id(matchday_date)
    cursor.execute(f'SELECT Players.id, Matchday.Type, Matchday.Wokeup, Players.Telegram_First_Name, Players.Telegram_Last_Name, Players.Telegram_Login, Players.Telegram_ID, Players.Friendly_First_Name, Players.Friendly_Last_Name, Players.Informal_Friendly_First_Name, Matchday.Squad FROM Matchday INNER JOIN Players ON Matchday.Player_ID=Players.id WHERE Matchday.Game_ID = \'{game_id}\' ORDER BY Matchday.Squad, Matchday.Time_Stamp ASC')
    matchdays = cursor.fetchall()
    close_connection_pool(connection_pool)
    return matchdays

def get_players_balance():
    connection_pool = create_connection_pool()
    connection = connection_pool.getconn()
    cursor = connection.cursor()
    cursor.execute(f"SELECT Players.id, Players.Friendly_First_Name, Players.Friendly_Last_Name, SUM(Balance_Change) as Balance FROM Matchday INNER JOIN Players ON Players.id = Matchday.Player_ID GROUP BY Players.Friendly_First_Name, Players.Friendly_Last_Name, Players.Birthday, Players.Height, Players.id ORDER BY Balance ASC")
    matchdays = cursor.fetchall()
    close_connection_pool(connection_pool)
    return matchdays

def wakeup(matchday_date, player_id):
    connection_pool = create_connection_pool()
    connection = connection_pool.getconn()
    cursor = connection.cursor()
    game_id = get_game_id(matchday_date)
    cursor.execute(f'UPDATE Matchday SET Wokeup = \'{True}\', Time_Stamp = \'{get_today_minsk_time()}\' WHERE Player_ID = {player_id} AND Game_ID = {game_id}')
    connection.commit()
    close_connection_pool(connection_pool)
    return get_sleeping_player_count(matchday_date)

def get_sleeping_player_count(matchday_date):
    connection_pool = create_connection_pool()
    connection = connection_pool.getconn()
    cursor = connection.cursor()
    game_id = get_game_id(matchday_date)
    cursor.execute(f'SELECT COUNT(*) FROM Matchday WHERE Game_ID = \'{game_id}\' AND wokeup = FALSE AND type=\'add\'')
    sleeping_player_count = cursor.fetchone()
    close_connection_pool(connection_pool)
    return sleeping_player_count[0]
