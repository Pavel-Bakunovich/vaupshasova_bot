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

def execute_sql_query_return_one(sql_query):
    connection_pool = create_connection_pool()
    connection = connection_pool.getconn()
    cursor = connection.cursor()
    cursor.execute(sql_query)
    result = cursor.fetchone()
    close_connection_pool(connection_pool)
    return result[0]

def execute_sql_query_return_many(sql_query):
    connection_pool = create_connection_pool()
    connection = connection_pool.getconn()
    cursor = connection.cursor()
    cursor.execute(sql_query)
    result = cursor.fetchall()
    close_connection_pool(connection_pool)
    return result

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
ORDER BY Games_Played DESC
LIMIT 20;
    ''')
    stats = cursor.fetchall()
    
    connection.commit()
    return stats

def get_individual_stats_by_season(player_id):
    connection_pool = create_connection_pool()
    connection = connection_pool.getconn()
    cursor = connection.cursor()
    cursor.execute(f'''
            SELECT 
                EXTRACT(year FROM Games.game_date) as Season,
                COUNT(Matchday.Player_ID) as Games_Played,
                SUM(Goals) as Goals_Sum,
                SUM(Assists) as Assists_Sum,
                SUM(Own_Goals) as Own_Goals_Sum
            FROM Matchday INNER JOIN Players ON Players.id = Matchday.Player_ID
                            INNER JOIN Games on Games.id = Matchday.Game_ID
            WHERE Matchday.type like 'add'
                    and Games.game_date <= current_date
                    and Games.Played = TRUE
            GROUP BY EXTRACT(year FROM Games.game_date), Players.id
            HAVING Players.id = {player_id}
            ORDER BY Season DESC
    ''')
    stats = cursor.fetchall()
    connection.commit()
    return stats

def get_individual_stats(player_id):
    connection_pool = create_connection_pool()
    connection = connection_pool.getconn()
    cursor = connection.cursor()
    cursor.execute(f'''
            SELECT
                COUNT(Matchday.Player_ID) as Games_Played,
                SUM(Goals) as Goals_Sum,
                SUM(Assists) as Assists_Sum,
                SUM(Own_Goals) as Own_Goals_Sum,
                SUM(CASE  
                    WHEN Squad = 'Corn'
                    THEN 1 ELSE 0 END) as Games_played_for_Corn,
                SUM(CASE  
                    WHEN Squad = 'Tomato'
                    THEN 1 ELSE 0 END) as Games_played_for_Tomato
            FROM Matchday INNER JOIN Players ON Players.id = Matchday.Player_ID
                            INNER JOIN Games on Games.id = Matchday.Game_ID
            WHERE Matchday.type like 'add'
                    and Games.game_date <= current_date
                    and Games.Played = TRUE
                    and Players.id = {player_id}
    ''')
    stats = cursor.fetchone()
    connection.commit()
    return stats

def get_active_win_streak_by_player(player_id):
    with open(f"SQL Queries/{constants.SQL_ACTIVE_WIN_STREAK_INDIVIDUAL}" , "r") as file:
        sql_file = file.read()
    connection_pool = create_connection_pool()
    connection = connection_pool.getconn()
    cursor = connection.cursor()
    cursor.execute(fill_template(sql_file, player_id = player_id))
    stats = cursor.fetchone()
    connection.commit()
    return stats

def get_active_loss_streak_by_player(player_id):
    with open(f"SQL Queries/{constants.SQL_ACTIVE_LOSS_STREAK_INDIVIDUAL}" , "r") as file:
        sql_file = file.read()
    connection_pool = create_connection_pool()
    connection = connection_pool.getconn()
    cursor = connection.cursor()
    cursor.execute(fill_template(sql_file, player_id = player_id))
    stats = cursor.fetchone()
    connection.commit()
    return stats

def get_active_no_loss_streak_by_player(player_id):
    with open(f"SQL Queries/{constants.SQL_ACTIVE_NO_LOSS_STREAKS_INDIVIDUAL}" , "r") as file:
        sql_file = file.read()
    connection_pool = create_connection_pool()
    connection = connection_pool.getconn()
    cursor = connection.cursor()
    cursor.execute(fill_template(sql_file, player_id = player_id))
    stats = cursor.fetchone()
    connection.commit()
    return stats

def get_top_win_streak_by_player(player_id):
    with open(f"SQL Queries/{constants.SQL_WIN_STREAKS_INDIVIDUAL}" , "r") as file:
        sql_file = file.read()
    connection_pool = create_connection_pool()
    connection = connection_pool.getconn()
    cursor = connection.cursor()
    cursor.execute(fill_template(sql_file, player_id = player_id))
    stats = cursor.fetchone()
    connection.commit()
    return stats

def get_top_loss_streak_by_player(player_id):
    with open(f"SQL Queries/{constants.SQL_LOSING_STREAKS_INDIVIDUAL}" , "r") as file:
        sql_file = file.read()
    connection_pool = create_connection_pool()
    connection = connection_pool.getconn()
    cursor = connection.cursor()
    cursor.execute(fill_template(sql_file, player_id = player_id))
    stats = cursor.fetchone()
    connection.commit()
    return stats

def get_top_no_loss_streak_by_player(player_id):
    with open(f"SQL Queries/{constants.SQL_NO_LOSS_STREAKS_INDIVIDUAL}" , "r") as file:
        sql_file = file.read()
    connection_pool = create_connection_pool()
    connection = connection_pool.getconn()
    cursor = connection.cursor()
    cursor.execute(fill_template(sql_file, player_id = player_id))
    stats = cursor.fetchone()
    connection.commit()
    return stats

def get_last_individual_games(player_id):
    connection_pool = create_connection_pool()
    connection = connection_pool.getconn()
    cursor = connection.cursor()
    cursor.execute(f'''
        SELECT Games.game_date, Games.score_corn, Games.score_tomato, Matchday.goals, Matchday.assists, Matchday.own_goals, Matchday.squad FROM Matchday
            INNER JOIN Games on Games.id = Matchday.Game_id
            WHERE played = True and type = 'add'
                    and Matchday.Player_id = {player_id}
                    and Games.game_date <= current_date
            ORDER BY game_date DESC
            LIMIT 25
    ''')
    stats = cursor.fetchall()
    connection.commit()
    return stats

def get_max_goals_per_game_by_player(player_id):
    with open(f"SQL Queries/{constants.SQL_MAX_GOALS_PER_GAME_BY_PLAYER}" , "r") as file:
        sql_file = file.read()
    connection_pool = create_connection_pool()
    connection = connection_pool.getconn()
    cursor = connection.cursor()
    cursor.execute(fill_template(sql_file, Player_ID = player_id))
    result = cursor.fetchall()
    connection.commit()
    return result

def get_max_assists_per_game_by_player(player_id):
    with open(f"SQL Queries/{constants.SQL_MAX_ASSISTS_PER_GAME_BY_PLAYER}" , "r") as file:
        sql_file = file.read()
    connection_pool = create_connection_pool()
    connection = connection_pool.getconn()
    cursor = connection.cursor()
    cursor.execute(fill_template(sql_file, Player_ID = player_id))
    result = cursor.fetchall()
    connection.commit()
    return result

def get_max_own_goals_per_game_by_player(player_id):
    with open(f"SQL Queries/{constants.SQL_MAX_OWN_GOALS_PER_GAME_BY_PLAYER}" , "r") as file:
        sql_file = file.read()
    connection_pool = create_connection_pool()
    connection = connection_pool.getconn()
    cursor = connection.cursor()
    cursor.execute(fill_template(sql_file, Player_ID = player_id))
    result = cursor.fetchall()
    connection.commit()
    return result

def get_win_rate(player_id):
    connection_pool = create_connection_pool()
    connection = connection_pool.getconn()
    cursor = connection.cursor()
    cursor.execute(f'''
SELECT 
    Player_Id, Players.Friendly_First_Name, Players.Friendly_Last_Name,
    COUNT(*) AS total_games,
    SUM(CASE 
        WHEN (Squad = 'Corn' AND Games.score_corn > Games.score_tomato) OR
             (Squad = 'Tomato' AND Games.score_tomato > Games.score_corn)
        THEN 1 ELSE 0 END) AS wins,
    ROUND(
        SUM(CASE 
            WHEN (Squad = 'Corn' AND Games.score_corn > Games.score_tomato) OR
                 (Squad = 'Tomato' AND Games.score_tomato > Games.score_corn)
            THEN 1 ELSE 0 END) * 100.0 / COUNT(*),
        2
    ) AS win_rate_percentage
FROM 
    Matchday
INNER JOIN Games ON Games.id = Matchday.Game_ID
INNER JOIN Players ON Players.id = Matchday.Player_Id
WHERE squad is not NULL
GROUP BY 
    Players.Id, Player_Id,Players.Friendly_First_Name, Players.Friendly_Last_Name,Matchday.type
HAVING Matchday.type = 'add' and Players.Id = {player_id}
ORDER BY 
    win_rate_percentage DESC;
    ''')
    stats = cursor.fetchone()
    connection.commit()
    return stats

def get_alltime_stats():
    connection_pool = create_connection_pool()
    connection = connection_pool.getconn()
    cursor = connection.cursor()
    cursor.execute(f'''
SELECT 
    Players.Friendly_First_Name, Players.Friendly_Last_Name,
    COUNT(Matchday.Player_ID) as Games_Played,
	SUM(Goals) as Goals_Sum,
	SUM(Assists) as Assists_Sum,
	SUM(Own_Goals) as Own_Goals_Sum,
	ROUND(SUM(CAST(Matchday.goals as decimal))/COUNT(Matchday.Player_ID),2) as avg_goals,
    SUM(CASE 
        WHEN (Squad = 'Corn' AND Games.score_corn > Games.score_tomato) OR
             (Squad = 'Tomato' AND Games.score_tomato > Games.score_corn)
        THEN 1 ELSE 0 END) AS wins,
    ROUND(
        SUM(CASE 
            WHEN (Squad = 'Corn' AND Games.score_corn > Games.score_tomato) OR
                 (Squad = 'Tomato' AND Games.score_tomato > Games.score_corn)
            THEN 1 ELSE 0 END) * 100.0 / COUNT(*),
        2
    ) AS win_rate_percentage
FROM 
    Matchday
	
INNER JOIN Games ON Games.id = Matchday.Game_ID
INNER JOIN Players ON Players.id = Matchday.Player_Id
where Matchday.type like 'add'
	and Games.game_date <= current_date
	and Games.Played = TRUE
GROUP BY 
    Players.Id, Player_Id,Players.Friendly_First_Name, Players.Friendly_Last_Name--, Matchday.type
HAVING COUNT(*) > 5
ORDER BY 
    Games_Played DESC
LIMIT 35
    ''')
    stats = cursor.fetchall()
    connection.commit()
    return stats

def get_alltime_stats_games_goal():
    connection_pool = create_connection_pool()
    connection = connection_pool.getconn()
    cursor = connection.cursor()
    cursor.execute(f'''
SELECT 
	(select count(*) from games
		where Games.game_date <= current_date
		and Games.Played = TRUE) as total_games,
	SUM(Goals) as Goals_Sum,
	SUM(Own_Goals) as Own_Goals_Sum
FROM 
    Matchday
INNER JOIN Games ON Games.id = Matchday.Game_ID
where Matchday.type like 'add'
	and Games.game_date <= current_date
	and Games.Played = TRUE;
    ''')
    stats = cursor.fetchone()
    connection.commit()
    return stats

def get_season_score(year):
    connection_pool = create_connection_pool()
    connection = connection_pool.getconn()
    cursor = connection.cursor()

    cursor.execute(f'''
    SELECT 
    SUM(CASE WHEN score_tomato > score_corn THEN 1 ELSE 0 END) AS tomato_wins,
    SUM(CASE WHEN score_corn > score_tomato THEN 1 ELSE 0 END) AS corn_wins,
    SUM(CASE WHEN score_tomato = score_corn THEN 1 ELSE 0 END) AS draws
FROM 
    Games
	WHERE Games.game_date <= '{year}-12-31'
          and Games.game_date >= '{year}-01-01'
          and Games.game_date <= current_date
          and Games.Played = TRUE;
    ''')
    season_score = cursor.fetchone()
    
    connection.commit()
    return season_score

def get_players_balance():
    connection_pool = create_connection_pool()
    connection = connection_pool.getconn()
    cursor = connection.cursor()
    cursor.execute(f'''
SELECT Players.id, Players.Friendly_First_Name, Players.Friendly_Last_Name,
      SUM(Balance_Change) as Balance
  FROM Matchday INNER JOIN Players ON Players.id = Matchday.Player_ID
GROUP BY Players.Friendly_First_Name, Players.Friendly_Last_Name, Players.id
HAVING SUM(Balance_Change) is not NULL
ORDER BY Balance ASC
    ''')
    players_balance = cursor.fetchall()
    
    connection.commit()
    return players_balance

def get_individual_balance(player_id):
    connection_pool = create_connection_pool()
    connection = connection_pool.getconn()
    cursor = connection.cursor()
    cursor.execute(f'''
SELECT SUM(Balance_Change) as Balance,
	  SUM(money_given) as total_money_given
  FROM Matchday INNER JOIN Players ON Players.id = Matchday.Player_ID
  where Matchday.Player_ID = {player_id}
GROUP BY Players.Friendly_First_Name, Players.Friendly_Last_Name, Players.id
ORDER BY Balance ASC
    ''')
    balance = cursor.fetchone()
    connection.commit()
    return balance

def get_payments_history(player_id):
    connection_pool = create_connection_pool()
    connection = connection_pool.getconn()
    cursor = connection.cursor()
    cursor.execute(f'''
SELECT Games.game_date as Payment_Date,
	Matchday.money_given,
	matchday.balance_change,
	SUM(balance_change) OVER (ORDER BY Games.game_date) AS Actual_balance
  FROM Matchday
  INNER JOIN Players ON Players.id = Matchday.Player_ID
  LEFT JOIN Games on Games.id = Matchday.Game_ID
  where Matchday.Player_ID = {player_id} and balance_change is not NULL
ORDER BY Games.game_date DESC
LIMIT 25
    ''')
    payment_history = cursor.fetchall()
    connection.commit()
    return payment_history

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

    select = f"SELECT id FROM Games WHERE Game_Date = '{matchday_date}'"
    cursor.execute(select)
    game_day = cursor.fetchone()
    if game_day is None:
        cursor.execute(f"INSERT INTO Games (Game_Date) VALUES ('{matchday_date}')")
        cursor.execute(select)
        game_day = cursor.fetchone()
    
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

def register_game_score(game_id, score_corn, score_tomato):
    connection_pool = create_connection_pool()
    connection = connection_pool.getconn()
    cursor = connection.cursor()
    cursor.execute(f'UPDATE Games SET score_corn = {score_corn}, score_tomato = {score_tomato} WHERE ID = {game_id};')
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

def get_matchday_chair_count(matchday_date):
    connection_pool = create_connection_pool()
    connection = connection_pool.getconn()
    cursor = connection.cursor()
    game_id = get_game_id(matchday_date)
    cursor.execute(f'SELECT COUNT(*) FROM Matchday INNER JOIN Players ON Matchday.Player_ID=Players.id WHERE Matchday.Game_ID = {game_id} AND Matchday.Type=\'chair\'')
    matchday_players_count = cursor.fetchone()
    close_connection_pool(connection_pool)
    return matchday_players_count[0]

def get_matchday_players_on_chair(matchday_date):
    connection_pool = create_connection_pool()
    connection = connection_pool.getconn()
    cursor = connection.cursor()
    game_id = get_game_id(matchday_date)
    cursor.execute(f'''
                   SELECT Player_ID, friendly_first_name, friendly_last_name, informal_friendly_first_name, telegram_login, time_stamp FROM Matchday INNER JOIN Players ON Matchday.Player_ID=Players.id WHERE Matchday.Game_ID = {game_id} AND Matchday.Type=\'chair\'
                   ORDER BY time_stamp ASC
                   ''')
    matchday_players_on_chair = cursor.fetchall()
    close_connection_pool(connection_pool)
    return matchday_players_on_chair

def get_squad(matchday_date):
    connection_pool = create_connection_pool()
    connection = connection_pool.getconn()
    cursor = connection.cursor()
    game_id = get_game_id(matchday_date)
    cursor.execute(f'SELECT Players.id, Matchday.Type, Matchday.Wokeup, Players.Telegram_First_Name, Players.Telegram_Last_Name, Players.Telegram_Login, Players.Telegram_ID, Players.Friendly_First_Name, Players.Friendly_Last_Name, Players.Informal_Friendly_First_Name, Matchday.Squad FROM Matchday INNER JOIN Players ON Matchday.Player_ID=Players.id WHERE Matchday.Game_ID = \'{game_id}\' ORDER BY Matchday.Squad, Matchday.Time_Stamp ASC')
    matchdays = cursor.fetchall()
    close_connection_pool(connection_pool)
    return matchdays

def get_scores():
    connection_pool = create_connection_pool()
    connection = connection_pool.getconn()
    cursor = connection.cursor()
    cursor.execute(f'''
        SELECT game_date, score_corn, score_tomato, paid_for_pitch, played FROM Games
        ORDER BY game_date DESC
        LIMIT 25
                   ''')
    scores = cursor.fetchall()
    close_connection_pool(connection_pool)
    return scores

def how_many_games_since_last_layment_for_pitch():
    connection_pool = create_connection_pool()
    connection = connection_pool.getconn()
    cursor = connection.cursor()
    cursor.execute(f'''
        SELECT COUNT(id) FROM Games WHERE game_date > (SELECT game_date FROM Games
            WHERE Paid_for_Pitch is not NULL and played = TRUE
        ORDER BY game_date DESC
        LIMIT 1)
                   ''')
    games_since_last_layment = cursor.fetchone()
    close_connection_pool(connection_pool)
    return games_since_last_layment[0]

def date_of_last_layment_for_pitch():
    connection_pool = create_connection_pool()
    connection = connection_pool.getconn()
    cursor = connection.cursor()
    cursor.execute(f'''
        SELECT game_date FROM Games
        WHERE paid_for_Pitch is not NULL
                ORDER BY game_date DESC
            LIMIT 1
                   ''')
    date_of_last_layment_for_pitch = cursor.fetchone()
    close_connection_pool(connection_pool)
    return date_of_last_layment_for_pitch[0]

def register_pitch_payment(game_id, payment_sum):
    connection_pool = create_connection_pool()
    connection = connection_pool.getconn()
    cursor = connection.cursor()
    cursor.execute(f'UPDATE Games SET paid_for_pitch = {payment_sum} WHERE id = {game_id}')
    connection.commit()
    close_connection_pool(connection_pool)

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

def get_todays_birthdays():
    connection_pool = create_connection_pool()
    connection = connection_pool.getconn()
    cursor = connection.cursor()
    today = get_today_minsk_time()
    cursor.execute(f'''
        SELECT Friendly_First_Name, Friendly_Last_Name FROM Players
        WHERE EXTRACT(MONTH FROM Birthday) = {today.month} AND EXTRACT(DAY FROM Birthday) = {today.day}
                   ''')
    birthdays = cursor.fetchall()
    close_connection_pool(connection_pool)
    return birthdays



def get_random_player():
    connection_pool = create_connection_pool()
    connection = connection_pool.getconn()
    cursor = connection.cursor()
    cursor.execute(f'''
        SELECT Players.ID, friendly_first_name, friendly_last_name, informal_friendly_first_name, height, birthday, COUNT(Matchday.ID) 
        FROM Players
        INNER JOIN matchday ON Players.ID = matchday.player_id
        WHERE matchday.type = 'add'
        GROUP BY Players.ID, friendly_first_name, friendly_last_name
        HAVING COUNT(Matchday.ID) > 6
        ORDER BY RANDOM()
        LIMIT 1
                   ''')
    result = cursor.fetchone()
    close_connection_pool(connection_pool)
    return result
