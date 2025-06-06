from logger import log, log_error
from telebot.types import ReactionTypeEmoji
from helpers import get_next_matchday, get_next_matchday_formatted, get_today_minsk_time
from common import add_player_if_not_existant, validate_access_no_game_registration_needed, text_to_image, get_player_name_formal, reply_only_CEO_can_do_it, validate_CEO_zone
import database
import constants
import prettytable as pt

records_template = ""

sql_how_many_games_we_played = ""
sql_how_many_games_were_cancelled = ""

text_how_many_games_we_played = ""
text_how_many_games_were_cancelled = ""

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
            load_sql_queries()

            global records_template
            with open(constants.RECORDS_TEMPLATE_FILE, "r") as file:
                records_template = file.read()

            text_how_many_games_we_played = database.execute_sql_query_return_one(sql_how_many_games_we_played)
            text_how_many_games_were_cancelled = database.execute_sql_query_return_one(sql_how_many_games_were_cancelled)

            records_template = fill_records_template(records_template, constants.SQL_HOW_MANY_GAMES_WE_PLAYED, text_how_many_games_we_played)
            records_template = fill_records_template(records_template, constants.SQL_HOW_MANY_GAMES_WERE_CANCELLED, text_how_many_games_were_cancelled)
            records_template = fill_records_template(records_template, constants.SQL_TOP_ASSISTS_PER_GAME, "?")
            records_template = fill_records_template(records_template, constants.SQL_TOP_GOALS_PER_GAME, "?")
            records_template = fill_records_template(records_template, constants.SQL_TOP_OWN_GOALS_PER_GAME, "?")
            records_template = fill_records_template(records_template, constants.SQL_WHO_HAS_THE_HIGHER_WIN_RATE, "?")
            records_template = fill_records_template(records_template, constants.SQL_WHO_PAID_THE_MOST_MONEY, "?")
            records_template = fill_records_template(records_template, constants.SQL_WHO_PLAYED_THE_MOST_GAMES_FOR_CORN, "?")
            records_template = fill_records_template(records_template, constants.SQL_WHO_PLAYED_THE_MOST_GAMES_FOR_TOMATO, "?")
            records_template = fill_records_template(records_template, constants.SQL_WHO_SAT_ON_A_CHAIR_THE_MOST_TIMES, "?")
            records_template = fill_records_template(records_template, constants.SQL_WHO_SCORED_MOST_OWN_GOALS, "?")
            records_template = fill_records_template(records_template, constants.SQL_WIN_STREAKS, "?")
            records_template = fill_records_template(records_template, constants.SQL_LOSING_STREAKS, "?")

            bot.reply_to(message, records_template, parse_mode='MarkdownV2')
            bot.set_message_reaction(message.chat.id,
                                                message.message_id,
                                                [ReactionTypeEmoji('✍️')],
                                                is_big=True)
            log(f"/records requested by: {get_player_name_formal(current_player)}")
    except Exception as e:
        bot.reply_to(message, constants.UNHANDLED_EXCEPTION_MESSAGE)
        log_error(e)

def load_sql_queries():
    global sql_how_many_games_we_played
    with open(f"SQL Queries/{constants.SQL_HOW_MANY_GAMES_WE_PLAYED}" , "r") as file:
        sql_how_many_games_we_played = file.read()

    global sql_how_many_games_were_cancelled
    with open(f"SQL Queries/{constants.SQL_HOW_MANY_GAMES_WERE_CANCELLED}" , "r") as file:
        sql_how_many_games_were_cancelled = file.read()

def fill_records_template(template, replace_to, replace_with):
    return template.replace("{"+replace_to+"}", str(replace_with))