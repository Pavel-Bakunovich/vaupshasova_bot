from logger import log, log_error
from telebot.types import ReactionTypeEmoji
from helpers import get_arguments, get_next_matchday, get_next_matchday_formatted, get_today_minsk_time
from common import add_player_if_not_existant, validate_access, text_to_image, get_player_name_extended, reply_only_CEO_can_do_it, validate_CEO_zone
import database
import constants
import prettytable as pt

def execute(message, bot):
    try:
        player = add_player_if_not_existant(message.from_user.first_name,
                                            message.from_user.last_name,
                                            message.from_user.username,
                                            message.from_user.id)
        '''if validate_access(message.chat.id, player, bot, message):
            table = pt.PrettyTable(['N','Игрок', 'Игры', 'Голы', 'Асисты', 'Автоголы'])
            table.align['N'] = 'c'
            table.align['Игрок'] = 'l'
            table.align['Игры'] = 'c'
            table.align['Голы'] = 'c'
            table.align['Асисты'] = 'c'
            table.align['Автоголы'] = 'c'
            table.hrules = True
            season_stats = database.get_season_stats(get_today_minsk_time().year)
            i = 1
            
            for player in season_stats:
                first_name = player[0]
                last_name = player[1]
                games_played = player[2]
                goals = player[3]
                assists = player[4]
                own_goals = player[5]
                table.add_row([i, f"{first_name} {last_name}", games_played, goals, assists, own_goals])
                i+=1
            photo = text_to_image(table.get_string(),image_size=(600, 1000))
            bot.send_photo(message.chat.id, photo, reply_to_message_id=message.message_id)'''
    except Exception as e:
        bot.reply_to(message, constants.UNHANDLED_EXCEPTION_MESSAGE)
        log_error(e)
        