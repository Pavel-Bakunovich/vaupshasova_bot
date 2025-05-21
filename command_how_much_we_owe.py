from logger import log, log_error
from telebot.types import ReactionTypeEmoji
from helpers import format_date, get_arguments, get_next_matchday, get_next_matchday_formatted, get_today_minsk_time
from common import add_player_if_not_existant, validate_access_no_game_registration_needed, get_player_name_formal, text_to_image, get_player_name_extended, reply_only_CEO_can_do_it, validate_CEO_zone
import database
import constants
import prettytable as pt

def execute(message, bot):
    try:
        current_player = add_player_if_not_existant(message.from_user.first_name,
                                            message.from_user.last_name,
                                            message.from_user.username,
                                            message.from_user.id)
        if validate_access_no_game_registration_needed(message.chat.id, current_player, bot, message):
            games_since_last_layment_for_pitch = database.how_many_games_since_last_layment_for_pitch()
            date_of_last_layment_for_pitch = format_date(database.date_of_last_layment_for_pitch())
            how_much_we_owe = games_since_last_layment_for_pitch * constants.COST_OF_1_GAME
            bot.reply_to(message, f"Последний раз мы платили за поле {date_of_last_layment_for_pitch}. С того момента уже сыграли {games_since_last_layment_for_pitch} игр (в том числе считая следующую субботу).\n💲 Сумма к оплате: {how_much_we_owe} р.")
            log(f"/how_much_we_owe requested by: {get_player_name_formal(current_player)}")
    except Exception as e:
        bot.reply_to(message, constants.UNHANDLED_EXCEPTION_MESSAGE)
        log_error(e)
        