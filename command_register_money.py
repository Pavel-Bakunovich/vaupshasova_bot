from logger import log, log_error
from telegram import ReactionTypeEmoji
from helpers import get_arguments, get_next_matchday, get_next_matchday_formatted, get_today_minsk_time
from common import add_player_if_not_existant, validate_access_no_game_registration_needed, get_player_name_formal, text_to_image, get_player_name_extended, reply_only_CEO_can_do_it, validate_CEO_zone_no_arguments
import database
import constants
import prettytable as pt
import datetime
import re

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
            if validate_CEO_zone_no_arguments(message.from_user.id):
                command_and_argument_split = message.text.split('\n', 1)
                if len(command_and_argument_split)>1:
                    date_params = command_and_argument_split[0].split(' ', 1)
                    if len(date_params) > 1:
                        date = None
                        try:
                            date = datetime.datetime.strptime(date_params[1], "%b %d, %Y")
                        except:
                            await bot.reply_to(message, "С датой что-то неправильно! Вот в таком формате пиши: /register_money May 17, 2025")
                        if date is not None:
                            parts = command_and_argument_split[1].split('\n')
                            game_id = database.get_game_id_without_adding_new(date)
                            output = "После внесения денег: сколько списалось со счета / оставшийся баланс\n"
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
                                            await bot.reply_to(message, f"Что-то не то с данными по деньгам для этого игрока: {first_name} {last_name}. Давай исправь там что-нибудь и заново запускивай команду.")
                                        else:
                                            money_given_float = float(money_given)
                                            balance_change_int = money_given_float - constants.COST_OF_1_GAME_PER_PLAYER
                                            database.add_matchday_money(player_id,game_id,money_given_float,balance_change_int,comment)
                                            individual_balance = database.get_individual_balance(player_id)[0]
                                            output += f"💰 {first_name} {last_name}: {balance_change_int} р. / {individual_balance} р.\n"
                                    else:
                                        await bot.reply_to(message, f"Вот этого игрока не смог найти в базе: {first_name} {last_name}. Давай исправь там что-нибудь и заново запускивай команду.")
                                        log(f"Can't find player to register in a lineup: {lineup_player_params}")
                                log(f"/register_money requested by: {get_player_name_formal(current_player)}")
                                await bot.reply_to(message, "✅ Бухгалтерия записана! Деньги мутятся, бухгалтерия крутится! Ванька едет в Египет! А может и в Дубаи! Красава!")
                                await bot.reply_to(message, output)
                                await bot.set_message_reaction(message.chat.id,
                                                    message.message_id,
                                                    [ReactionTypeEmoji('✍️')],
                                                    is_big=True)
                            else:
                                await bot.reply_to(message, "Не могу найти в базе такой игровой день. Может, дату какую-то не ту указал? Должна быть по-любому суббота. И не должна быть далеко в будущем.")
                    else:
                        await bot.reply_to(message, "Дату надо указать! Без даты ничего не получится. Откуда ж я знаю за какой день бухгалтерию записывать? Вот в таком формате пиши: /register_money May 17, 2025")
                else:
                    await bot.reply_to(message, "Пришли данные кто сколько сдал! Ты ж ничего не прислал. Знаешь в каком формате прислать? Сам разберись!")
            else:
                await reply_only_CEO_can_do_it(bot, message)
    except Exception as e:
        await bot.reply_to(message, constants.UNHANDLED_EXCEPTION_MESSAGE)
        log_error(e)
        