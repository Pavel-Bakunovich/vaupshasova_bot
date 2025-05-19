from logger import log, log_error
from telebot.types import ReactionTypeEmoji
from helpers import get_arguments, get_next_matchday, get_next_matchday_formatted
from common import add_player_if_not_existant, get_player_name_formal, get_player_name_extended, text_to_image, validate_access_no_game_registration_needed, reply_only_CEO_can_do_it, validate_CEO_zone
import database
import constants
import re
import prettytable as pt

def get_player_balance(player_id, players_balances):
    for player in players_balances:
        if player[0] == player_id:
            return player[3]
    return None

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
            table = pt.PrettyTable(['N', 'Игрок', 'Сдал', 'Баланс', 'Команда', 'Голы', 'Асисты', 'Автоголы'])
            table.align['N'] = 'c'
            table.align['Игрок'] = 'l'
            table.align['Сдал'] = 'c'
            table.align['Баланс'] = 'c'
            table.align['Команда'] = 'c'
            table.align['Голы'] = 'c'
            table.align['Асисты'] = 'c'
            table.align['Автоголы'] = 'c'
            table.hrules = True
            matchday_roster = database.get_squad(get_next_matchday())
            i = 1
            players_balances = database.get_players_balance()
            for player in matchday_roster:
                matchday_player_registration_type = player[1]
                player_id = player[0]
                if matchday_player_registration_type == constants.TYPE_ADD:
                    squad = player[10]
                    if squad is not None:
                        squad = squad.replace(constants.SQUAD_CORN, "К")
                        squad = squad.replace(constants.SQUAD_TOMATO, "П")
                    else:
                        squad = "-"
                    balance = get_player_balance(player_id, players_balances)
                    table.add_row([i, get_player_name_extended(player), "", f"{balance} р.",squad, "", "", ""])
                    i+=1
            table._min_width = {"Голы" : 15, "Асисты" : 15, "Автоголы": 5}
            table._max_width = {"Голы" : 15, "Асисты" : 15, "Автоголы": 5}
            
            score = pt.PrettyTable([' ', 'К ', ':', 'П'])
            score.align[' '] = 'c'
            score.align['K'] = 'c'
            score.align[':'] = 'c'
            score.align['П'] = 'c'
            score.add_row(["Счет", " ", ":", " "])
            score._min_width = {"K" : 5, "П" : 5}
            score._max_width = {"K" : 5, "П" : 5}

            result = f"{get_next_matchday_formatted()}\n{score.get_string()}\n{table.get_string()}" 
            photo = text_to_image(result, image_size=(950, 650))
            bot.send_photo(message.chat.id, photo, reply_to_message_id=message.message_id)
            log(f"Successfullty printed lineups. Requested by: {get_player_name_formal(current_player)}")
            
    except Exception as e:
        bot.reply_to(message, constants.UNHANDLED_EXCEPTION_MESSAGE)
        log_error(e)

