from logger import log, log_error
from telebot.types import ReactionTypeEmoji
from helpers import get_arguments, get_next_matchday
from common import add_player_if_not_existant, validate_access_no_game_registration_needed, reply_only_CEO_can_do_it, validate_CEO_zone
import database
import constants
import re

def execute(message, bot):
    try:
        player = add_player_if_not_existant(message.from_user.first_name,
                                            message.from_user.last_name,
                                            message.from_user.username,
                                            message.from_user.id)
        if validate_access_no_game_registration_needed(message.chat.id, player, bot, message):
            command_and_argument_split = message.text.split('\n', 1)
            if len(command_and_argument_split)>1:
                parts = command_and_argument_split[1].split('\n')
                
                for line in parts:
                    lineup_player_params = re.split(r'[\s]+', line.strip())
                    lineup_player = database.find_player_by_name(lineup_player_params[1], lineup_player_params[2])
                    if lineup_player is not None:
                        squad_emoji = lineup_player_params[0]
                        squad_player_id = lineup_player[7]
                        squad = None
                        if squad_emoji == constants.SQUAD_CORN_EMOJI:
                            squad = constants.SQUAD_CORN
                        else:
                            if squad_emoji == constants.SQUAD_TOMATO_EMOJI:
                                squad = constants.SQUAD_TOMATO
                        if squad is None:
                            log(f"Can't recognize squad: {squad_emoji} for the player {lineup_player_params}")
                        
                        database.update_player_squad_for_matchday(squad_player_id, squad, get_next_matchday())
                    else:
                        log(f"Can't find player to register in a lineup: {lineup_player_params}")
                log(f"Squad successfully registered")
                bot.reply_to(message, "Результат деления на команды внесен!")
                bot.set_message_reaction(message.chat.id,
                                    message.message_id,
                                    [ReactionTypeEmoji('✍️')],
                                    is_big=True)
            else:
                bot.reply_to(message, "Пришли результат дележки! Ты ж ничего не прислал.")

    except Exception as e:
        bot.reply_to(message, constants.UNHANDLED_EXCEPTION_MESSAGE)
        log_error(e)
