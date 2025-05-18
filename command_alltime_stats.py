from logger import log, log_error
from telebot.types import ReactionTypeEmoji
from helpers import get_arguments, get_next_matchday, get_next_matchday_formatted, get_today_minsk_time
from common import add_player_if_not_existant, validate_access_no_game_registration_needed, text_to_image, get_player_name_extended, reply_only_CEO_can_do_it, validate_CEO_zone
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
            table = pt.PrettyTable(['N','Игрок', 'Игры', 'Голы', 'Асисты', 'Автоголы', 'Гол/Игра', 'Побед', '% Побед'])
            table.align['N'] = 'c'
            table.align['Игрок'] = 'l'
            table.align['Игры'] = 'c'
            table.align['Голы'] = 'c'
            table.align['Асисты'] = 'c'
            table.align['Автоголы'] = 'c'
            table.align['Гол/Игра'] = 'c'
            table.align['Побед'] = 'c'
            table.align['% Побед'] = 'c'
            table.hrules = True
            stats = database.get_alltime_stats()
            i = 1
            
            for player in stats:
                first_name = player[0]
                last_name = player[1]
                games_played = player[2]
                goals = player[3]
                assists = player[4]
                own_goals = player[5]
                avg_goals = player[6]
                wins = player[7]
                win_rate = player[8]
                table.add_row([i, f"{first_name} {last_name}", games_played, goals, assists, own_goals, avg_goals, wins, f"{win_rate}%"])
                i+=1

            stats_goals_games = database.get_alltime_stats_games_goal()
            output = f"Всего игр сыграно: {stats_goals_games[0]}. Всего голов забито: {stats_goals_games[1]}. Всего автоголов забито: {stats_goals_games[2]}\n{table.get_string()}"
            photo = text_to_image(output,image_size=(800, 1150),font_size=12)
            bot.send_photo(message.chat.id, photo, reply_to_message_id=message.message_id)
    except Exception as e:
        bot.reply_to(message, constants.UNHANDLED_EXCEPTION_MESSAGE)
        log_error(e)
        