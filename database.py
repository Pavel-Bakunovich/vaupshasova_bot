import os
from psycopg2 import pool
from dotenv import load_dotenv
from helpers import fill_template

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
            'DELETE FROM "public"."Players" WHERE "Telegram_ID" = {telegram_id}',
            telegram_id=telegram_id))
    connection.commit()

    close_connection_pool(connection_pool)


def update_player(id, first_name, last_name, login, telegram_id):
    connection_pool = create_connection_pool()
    connection = connection_pool.getconn()
    cursor = connection.cursor()

    cursor.execute(
        fill_template(
            'UPDATE "public"."Players" SET "Telegram_First_Name" = \'{first_name}\', "Telegram_Last_Name" = \'{last_name}\', "Telegram_Login" = \'{login}\', "Telegram_ID" = \'{}\' WHERE "id" = \'{playerID}\'',
            first_name=first_name,
            last_name=last_name,
            login=login,
            id=id,
            playerID=id))
    connection.commit()

    close_connection_pool(connection_pool)


def create_player(first_name, last_name, username, telegram_id):
    connection_pool = create_connection_pool()
    connection = connection_pool.getconn()
    cursor = connection.cursor()

    cursor.execute(
        fill_template(
            'INSERT INTO "public"."Players" ("Telegram_First_Name", "Telegram_Last_Name", "Telegram_Login", "Telegram_ID") VALUES (\'{first_name}\', \'{last_name}\', \'{username}\', \'{telegram_id}\')',
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
            'SELECT * FROM "public"."Players" WHERE "Telegram_ID" = \'{telegram_id}\'',
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
            'INSERT INTO "public"."Matchday" ("Matchday_Date", "Type", "Player_ID", "Time_Stamp") VALUES (\'{matchday_date}\', \'{type}\', \'{player_id}\', NOW())',
            matchday_date=matchday_date,
            type=type,
            player_id=player_id))
    connection.commit()

    close_connection_pool(connection_pool)


def find_registraion_player_matchday(matchday_date, telegram_id):
    connection_pool = create_connection_pool()
    connection = connection_pool.getconn()
    cursor = connection.cursor()
    cursor.execute(
        fill_template(
            'SELECT * FROM "public"."Matchday" INNER JOIN "public"."Players"  ON "public"."Matchday"."Player_ID"="public"."Players"."id" WHERE "public"."Players"."Telegram_ID" = \'{telegram_id}\' AND "public"."Matchday"."Matchday_Date" = \'{matchday_date}\'',
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
            'UPDATE "public"."Matchday" SET "Type" = \'{type}\', "Time_Stamp" = NOW() WHERE "Player_ID" = \'{player_id}\' AND "Matchday_Date" = \'{matchday_date}\'',
            matchday_date=matchday_date,
            type=type,
            player_id=player_id))
    connection.commit()

    close_connection_pool(connection_pool)


def get_matchday_players_count(matchday_date):
    connection_pool = create_connection_pool()
    connection = connection_pool.getconn()
    cursor = connection.cursor()
    cursor.execute(
        fill_template(
            'SELECT COUNT(*) FROM "public"."Matchday" INNER JOIN "public"."Players"  ON "public"."Matchday"."Player_ID"="public"."Players"."id" WHERE "public"."Matchday"."Matchday_Date" = \'{matchday_date}\' AND "public"."Matchday"."Type"=\'add\'',
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
            'SELECT * FROM "public"."Matchday" INNER JOIN "public"."Players"  ON "public"."Matchday"."Player_ID"="public"."Players"."id" WHERE "public"."Matchday"."Matchday_Date" = \'{matchday_date}\'',
            matchday_date=matchday_date))
    matchdays = cursor.fetchall()

    close_connection_pool(connection_pool)

    return matchdays


#print(find_registraion_player_matchday('03/22/2025',343151297))

#create_player("Pavel", "Bakunovich", "@pavel_bakunovich", 34756345)
#remove_player(34756345)
#update_player(15, "Pavel1", "Bakunovich2", "@pavel_bakunovich2", 555)

#def get_players():

#def create_or_update_matchday():

#def register_player_matchday():

#def unregisterplayer_matchday():
