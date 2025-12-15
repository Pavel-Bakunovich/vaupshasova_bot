import constants
import os
from helpers import format_date
import deepseek
from logger import log, log_error
import database
import io

class HotStatsGenerator:
    def __init__(self):
        pass

    def get_message(self):    
        random_player = database.get_random_player()
        player_id = random_player[0]
        friendly_first_name = random_player[1]
        friendly_last_name = random_player[2]
        informal_friendly_first_name = random_player[3]
        height = random_player[4]
        birthday = random_player[5]
        games_played = random_player[6]

        individual_stats = database.get_individual_stats(player_id)
        individual_balance = database.get_individual_balance(player_id)
        goals_sum = individual_stats[1]
        assists_sum = individual_stats[2]
        own_goals_sum = individual_stats[3]
        games_played_for_corn = individual_stats[4]
        games_played_for_tomato = individual_stats[5]

        win_rate = database.get_win_rate(player_id)
        total_wins = win_rate[4]
        win_rate_percentage = win_rate[5]

        max_goals_per_game = database.get_max_goals_per_game_by_player(player_id)
        max_assists_per_game = database.get_max_assists_per_game_by_player(player_id)
        max_own_goals_per_game = database.get_max_own_goals_per_game_by_player(player_id)

        get_individual_balance = database.get_individual_balance(player_id)
        individual_balance = get_individual_balance[0]
        total_money_given = get_individual_balance[1]

        stats = f'''Рубрика "Статистика дня".
        
Игрок дня: {friendly_first_name} {friendly_last_name}
Сыграно игр: {games_played}
Сыграно игр за Кукурузу: {games_played_for_corn}
Сыграно игр за Помидор: {games_played_for_tomato}
Всего побед: {total_wins}
Процент побед: {win_rate_percentage}%
Всего голов: {goals_sum}
Всего ассистов: {assists_sum}
Всего автоголов: {own_goals_sum}
Максимальное количество голов в одном матче: {max_goals_per_game[0][4] if max_goals_per_game[0][4] is not None else "-"} ({format_date(max_goals_per_game[0][3] if max_goals_per_game[0][3] is not None else "-")})
Максимальное количество ассистов в одном матче: {max_assists_per_game[0][4] if max_assists_per_game[0][4] is not None else "-"} ({format_date(max_assists_per_game[0][3] if max_assists_per_game[0][3] is not None else "-")})
Максимальное количество автоголов в одном матче: {max_own_goals_per_game[0][4] if max_own_goals_per_game[0][4] is not None else "-"} ({format_date(max_own_goals_per_game[0][3] if max_own_goals_per_game[0][3] is not None else "-")})
Общий баланс на сегодняшний день: {individual_balance} р.
Всего сдал денег за все время: {total_money_given} р.'''
        #response = deepseek.send_request(f"Вот индивидуальная статистика игрока. Перескажи всю эту статистику с приколами. Упомяни имя игрока и передай в точности все цифры. Не используй разметку. \n{stats}", 0)

        return stats

    