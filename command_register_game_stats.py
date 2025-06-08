from logger import log, log_error
from telebot.types import ReactionTypeEmoji
from helpers import get_arguments, get_next_matchday
from common import add_player_if_not_existant, validate_access_no_game_registration_needed, get_player_name_formal, reply_only_CEO_can_do_it, validate_CEO_zone
import database
import constants
import re
import datetime

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
            command_and_argument_split = message.text.split('\n', 1)
            if len(command_and_argument_split)>1:
                date_params = command_and_argument_split[0].split(' ', 1)
                if len(date_params) > 1:
                    date = None
                    try:
                        date = datetime.datetime.strptime(date_params[1], "%b %d, %Y")
                    except:
                        bot.reply_to(message, "С датой что-то неправильно! Вот в таком формате пиши: /register_game_stats May 17, 2025")
                    if date is not None:
                        parts = command_and_argument_split[1].split('\n')
                        game_id = database.get_game_id_without_adding_new(date)
                        if game_id is not None:
                            corn_scored_goals_counter = 0
                            tomato_scored_goals_counter = 0
                            squad = database.get_squad(date)
                            for line in parts:
                                lineup_player_params = re.split(r'[\s]+', line.strip())
                                first_name = lineup_player_params[0]
                                last_name = lineup_player_params[1]
                                lineup_player = database.find_player_by_name(first_name, last_name)
                                is_data_valid = False
                                if lineup_player is not None:
                                    player_id = lineup_player[7]
                                    try:
                                        goals = lineup_player_params[2]
                                        assists = lineup_player_params[3]
                                        own_goals = lineup_player_params[4]
                                        is_data_valid = True
                                    except:
                                        bot.reply_to(message, f"Что-то не то с данными по голам/асистам/автоголам для этого игрока: {first_name} {last_name}. Скорее всего ты не ввел все цифры. Напротив каждого имени надо вводить 3 цифры через запятую - <голы> <асисты> <автоголы>. Давай исправь там что-нибудь и заново запускивай команду.")
                                    
                                    if is_data_valid is True:
                                        if goals.isdigit() is False or assists.isdigit() is False or own_goals.isdigit() is False:
                                            bot.reply_to(message, f"Что-то не то с данными по голам/асистам/автоголам для этого игрока: {first_name} {last_name}. Скорее всего ты ввел не цифру, а текст какой-то. Давай исправь там что-нибудь и заново запускивай команду.")
                                        else:
                                            database.add_game_stats(player_id,game_id,goals,assists,own_goals)
                                            if get_player_team(player_id, squad) == constants.SQUAD_CORN:
                                                corn_scored_goals_counter += int(goals)
                                                if int(own_goals) > 0:
                                                    tomato_scored_goals_counter += int(own_goals)
                                            else:
                                                tomato_scored_goals_counter += int(goals)
                                                if int(own_goals) > 0:
                                                    corn_scored_goals_counter += int(own_goals)
                                else:
                                    bot.reply_to(message, f"Вот этого игрока не смог найти в базе: {first_name} {last_name}. Давай исправь там что-нибудь и заново запускивай команду.")
                                    log(f"Can't find player to register in a lineup: {lineup_player_params}")
                            database.register_game_score(game_id,corn_scored_goals_counter,tomato_scored_goals_counter)
                            log(f"/register_game_stats requested by: {get_player_name_formal(current_player)}")
                            bot.reply_to(message, f"✅ Статистика записана! Цифры мутятся, статистика крутится! Красава!\nСчет матча 🌽 {corn_scored_goals_counter}:{tomato_scored_goals_counter} 🍅")
                            bot.set_message_reaction(message.chat.id,
                                                message.message_id,
                                                [ReactionTypeEmoji('✍️')],
                                                is_big=True)
                        else:
                            bot.reply_to(message, "Не могу найти в базе такой игровой день. Может, дату какую-то не ту указал? Должна быть по-любому суббота. И не должна быть далеко в будущем.")
                else:
                    bot.reply_to(message, "Дату надо указать! Без даты ничего не получится. Откуда ж я знаю за какой день эту статистику записывать? Вот в таком формате пиши: /register_game_stats May 17, 2025")
            else:
                bot.reply_to(message, "Пришли голы/асисты/автоголы! Ты ж ничего не прислал. Знаешь в каком формате прислать? Сам разберись!")
    except Exception as e:
        bot.reply_to(message, constants.UNHANDLED_EXCEPTION_MESSAGE)
        log_error(e)

def get_player_team(player_id, squad):
    for item in squad:
        if item[0] == player_id:
            return item[10]



'''
/register_game_stats May 17, 2025
Ваня Шмарловский 4 5 0
Костя Ведьгун 3 2 0
Юра Лупинов 0 8 1
Сергей Лисовский 4 9 0
Олег Малахов 3 2 0
Сергей Мшар 4 6 1
Рома Махныткин 14 4 0
Леша Юрченко 3 4 0
Дима Шилько1 1 0
Дима Приставнев 4 2 0
Олег Будевич 2 4 0
Паша Бакунович 4 3 0
'''
