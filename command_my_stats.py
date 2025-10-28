from logger import log, log_error
from telebot.types import ReactionTypeEmoji
from helpers import get_next_matchday, get_next_matchday_formatted, get_today_minsk_time
from common import add_player_if_not_existant_with_params, validate_access_no_game_registration_needed, text_to_image, get_player_name_formal, reply_only_CEO_can_do_it, validate_CEO_zone
import database
import constants
import prettytable as pt

def execute(message, bot):
    try:
        current_player = add_player_if_not_existant_with_params(message.text,
                                                                message.from_user.first_name,
                                                                message.from_user.last_name,
                                                                message.from_user.username,
                                                                message.from_user.id)
       
        if validate_access_no_game_registration_needed(message.chat.id, current_player, bot, message):
            season_stats_photo = season_stats(current_player)
            bot.send_photo(message.chat.id, season_stats_photo, reply_to_message_id=message.message_id)
            
            alltime_personal_stats_photo = alltime_personal_stats(current_player)
            bot.send_photo(message.chat.id, alltime_personal_stats_photo, reply_to_message_id=message.message_id)
            
            last_games_photo = last_games(current_player)
            bot.send_photo(message.chat.id, last_games_photo, reply_to_message_id=message.message_id)
            
            log(f"/my_stats requested by: {get_player_name_formal(current_player)}")
    except Exception as e:
        bot.reply_to(message, constants.UNHANDLED_EXCEPTION_MESSAGE)
        log_error(e)

def season_stats(current_player):
    table = pt.PrettyTable(['Сезон', 'Игры', 'Голы', 'Асисты', 'Автоголы'])
    table.align['Сезон'] = 'c'
    table.align['Игры'] = 'c'
    table.align['Голы'] = 'c'
    table.align['Асисты'] = 'c'
    table.align['Автоголы'] = 'c'
    table.hrules = True
    individual_stats = database.get_individual_stats_by_season(current_player[7])

    for season_stats in individual_stats:
        season = season_stats[0] if season_stats[0] is not None else "-"
        games_played = season_stats[1] if season_stats[1] is not None else "-"
        goals = season_stats[2] if season_stats[2] is not None else "-"
        assists = season_stats[3] if season_stats[3] is not None else "-"
        own_goals = season_stats[4] if season_stats[4] is not None else "-"

        table.add_row([season, games_played, goals, assists, own_goals])
    output = f"{get_player_name_formal(current_player)}\n{table.get_string()}"
    photo = text_to_image(output,image_size=(550, 400))
    return photo

def last_games(current_player):
    table = pt.PrettyTable(['Дата', 'К', ':', 'П', 'Команда', 'Результат', 'Голы', 'Асисты', 'Автоголы'])
    table.align['Дата'] = 'c'
    table.align['К'] = 'c'
    table.align[':'] = 'c'
    table.align['П'] = 'c'
    table.align['Команда'] = 'c'
    table.align['Результат'] = 'c'
    table.align['Голы'] = 'c'
    table.align['Асисты'] = 'c'
    table.align['Автоголы'] = 'c'
    table.hrules = True
    individual_stats = database.get_last_individual_games(current_player[7])

    for stat in individual_stats:
        date = stat[0]
        score_corn = stat[1]
        score_tomato = stat[2]
        goals = stat[3]
        assists = stat[4]
        own_goals = stat[5]
        squad = stat[6]
        result = ""
        squad_short = ""
        if squad is None: #for cases with legacy stats when we didn't document split into 2 teams.
            result = "-"
            squad = "-"
            squad_short = "-"
            score_corn = "-"
            score_tomato = "-"
            goals = "-"
            assists = "-"
            own_goals = "-"
        else:
            if score_corn > score_tomato and squad == constants.SQUAD_CORN:
                result = "Победа"
            if score_corn < score_tomato and squad == constants.SQUAD_CORN:
                result = "Поражение"
            if score_corn > score_tomato and squad == constants.SQUAD_TOMATO:
                result = "Поражение"
            if score_corn < score_tomato and squad == constants.SQUAD_TOMATO:
                result = "Победа"
            if score_corn == score_tomato:
                result = "Ничья"
            squad_short = "К" if squad == constants.SQUAD_CORN else "П"
        table.add_row([date, score_corn, ":", score_tomato, squad_short, result, goals, assists, own_goals])
    
    output = f"{get_player_name_formal(current_player)}\n{table.get_string()}"
    photo = text_to_image(output,image_size=(600, 900),font_size=12)
    return photo

def alltime_personal_stats(current_player):
    player_id = current_player[7]

    win_rate = database.get_win_rate(player_id)

    individual_stats = database.get_individual_stats(player_id)

    output = f'''{get_player_name_formal(current_player)}\n
    Максимальная серия побед подряд: {'<еще не работает>'}\n
    Максимальная серия без поражений подряд: {'<еще не работает>'}\n
    Максимальная серия поражений подряд: {'<еще не работает>'}\n
    Текущая серия побед подряд: {'<еще не работает>'}\n
    Текущая серия без поражений подряд: {'<еще не работает>'}\n
    Текущая серия поражений подряд: {'<еще не работает>'}\n
    Максимальное количество голов в одном матче: {'<еще не работает>'}\n
    Максимальное количество ассистов в одном матче: {'<еще не работает>'}\n
    Максимальное количество автоголов в одном матче: {'<еще не работает>'}\n
    Всего голов: {individual_stats[1] if individual_stats[1] is not None else "-"}\n 
    Всего ассистов: {individual_stats[2] if individual_stats[2] is not None else "-"}\n
    Всего автоголов: {individual_stats[3] if individual_stats[3] is not None else "-"}\n
    Игр сыграно за Кукурузу: {individual_stats[4] if individual_stats[4] is not None else "-"}\n
    Игр сыграно за Помидор: {individual_stats[5] if individual_stats[5] is not None else "-"}\n
    Всего побед: {win_rate[4] if win_rate[4] is not None else "-"}\n
    Процент побед: {win_rate[5] if win_rate[5] is not None else "-"}%\n
    Всего игр сыграно: {win_rate[3] if win_rate[3] is not None else "-"}\n
    '''

    photo = text_to_image(output,image_size=(550, 600),font_size=12)
    return photo