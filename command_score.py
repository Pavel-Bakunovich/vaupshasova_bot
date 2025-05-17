from logger import log, log_error
from telebot.types import ReactionTypeEmoji
from helpers import format_date
from common import add_player_if_not_existant, validate_access_no_game_registration_needed, text_to_image, get_player_name_formal, reply_only_CEO_can_do_it, validate_CEO_zone
import database
import constants
import prettytable as pt
import datetime

def execute(message, bot):
    try:
        current_player = add_player_if_not_existant(message.from_user.first_name,
                                            message.from_user.last_name,
                                            message.from_user.username,
                                            message.from_user.id)
        if validate_access_no_game_registration_needed(message.chat.id, current_player, bot, message):
            table = pt.PrettyTable(['Дата', 'К',':', 'П', 'Оплачено', 'Состоялась?'])
            table.align['Дата'] = 'c'
            table.align['К'] = 'r'
            table.align[':'] = 'c'
            table.align['П'] = 'l'
            table.align['Оплачено'] = 'c'
            table.align['Состоялась?'] = 'c'
            table.hrules = True
            scores = database.get_scores()
            for game_score in scores:
                date = format_date(game_score[0])
                score_corn = game_score[1] if game_score[1] is not None else ""
                score_tomato = game_score[2] if game_score[2] is not None else ""
                paid_for_pitch = f"{game_score[3]} р." if game_score[3] is not None else ""
                played = "Отменили" if game_score[4] == False else ""
                table.add_row([date, score_corn, ":", score_tomato, paid_for_pitch, played])
            photo = text_to_image(table.get_string(), image_size=(650, 950))
            bot.send_photo(message.chat.id, photo, reply_to_message_id=message.message_id)
            log(f"Successfullty provided game scores /score. Requested by: {get_player_name_formal(current_player)}")
    except Exception as e:
        bot.reply_to(message, constants.UNHANDLED_EXCEPTION_MESSAGE)
        log_error(e)
        