import os
from psycopg2 import pool
from dotenv import load_dotenv
from helpers import fill_template,get_next_matchday,get_today_minsk_time

load_dotenv()
connection_string = os.getenv('DATABASE_URL')


def create_connection_pool():
    connection_pool = pool.SimpleConnectionPool(1, 10, connection_string)
    if not connection_pool:
        print("Connection pool not created successfully")
    conn = connection_pool.getconn()
    cur = conn.cursor()

    return connection_pool


def close_connection_pool(pool):
    conn = pool.getconn()
    conn.close()
    pool.putconn(conn)
    pool.closeall()


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
    cursor.execute(
        fill_template(
            'SELECT * FROM Players WHERE Telegram_ID = \'{telegram_id}\'',
            telegram_id=telegram_id))
    player = cursor.fetchone()

    close_connection_pool(connection_pool)

    return player


def register_player_matchday(matchday_date, type, player_id):
    connection_pool = create_connection_pool()
    connection = connection_pool.getconn()
    cursor = connection.cursor()
    cursor.execute(
        fill_template(
            'INSERT INTO Matchday (Matchday_Date, Type, Player_ID, Time_Stamp) VALUES (\'{matchday_date}\', \'{type}\', \'{player_id}\', \'{date_now}\')',
            matchday_date=matchday_date,
            type=type,
            player_id=player_id,
            date_now=get_today_minsk_time()))
    connection.commit()

    close_connection_pool(connection_pool)


def find_registraion_player_matchday(matchday_date, telegram_id):
    connection_pool = create_connection_pool()
    connection = connection_pool.getconn()
    cursor = connection.cursor()
    cursor.execute(
        fill_template(
            'SELECT * FROM Matchday INNER JOIN Players ON Matchday.Player_ID=Players.id WHERE Players.Telegram_ID = \'{telegram_id}\' AND Matchday.Matchday_Date = \'{matchday_date}\'',
            telegram_id=telegram_id,
            matchday_date=matchday_date))
    matchday = cursor.fetchone()

    close_connection_pool(connection_pool)

    return matchday


def update_registraion_player_matchday(matchday_date, type, player_id):
    connection_pool = create_connection_pool()
    connection = connection_pool.getconn()
    cursor = connection.cursor()

    cursor.execute(
        fill_template(
            'UPDATE Matchday SET Type = \'{type}\', Time_Stamp = \'{date_now}\' WHERE Player_ID = \'{player_id}\' AND Matchday_Date = \'{matchday_date}\'',
            matchday_date=matchday_date,
            type=type,
            date_now=get_today_minsk_time(),
            player_id=player_id))
    connection.commit()

    close_connection_pool(connection_pool)


def get_matchday_players_count(matchday_date):
    connection_pool = create_connection_pool()
    connection = connection_pool.getconn()
    cursor = connection.cursor()
    cursor.execute(
        fill_template(
            'SELECT COUNT(*) FROM Matchday INNER JOIN Players ON Matchday.Player_ID=Players.id WHERE Matchday.Matchday_Date = \'{matchday_date}\' AND Matchday.Type=\'add\'',
            matchday_date=matchday_date))
    matchday_players_count = cursor.fetchone()

    close_connection_pool(connection_pool)

    return matchday_players_count[0]


def get_squad(matchday_date):
    connection_pool = create_connection_pool()
    connection = connection_pool.getconn()
    cursor = connection.cursor()
    cursor.execute(
        fill_template(
            'SELECT * FROM Matchday INNER JOIN Players ON Matchday.Player_ID=Players.id WHERE Matchday.Matchday_Date = \'{matchday_date}\'',
            matchday_date=matchday_date))
    matchdays = cursor.fetchall()

    close_connection_pool(connection_pool)

    return matchdays

def wakeup(matchday_date, player_id):
    connection_pool = create_connection_pool()
    connection = connection_pool.getconn()
    cursor = connection.cursor()
    cursor.execute(fill_template(
            'UPDATE Matchday SET Wokeup = \'{wokeup}\', Time_Stamp = \'{date_now}\' WHERE Player_ID = \'{player_id}\' AND Matchday_Date = \'{matchday_date}\'',
            wokeup=True,
            date_now=get_today_minsk_time(),
            matchday_date=matchday_date,
            player_id=player_id))
    connection.commit()
    close_connection_pool(connection_pool)
    return get_sleeping_player_count(matchday_date)

def get_sleeping_player_count(matchday_date):
    connection_pool = create_connection_pool()
    connection = connection_pool.getconn()
    cursor = connection.cursor()
    cursor.execute(
        fill_template(
            'SELECT COUNT(*) FROM Matchday WHERE Matchday_Date = \'{matchday_date}\' AND wokeup = FALSE',
            matchday_date=matchday_date))
    sleeping_player_count = cursor.fetchone()

    close_connection_pool(connection_pool)

    return sleeping_player_count[0]