from logger import log, log_error
from telebot.types import ReactionTypeEmoji
from helpers import get_next_matchday, get_next_matchday_formatted, get_today_minsk_time, format_date, escape_markdown
from common import add_player_if_not_existant, validate_access_no_game_registration_needed, text_to_image, get_player_name_formal, reply_only_CEO_can_do_it, validate_CEO_zone
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

text_how_many_games_we_played = ""
text_how_many_games_were_cancelled = ""
text_losing_streaks = ""
text_top_goals_per_game = ""
text_top_assists_per_game = ""
text_top_own_goals_per_game = ""

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
            build_records_text()
            bot.reply_to(message, records_template, parse_mode='MarkdownV2')
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

    records_template = fill_records_template(records_template, constants.SQL_HOW_MANY_GAMES_WE_PLAYED, text_how_many_games_we_played)
    records_template = fill_records_template(records_template, constants.SQL_HOW_MANY_GAMES_WERE_CANCELLED, text_how_many_games_were_cancelled)
    records_template = fill_records_template(records_template, constants.SQL_TOP_ASSISTS_PER_GAME, format_top_goals(text_top_assists_per_game))
    records_template = fill_records_template(records_template, constants.SQL_TOP_GOALS_PER_GAME, format_top_goals(text_top_goals_per_game))
    records_template = fill_records_template(records_template, constants.SQL_TOP_OWN_GOALS_PER_GAME, format_top_goals(text_top_own_goals_per_game))
    records_template = fill_records_template(records_template, constants.SQL_WHO_HAS_THE_HIGHER_WIN_RATE, "?")
    records_template = fill_records_template(records_template, constants.SQL_WHO_PAID_THE_MOST_MONEY, "?")
    records_template = fill_records_template(records_template, constants.SQL_WHO_PLAYED_THE_MOST_GAMES_FOR_CORN, "?")
    records_template = fill_records_template(records_template, constants.SQL_WHO_PLAYED_THE_MOST_GAMES_FOR_TOMATO, "?")
    records_template = fill_records_template(records_template, constants.SQL_WHO_SAT_ON_A_CHAIR_THE_MOST_TIMES, "?")
    records_template = fill_records_template(records_template, constants.SQL_WHO_SCORED_MOST_OWN_GOALS, "?")
    records_template = fill_records_template(records_template, constants.SQL_WIN_STREAKS, format_win_loose_streaks(text_win_streaks))
    records_template = fill_records_template(records_template, constants.SQL_LOSING_STREAKS, format_win_loose_streaks(text_losing_streaks))

    return records_template

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

def format_win_loose_streaks(response_from_database):
    result=""
    for record in response_from_database:
        result = result + escape_markdown(f"🔥 {record[0]} - {record[1]} ({format_date(record[2])} - {format_date(record[3])})\n")
    return result

def format_top_goals(response_from_database):
    result=""
    for record in response_from_database:
        result = result + escape_markdown(f"🔥 {record[0]} - {record[1]} ({format_date(record[2])})\n")
    return result

def fill_records_template(template, replace_to, replace_with):
    return template.replace("{"+replace_to+"}", str(replace_with))