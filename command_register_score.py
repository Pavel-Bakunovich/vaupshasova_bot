from logger import log, log_error
from telegram import ReactionTypeEmoji
from helpers import get_arguments, get_next_matchday, get_next_matchday_formatted, get_today_minsk_time
from common import add_player_if_not_existant, validate_access_no_game_registration_needed, get_player_name_formal, text_to_image, get_player_name_extended, reply_only_CEO_can_do_it, validate_CEO_zone
import database
import constants
import prettytable as pt
import datetime

async def execute(message, bot):
    try:
        await bot.set_message_reaction(message.chat.id,
                                            message.message_id,
                                            [ReactionTypeEmoji('👾')],
                                            is_big=True)
        current_player = add_player_if_not_existant(message.from_user.first_name,
                                            message.from_user.last_name,
                                            message.from_user.username,
                                            message.from_user.id)
        if await validate_access_no_game_registration_needed(message.chat.id, current_player, bot, message):
            command_and_argument_split = message.text.split('\n', 1)
            if len(command_and_argument_split)>1:
                date_params = command_and_argument_split[0].split(' ', 1)
                if len(date_params) > 1:
                    date = None
                    try:
                        date = datetime.datetime.strptime(date_params[1], "%b %d, %Y")
                    except:
                        await bot.reply_to(message, "С датой что-то неправильно! Вот в таком формате пиши: /register_score May 17, 2025...")
                    if date is not None:
                        score_params = command_and_argument_split[1].split(':',1)
                        score_corn = score_params[0]
                        score_tomato = score_params[1]
                        game_id = database.get_game_id_without_adding_new(date)
                        
                        if game_id is not None:
                            if score_corn.isdigit() is False or score_tomato.isdigit() is False:
                                await bot.reply_to(message, f"Что-то не то с цифрами. Введи ты уже нормально! Вот в таком формате надо: <🌽>:<🍅>")
                            else:
                                database.register_game_score(game_id, score_corn, score_tomato)
                        else:
                            await bot.reply_to(message, "Не могу найти в базе такой игровой день. Может, дату какую-то не ту указал? Должна быть по-любому суббота. И не должна быть далеко в будущем.")
                
                        log(f"Game score successfully registered: 🌽 {score_corn}:{score_tomato} 🍅")
                        await bot.reply_to(message, f"✅ Счет записал. 🌽 {score_corn}:{score_tomato} 🍅")
                        await bot.set_message_reaction(message.chat.id,
                                            message.message_id,
                                            [ReactionTypeEmoji('✍️')],
                                    is_big=True)
                        log(f"/register_score requested by: {get_player_name_formal(current_player)}")
            else:
                await bot.reply_to(message, "Что-то не то. Укажи дату, потом переход на новую строку и счет вот в таком формате <🌽>:<🍅>")
    except Exception as e:
        await bot.reply_to(message, constants.UNHANDLED_EXCEPTION_MESSAGE)
        log_error(e)
        
