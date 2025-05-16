from logger import log, log_error
from telebot.types import ReactionTypeEmoji
from helpers import get_arguments, get_next_matchday, get_next_matchday_formatted, get_today_minsk_time
from common import add_player_if_not_existant, validate_access_no_game_registration_needed, text_to_image, get_player_name_extended, reply_only_CEO_can_do_it, validate_CEO_zone_no_arguments
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
        player = add_player_if_not_existant(message.from_user.first_name,
                                            message.from_user.last_name,
                                            message.from_user.username,
                                            message.from_user.id)
        if validate_access_no_game_registration_needed(message.chat.id, player, bot, message):
            if validate_CEO_zone_no_arguments(message.from_user.id):
                command_and_argument_split = message.text.split('\n', 1)
                if len(command_and_argument_split)>1:
                    date_params = command_and_argument_split[0].split(' ', 1)
                    if len(date_params) > 1:
                        date = None
                        try:
                            date = datetime.datetime.strptime(date_params[1], "%b %d, %Y")
                        except:
                            bot.reply_to(message, "С датой что-то неправильно! Вот в таком формате пиши: /register_money May 17, 2025")
                        if date is not None:
                            parts = command_and_argument_split[1].split('\n')
                            game_id = database.get_game_id_without_adding_new(date)
                            output = "Изменение балансов:\n"
                            if game_id is not None:
                                for line in parts:
                                    lineup_player_params = re.split(r'[\s]+', line.strip(),3)
                                    first_name = lineup_player_params[0]
                                    last_name = lineup_player_params[1]
                                    lineup_player = database.find_player_by_name(first_name, last_name)
                                    if lineup_player is not None:
                                        player_id = lineup_player[7]
                                        money_given = lineup_player_params[2]
                                        comment = ""
                                        if len(lineup_player_params)>3:
                                            comment = lineup_player_params[3]
                                        if money_given.isdigit() is False:
                                            bot.reply_to(message, f"Что-то не то с данными по деньгам для этого игрока: {first_name} {last_name}. Давай исправь там что-нибудь и заново запускивай команду.")
                                        else:
                                            money_given_int = int(money_given)
                                            balance_change_int = money_given_int - constants.COST_OF_1_GAME
                                            database.add_matchday_money(player_id,game_id,money_given,balance_change_int,comment)
                                            output += f"{first_name} {last_name}: {balance_change_int}\n"
                                    else:
                                        bot.reply_to(message, f"Вот этого игрока не смог найти в базе: {first_name} {last_name}. Давай исправь там что-нибудь и заново запускивай команду.")
                                        log(f"Can't find player to register in a lineup: {lineup_player_params}")
                                log(f"Game stats successfully registered")
                                bot.reply_to(message, "✅ Бухгалтерия записана! Деньги мутятся, бухгалтерия крутится! Ванька едет в Египет! Красава!")
                                bot.reply_to(message, output)
                                bot.set_message_reaction(message.chat.id,
                                                    message.message_id,
                                                    [ReactionTypeEmoji('✍️')],
                                                    is_big=True)
                            else:
                                bot.reply_to(message, "Не могу найти в базе такой игровой день. Может, дату какую-то не ту указал? Должна быть по-любому суббота. И не должна быть далеко в будущем.")
                    else:
                        bot.reply_to(message, "Дату надо указать! Без даты ничего не получится. Откуда ж я знаю за какой день бухгалтерию записывать? Вот в таком формате пиши: /register_money May 17, 2025")
                else:
                    bot.reply_to(message, "Пришли даннные кто сколько сдал! Ты ж ничего не прислал. Знаешь в каком формате прислать? Сам разберись!")
            else:
                reply_only_CEO_can_do_it(bot, message)
    except Exception as e:
        bot.reply_to(message, constants.UNHANDLED_EXCEPTION_MESSAGE)
        log_error(e)
        