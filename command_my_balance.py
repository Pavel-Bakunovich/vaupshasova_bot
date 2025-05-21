from logger import log, log_error
from telebot.types import ReactionTypeEmoji
from helpers import get_arguments, get_next_matchday, get_next_matchday_formatted, get_today_minsk_time, format_date
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
            table = pt.PrettyTable(['N','Дата', 'Сдал', 'Изменение баланса', 'Баланс на дату'])
            table.align['N'] = 'c'
            table.align['Дата'] = 'l'
            table.align['Сдал'] = 'c'
            table.align['Изменение баланса'] = 'c'
            table.align['Баланс на дату'] = 'c'
            table.hrules = True

            payments_history = database.get_payments_history(current_player[7])
            i = 1  
            for payment in payments_history:
                date = payment[0]
                money_given = payment[1]
                balance_change = payment[2]
                balance_by_date = payment[3]
                table.add_row([i, format_date(date), f"{money_given} р.", f"{balance_change} р.",f"{balance_by_date} р."])
                i+=1

            individual_balance = database.get_individual_balance(current_player[7])

            output = f"{get_player_name_formal(current_player)}.\nТекущий баланс: {individual_balance[0]} р.\nСдал денег за всю историю: {individual_balance[1]} р.\n{table.get_string()}"
            photo = text_to_image(output,image_size=(600, 900),font_size=12)
            bot.send_photo(message.chat.id, photo, reply_to_message_id=message.message_id)
            log(f"/my_balance requested by: {get_player_name_formal(current_player)}")
    except Exception as e:
        bot.reply_to(message, constants.UNHANDLED_EXCEPTION_MESSAGE)
        log_error(e)
        
