from logger import log, log_error
from telebot.types import ReactionTypeEmoji
from helpers import get_arguments, get_next_matchday, get_next_matchday_formatted, get_today_minsk_time
from common import add_player_if_not_existant, validate_access_no_game_registration_needed, text_to_image, get_player_name_formal, reply_only_CEO_can_do_it, validate_CEO_zone
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
            table = pt.PrettyTable(['Игрок', 'Баланс'])
            table.align['Игрок'] = 'l'
            table.align['Баланс'] = 'с'
            table.hrules = True
            players_balance = database.get_players_balance()
            for balance_item in players_balance:
                player_name = f"{balance_item[1]} {balance_item[2]}"
                balance = balance_item[3]
                if balance != 0:
                    table.add_row([player_name, balance])
            photo = text_to_image(table.get_string(), image_size=(320, 1200), font_size=11)
            bot.send_photo(message.chat.id, photo, reply_to_message_id=message.message_id)
            log(f"Successfullty provided players balance /balance. Requested by: {get_player_name_formal(current_player)}")
    except Exception as e:
        bot.reply_to(message, constants.UNHANDLED_EXCEPTION_MESSAGE)
        log_error(e)
        