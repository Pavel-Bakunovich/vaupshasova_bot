from logger import log, log_error
from telebot.types import ReactionTypeEmoji
from helpers import get_next_matchday, get_next_matchday_formatted, get_today_minsk_time, format_date, escape_markdown
from common import add_player_if_not_existant, validate_access_no_game_registration_needed, text_to_image, get_player_name_formal, reply_only_CEO_can_do_it, validate_CEO_zone, fill_records_template
import database
import constants
import prettytable as pt
import re

records_template = ""

sql_how_many_games_we_played = ""
sql_how_many_games_were_cancelled = ""
sql_win_streaks = ""
sql_losing_streaks = ""
sql_top_goals_per_game = ""
sql_top_assists_per_game = ""
sql_top_own_goals_per_game = ""
sql_win_rate = ""
sql_paid_most_money = ""
sql_played_most_games_for_corn = ""
sql_played_most_games_for_tomato = ""
sql_sat_on_chair_most_times = ""
sql_scored_most_own_goals = ""
sql_top_assists_alltime = ""
sql_top_goals_alltime = ""
sql_top_player_pairs = ""
sql_average_age_and_height = ""
sql_attendance_streaks = ""
sql_max_goal_difference = ""
sql_most_goals_scored_per_game_by_corn = ""
sql_most_goals_scored_per_game_by_tomato = ""

text_how_many_games_we_played = ""
text_how_many_games_were_cancelled = ""
text_losing_streaks = ""
text_top_goals_per_game = ""
text_top_assists_per_game = ""
text_top_own_goals_per_game = ""
text_win_rate = ""
text_paid_most_money = ""
text_played_most_games_for_corn = ""
text_played_most_games_for_tomato = ""
text_sat_on_chair_most_times = ""
text_scored_most_own_goals = ""
text_top_assists_alltime = ""
text_top_goals_alltime = ""
text_top_player_pairs = ""
text_average_age_and_height = ""
text_attandance_streaks = ""
text_max_goal_difference = ""
text_most_goals_scored_per_game_by_corn = ""
text_most_goals_scored_per_game_by_tomato = ""

def execute(message, bot):
    try:
        bot.set_message_reaction(message.chat.id,
                                            message.message_id,
                                            [ReactionTypeEmoji('👾')],
                                            is_big=True)
        
        current_player = add_player_if_not_existant(message.from_user.first_name,
                                            message.from_user.last_name,
                                            message.from_user.username,
                                            message.from_user.id)
       
        if validate_access_no_game_registration_needed(message.chat.id, current_player, bot, message):
            records = build_records_text()
            bot.reply_to(message, records[0])
            bot.reply_to(message, records[1])
            bot.set_message_reaction(message.chat.id,
                                                message.message_id,
                                                [ReactionTypeEmoji('✍️')],
                                                is_big=True)
            log(f"/records requested by: {get_player_name_formal(current_player)}")
    except Exception as e:
        bot.reply_to(message, constants.UNHANDLED_EXCEPTION_MESSAGE)
        log_error(e)

def build_records_text():
    load_sql_queries()

    global records_template
    with open(constants.RECORDS_TEMPLATE_FILE, "r") as file:
        records_template = file.read()

    text_how_many_games_we_played = database.execute_sql_query_return_one(sql_how_many_games_we_played)
    text_how_many_games_were_cancelled = database.execute_sql_query_return_one(sql_how_many_games_were_cancelled)
    text_win_streaks = database.execute_sql_query_return_many(sql_win_streaks)
    text_losing_streaks = database.execute_sql_query_return_many(sql_losing_streaks)
    text_top_goals_per_game = database.execute_sql_query_return_many(sql_top_goals_per_game)
    text_top_assists_per_game = database.execute_sql_query_return_many(sql_top_assists_per_game)
    text_top_own_goals_per_game = database.execute_sql_query_return_many(sql_top_own_goals_per_game)
    text_win_rate = database.execute_sql_query_return_many(sql_win_rate)
    text_paid_most_money = database.execute_sql_query_return_many(sql_paid_most_money)
    text_played_most_games_for_corn = database.execute_sql_query_return_many(sql_played_most_games_for_corn)
    text_played_most_games_for_tomato = database.execute_sql_query_return_many(sql_played_most_games_for_tomato)
    text_sat_on_chair_most_times = database.execute_sql_query_return_many(sql_sat_on_chair_most_times)
    text_scored_most_own_goals = database.execute_sql_query_return_many(sql_scored_most_own_goals)
    text_top_assists_alltime = database.execute_sql_query_return_many(sql_top_assists_alltime)
    text_top_goals_alltime = database.execute_sql_query_return_many(sql_top_goals_alltime)
    text_top_player_pairs = database.execute_sql_query_return_many(sql_top_player_pairs)
    text_active_win_streaks = database.execute_sql_query_return_many(sql_active_win_streaks)
    text_active_loss_streaks = database.execute_sql_query_return_many(sql_active_loss_streaks)
    text_average_age_and_height = database.execute_sql_query_return_many(sql_average_age_and_height)
    text_attandance_streaks = database.execute_sql_query_return_many(sql_attendance_streaks)
    text_max_goal_difference = database.execute_sql_query_return_many(sql_max_goal_difference)
    text_most_goals_scored_per_game_by_corn = database.execute_sql_query_return_many(sql_most_goals_scored_per_game_by_corn)
    text_most_goals_scored_per_game_by_tomato = database.execute_sql_query_return_many(sql_most_goals_scored_per_game_by_tomato)

    records_template = fill_records_template(records_template, constants.SQL_HOW_MANY_GAMES_WE_PLAYED, text_how_many_games_we_played)
    records_template = fill_records_template(records_template, constants.SQL_HOW_MANY_GAMES_WERE_CANCELLED, text_how_many_games_were_cancelled)
    records_template = fill_records_template(records_template, constants.SQL_TOP_ASSISTS_PER_GAME, format_top_goals(text_top_assists_per_game))
    records_template = fill_records_template(records_template, constants.SQL_TOP_GOALS_PER_GAME, format_top_goals(text_top_goals_per_game))
    records_template = fill_records_template(records_template, constants.SQL_TOP_OWN_GOALS_PER_GAME, format_top_goals(text_top_own_goals_per_game))
    records_template = fill_records_template(records_template, constants.SQL_WHO_HAS_THE_HIGHER_WIN_RATE, format_win_rate(text_win_rate))
    records_template = fill_records_template(records_template, constants.SQL_WHO_PAID_THE_MOST_MONEY, format_who_paid_most_money(text_paid_most_money))
    records_template = fill_records_template(records_template, constants.SQL_WHO_PLAYED_THE_MOST_GAMES_FOR_CORN, format_who_player_most_games_corn(text_played_most_games_for_corn))
    records_template = fill_records_template(records_template, constants.SQL_WHO_PLAYED_THE_MOST_GAMES_FOR_TOMATO, format_who_player_most_games_tomato(text_played_most_games_for_tomato))
    records_template = fill_records_template(records_template, constants.SQL_WHO_SAT_ON_A_CHAIR_THE_MOST_TIMES, format_most_chair(text_sat_on_chair_most_times))
    records_template = fill_records_template(records_template, constants.SQL_WHO_SCORED_MOST_OWN_GOALS, format_most_goals(text_scored_most_own_goals))
    records_template = fill_records_template(records_template, constants.SQL_WIN_STREAKS, format_win_loose_streaks(text_win_streaks))
    records_template = fill_records_template(records_template, constants.SQL_LOSING_STREAKS, format_win_loose_streaks(text_losing_streaks))
    records_template = fill_records_template(records_template, constants.SQL_ACTIVE_WIN_STREAKS, format_win_loose_streaks(text_active_win_streaks))
    records_template = fill_records_template(records_template, constants.SQL_ACTIVE_LOSS_STREAKS, format_win_loose_streaks(text_active_loss_streaks))
    records_template = fill_records_template(records_template, constants.SQL_TOP_ASSISTS_ALLTIME, format_most_goals(text_top_assists_alltime))
    records_template = fill_records_template(records_template, constants.SQL_TOP_GOALS_ALLTIME, format_most_goals(text_top_goals_alltime))
    records_template = fill_records_template(records_template, constants.SQL_TOP_PLAYER_PAIRS, format_player_pairs(text_top_player_pairs))
    records_template = fill_records_template(records_template, constants.SQL_AVERAGE_AGE_AND_HEIGHT, format_average_age_and_height(text_average_age_and_height))
    records_template = fill_records_template(records_template, constants.SQL_ATTENDANCE_STREAKS, format_attendance_streaks(text_attandance_streaks))
    records_template = fill_records_template(records_template, constants.SQL_MAX_GOAL_DIFFERENCE, format_max_goal_difference(text_max_goal_difference))
    records_template = fill_records_template(records_template, constants.SQL_MOST_GOALS_SCORED_PER_GAME_BY_CORN, format_most_goals_scored_per_game_by_team(text_most_goals_scored_per_game_by_corn))
    records_template = fill_records_template(records_template, constants.SQL_MOST_GOALS_SCORED_PER_GAME_BY_TOMATO, format_most_goals_scored_per_game_by_team(text_most_goals_scored_per_game_by_tomato))
    records_template = records_template.replace("[!]", "")

    parts = records_template.split("\n\n\n")

    return parts

def load_sql_queries():
    global sql_how_many_games_we_played
    with open(f"SQL Queries/{constants.SQL_HOW_MANY_GAMES_WE_PLAYED}" , "r") as file:
        sql_how_many_games_we_played = file.read()

    global sql_how_many_games_were_cancelled
    with open(f"SQL Queries/{constants.SQL_HOW_MANY_GAMES_WERE_CANCELLED}" , "r") as file:
        sql_how_many_games_were_cancelled = file.read()

    global sql_win_streaks
    with open(f"SQL Queries/{constants.SQL_WIN_STREAKS}" , "r") as file:
        sql_win_streaks = file.read()

    global sql_losing_streaks
    with open(f"SQL Queries/{constants.SQL_LOSING_STREAKS}" , "r") as file:
        sql_losing_streaks = file.read()

    global sql_top_goals_per_game
    with open(f"SQL Queries/{constants.SQL_TOP_GOALS_PER_GAME}" , "r") as file:
        sql_top_goals_per_game = file.read()

    global sql_top_own_goals_per_game
    with open(f"SQL Queries/{constants.SQL_TOP_OWN_GOALS_PER_GAME}" , "r") as file:
        sql_top_own_goals_per_game = file.read()

    global sql_top_assists_per_game
    with open(f"SQL Queries/{constants.SQL_TOP_ASSISTS_PER_GAME}" , "r") as file:
        sql_top_assists_per_game = file.read()

    global sql_win_rate
    with open(f"SQL Queries/{constants.SQL_WHO_HAS_THE_HIGHER_WIN_RATE}" , "r") as file:
        sql_win_rate = file.read()

    global sql_paid_most_money
    with open(f"SQL Queries/{constants.SQL_WHO_PAID_THE_MOST_MONEY}" , "r") as file:
        sql_paid_most_money = file.read()

    global sql_played_most_games_for_corn
    with open(f"SQL Queries/{constants.SQL_WHO_PLAYED_THE_MOST_GAMES_FOR_CORN}" , "r") as file:
        sql_played_most_games_for_corn = file.read()

    global sql_played_most_games_for_tomato
    with open(f"SQL Queries/{constants.SQL_WHO_PLAYED_THE_MOST_GAMES_FOR_TOMATO}" , "r") as file:
        sql_played_most_games_for_tomato = file.read()

    global sql_sat_on_chair_most_times
    with open(f"SQL Queries/{constants.SQL_WHO_SAT_ON_A_CHAIR_THE_MOST_TIMES}" , "r") as file:
        sql_sat_on_chair_most_times = file.read()

    global sql_scored_most_own_goals
    with open(f"SQL Queries/{constants.SQL_WHO_SCORED_MOST_OWN_GOALS}" , "r") as file:
        sql_scored_most_own_goals = file.read()

    global sql_top_assists_alltime
    with open(f"SQL Queries/{constants.SQL_TOP_ASSISTS_ALLTIME}" , "r") as file:
        sql_top_assists_alltime = file.read()

    global sql_top_goals_alltime
    with open(f"SQL Queries/{constants.SQL_TOP_GOALS_ALLTIME}" , "r") as file:
        sql_top_goals_alltime = file.read()

    global sql_top_player_pairs
    with open(f"SQL Queries/{constants.SQL_TOP_PLAYER_PAIRS}" , "r") as file:
        sql_top_player_pairs = file.read()

    global sql_active_win_streaks
    with open(f"SQL Queries/{constants.SQL_ACTIVE_WIN_STREAKS}" , "r") as file:
        sql_active_win_streaks = file.read()

    global sql_active_loss_streaks
    with open(f"SQL Queries/{constants.SQL_ACTIVE_LOSS_STREAKS}" , "r") as file:
        sql_active_loss_streaks = file.read()

    global sql_average_age_and_height
    with open(f"SQL Queries/{constants.SQL_AVERAGE_AGE_AND_HEIGHT}" , "r") as file:
        sql_average_age_and_height = file.read()

    global sql_attendance_streaks
    with open(f"SQL Queries/{constants.SQL_ATTENDANCE_STREAKS}" , "r") as file:
        sql_attendance_streaks = file.read()

    global sql_max_goal_difference
    with open(f"SQL Queries/{constants.SQL_MAX_GOAL_DIFFERENCE}" , "r") as file:
        sql_max_goal_difference = file.read()

    global sql_most_goals_scored_per_game_by_corn
    with open(f"SQL Queries/{constants.SQL_MOST_GOALS_SCORED_PER_GAME_BY_CORN}" , "r") as file:
        sql_most_goals_scored_per_game_by_corn = file.read()

    global sql_most_goals_scored_per_game_by_tomato
    with open(f"SQL Queries/{constants.SQL_MOST_GOALS_SCORED_PER_GAME_BY_TOMATO}" , "r") as file:
        sql_most_goals_scored_per_game_by_tomato = file.read()

def format_win_loose_streaks(response_from_database):
    result=""
    for record in response_from_database:
        result = result + f"🙌 {record[0]} - {record[1]} ({format_date(record[2])} - {format_date(record[3])})\n"
    return result

def format_top_goals(response_from_database):
    result=""
    for record in response_from_database:
        result = result + f"⚽️ {record[0]} - {record[1]} ({format_date(record[2])})\n"
    return result

def format_win_rate(response_from_database):
    result=""
    for record in response_from_database:
        result = result + f"🔥 {record[0]} - {record[3]}%\n"
    return result

def format_who_paid_most_money(response_from_database):
    result=""
    for record in response_from_database:
        result = result + f"💲 {record[0]} - {record[1]} р.\n"
    return result

def format_who_player_most_games_corn(response_from_database):
    result=""
    for record in response_from_database:
        result = result + f"🌽 {record[0]} - {record[1]}\n"
    return result

def format_who_player_most_games_tomato(response_from_database):
    result=""
    for record in response_from_database:
        result = result + f"🍅 {record[0]} - {record[1]}\n"
    return result

def format_most_goals(response_from_database):
    result=""
    for record in response_from_database:
        result = result + f"⚽️ {record[0]} - {record[1]}\n"
    return result

def format_most_chair(response_from_database):
    result=""
    for record in response_from_database:
        result = result + f"🪑 {record[0]} - {record[1]}\n"
    return result

def format_player_pairs(response_from_database):
    result=""
    for record in response_from_database:
        squad = ""
        if record[6] == constants.SQUAD_TOMATO:
            squad = constants.SQUAD_TOMATO_EMOJI
        else:
            if record[6] == constants.SQUAD_CORN:
                squad = constants.SQUAD_CORN_EMOJI
        result = result + f"{squad} {record[0]} + {record[1]} = {record[2]} игр\n"
    return result

def format_average_age_and_height(average_age_and_height_from_db):
    return f"👢 Средний рост: {average_age_and_height_from_db[0][0]:.2f} см.\n👴 Средний возраст: {average_age_and_height_from_db[0][1]:.2f} лет.\n"

def format_attendance_streaks(response_from_database):
    result=""
    for record in response_from_database:
        result = result + f"🔁 {record[0]} - {record[1]} ({format_date(record[2])} - {format_date(record[3])})\n"
    return result

def format_max_goal_difference(response_from_database):
    result=""
    for record in response_from_database:
        result = result + f"🔝 {format_date(record[0])}: 🌽 {record[1]}:{record[2]} 🍅 (разница {record[3]})\n"
    return result

def format_most_goals_scored_per_game_by_team(response_from_database):
    result=""
    for record in response_from_database:
        result = result + f"🔝 {format_date(record[0])}: 🌽 {record[1]}:{record[2]} 🍅\n"
    return result

def format_max_total_goals_per_game_by_two_teams(response_from_database):
    result=""
    for record in response_from_database:
        result = result + f"🔝 {format_date(record[0])}: 🌽 {record[1]}:{record[2]} 🍅 (всего голов {record[3]})\n"
    return result