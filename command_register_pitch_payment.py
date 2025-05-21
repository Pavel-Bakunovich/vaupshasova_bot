from logger import log, log_error
from telebot.types import ReactionTypeEmoji
from helpers import get_arguments, get_next_matchday, get_next_matchday_formatted, get_today_minsk_time
from common import add_player_if_not_existant, validate_access_no_game_registration_needed, get_player_name_formal, text_to_image, get_player_name_extended, reply_only_CEO_can_do_it, validate_CEO_zone_no_arguments
import database
import constants
import prettytable as pt
import datetime
import re

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
            if validate_CEO_zone_no_arguments(message.from_user.id):
                command_and_argument_split = message.text.split('\n', 1)
                if len(command_and_argument_split)>1:
                    date_params = command_and_argument_split[0].split(' ', 1)
                    if len(date_params) > 1:
                        date = None
                        try:
                            date = datetime.datetime.strptime(date_params[1], "%b %d, %Y")
                        except:
                            bot.reply_to(message, "С датой что-то неправильно! Вот в таком формате пиши: /register_pitch_payment May 17, 2025")
                        if date is not None:
                            parts = command_and_argument_split[1].split('\n')
                            
                            payment_sum = parts[0]

                            game_id = database.get_game_id_without_adding_new(date)
                            
                            if game_id is not None:
                                if payment_sum.isdigit() is False:
                                    bot.reply_to(message, "Не пойму что за сумма. Напиши нормально сумму.")    
                                else:
                                    database.register_pitch_payment(game_id, float(payment_sum))
                                    log(f"Pitch payment successfully registered")
                                    bot.reply_to(message, "✅ Оплата за поле записана! Деньги мутятся, бухгалтерия крутится! Красава!")
                                    bot.set_message_reaction(message.chat.id,
                                                        message.message_id,
                                                        [ReactionTypeEmoji('✍️')],
                                                        is_big=True)
                                    log(f"/register_pitch_payment requested by: {get_player_name_formal(current_player)}")
                            else:
                                bot.reply_to(message, "Не могу найти в базе такой игровой день. Может, дату какую-то не ту указал? Должна быть по-любому суббота. И не должна быть далеко в будущем.")
                    else:
                        bot.reply_to(message, "Дату надо указать! Без даты ничего не получится. Откуда ж я знаю за какой день записывать, что мы оплатили поле? Вот в таком формате пиши: /register_pitch_payment May 17, 2025")
                else:
                    bot.reply_to(message, "Пришли даннные сколько мы заплатили за поле! Ты ж ничего не прислал.")
            else:
                reply_only_CEO_can_do_it(bot, message)  
    except Exception as e:
        bot.reply_to(message, constants.UNHANDLED_EXCEPTION_MESSAGE)
        log_error(e)
        
