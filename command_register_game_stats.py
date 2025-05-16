from logger import log, log_error
from telebot.types import ReactionTypeEmoji
from helpers import get_arguments, get_next_matchday
from common import add_player_if_not_existant, validate_access, reply_only_CEO_can_do_it, validate_CEO_zone
import database
import constants
import re

def execute(message, bot):
    try:
        player = add_player_if_not_existant(message.from_user.first_name,
                                            message.from_user.last_name,
                                            message.from_user.username,
                                            message.from_user.id)
        bot.reply_to(message, "🛑 Пока эта команда не работает. Не дури галавы.")
        '''if validate_access(message.chat.id, player, bot, message):
            command_and_argument_split = message.text.split('\n', 1)
            if len(command_and_argument_split)>1:
                parts = command_and_argument_split[1].split('\n')
                
                for line in parts:
                    lineup_player_params = re.split(r'[\s]+', line.strip())
                    first_name = lineup_player_params[0]
                    last_name = lineup_player_params[1]
                    lineup_player = database.find_player_by_name(first_name, last_name)
                    if lineup_player is not None:
                        player_id = lineup_player[7]
                        goals = lineup_player_params[2]
                        assists = lineup_player_params[3]
                        own_goals = lineup_player_params[4]
                        game_id = database.get_game_id()
                        #database.add_game_stats(player_id,game_id,goals,assists,own_goals)
                        #database.update_player_squad_for_matchday(squad_player_id, squad, get_next_matchday())
                    else:
                        log(f"Can't find player to register in a lineup: {lineup_player_params}")
                log(f"Game stats successfully registered")
                bot.reply_to(message, "Результат деления на команды внесен!")
                bot.set_message_reaction(message.chat.id,
                                    message.message_id,
                                    [ReactionTypeEmoji('✍️')],
                                    is_big=True)
            else:
                bot.reply_to(message, "Пришли результат дележки! Ты ж ничего не прислал. Знаешь в каком формате прислать? Сам разберись.")'''
    except Exception as e:
        bot.reply_to(message, constants.UNHANDLED_EXCEPTION_MESSAGE)
        log_error(e)

        
        '''
/register_game_stats
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