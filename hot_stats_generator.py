from sqlalchemy import case
import constants
import os
from helpers import format_date
import deepseek
from logger import log, log_error
import database
import io
from common import fill_records_template
import random
import command_records

class HotStatsGenerator:
    def __init__(self):
        pass

    def get_message(self):
        random_number = random.randint(0, 23)
        match random_number:
            case 0:
                return self.how_many_games_we_played(random_number)
            case 1:
                return self.how_many_games_were_cancelled(random_number)
            case 2:
                return self.win_streaks(random_number)
            case 3:
                return self.losing_streaks(random_number)
            case 4:
                return self.active_win_streaks(random_number)
            case 5:
                return self.active_loss_streaks(random_number)
            case 6:
                return self.top_goals_per_game(random_number)
            case 7:
                return self.top_goals_alltime(random_number)
            case 8:
                return self.top_assists_per_game(random_number)
            case 9:
                return self.top_assists_alltime(random_number)
            case 10:
                return self.top_own_goals_per_game(random_number)
            case 11:
                return self.who_scored_most_own_goals(random_number)
            case 12:
                return self.who_has_the_higher_win_rate(random_number)
            case 13:
                return self.who_paid_the_most_money(random_number)
            case 14:
                return self.who_played_the_most_games_for_corn(random_number)
            case 15:
                return self.who_played_the_most_games_for_tomato(random_number)
            case 16:
                return self.who_sat_on_a_chair_the_most_times(random_number)
            case 17:
                return self.top_player_pairs(random_number)
            case 18: 
                return self.average_age_and_height(random_number)
            case 19: 
                return self.attendance_streaks(random_number)
            case 20: 
                return self.games_with_max_goal_difference(random_number)
            case 21: 
                return self.most_goals_scored_per_game_by_corn(random_number)
            case 22: 
                return self.most_goals_scored_per_game_by_tomato(random_number)
            case 23: 
                return self.individual_stats_random_player()
            case _:
                return "Нет сегодня никакой статистики"

    def get_records_template(self, random_number):
        records_template = ""
        with open(constants.RECORDS_TEMPLATE_FILE, "r") as file:
            records_template = file.read()
        parts = records_template.split('[!]')
        if random_number < len(parts):
            var = parts[random_number]
            return var
        return "Нет сегодня никакой статистики"

    def how_many_games_we_played(self, random_number):
        records_template = self.get_records_template(random_number)
        sql_how_many_games_we_played = ""
        with open(f"SQL Queries/{constants.SQL_HOW_MANY_GAMES_WE_PLAYED}" , "r") as file:
            sql_how_many_games_we_played = file.read()
        text_how_many_games_we_played = database.execute_sql_query_return_one(sql_how_many_games_we_played)
        records_template = fill_records_template(records_template, constants.SQL_HOW_MANY_GAMES_WE_PLAYED, text_how_many_games_we_played)
        return records_template
    
    def how_many_games_were_cancelled(self, random_number):
        records_template = self.get_records_template(random_number)
        sql_how_many_games_were_cancelled = ""
        with open(f"SQL Queries/{constants.SQL_HOW_MANY_GAMES_WERE_CANCELLED}" , "r") as file:
            sql_how_many_games_were_cancelled = file.read()
        text_how_many_games_were_cancelled = database.execute_sql_query_return_one(sql_how_many_games_were_cancelled)
        records_template = fill_records_template(records_template, constants.SQL_HOW_MANY_GAMES_WERE_CANCELLED, text_how_many_games_were_cancelled)
        return records_template

    def win_streaks(self, random_number):
        records_template = self.get_records_template(random_number)
        sql_win_streaks = ""
        with open(f"SQL Queries/{constants.SQL_WIN_STREAKS}" , "r") as file:
            sql_win_streaks = file.read()
        win_streaks_from_db = database.execute_sql_query_return_many(sql_win_streaks)
        text_win_streaks = command_records.format_win_loose_streaks(win_streaks_from_db)
        records_template = fill_records_template(records_template, constants.SQL_WIN_STREAKS, text_win_streaks)
        return records_template

    def losing_streaks(self, random_number):
        records_template = self.get_records_template(random_number)
        sql_losing_streaks = ""
        with open(f"SQL Queries/{constants.SQL_LOSING_STREAKS}" , "r") as file:
            sql_losing_streaks = file.read()
        losing_streaks_from_db = database.execute_sql_query_return_many(sql_losing_streaks)
        text_losing_streaks = command_records.format_win_loose_streaks(losing_streaks_from_db)
        records_template = fill_records_template(records_template, constants.SQL_LOSING_STREAKS, text_losing_streaks)
        return records_template

    def active_win_streaks(self, random_number):
        records_template = self.get_records_template(random_number)
        sql_active_win_streaks = ""
        with open(f"SQL Queries/{constants.SQL_ACTIVE_WIN_STREAKS}" , "r") as file:
            sql_active_win_streaks = file.read()
        active_win_streaks_from_db = database.execute_sql_query_return_many(sql_active_win_streaks)
        text_active_win_streaks = command_records.format_win_loose_streaks(active_win_streaks_from_db)
        records_template = fill_records_template(records_template, constants.SQL_ACTIVE_WIN_STREAKS, text_active_win_streaks)
        return records_template

    def active_loss_streaks(self, random_number):
        records_template = self.get_records_template(random_number)
        sql_active_loss_streaks = ""
        with open(f"SQL Queries/{constants.SQL_ACTIVE_LOSS_STREAKS}" , "r") as file:
            sql_active_loss_streaks = file.read()
        active_loss_streaks_from_db = database.execute_sql_query_return_many(sql_active_loss_streaks)
        text_active_loss_streaks = command_records.format_win_loose_streaks(active_loss_streaks_from_db)
        records_template = fill_records_template(records_template, constants.SQL_ACTIVE_LOSS_STREAKS, text_active_loss_streaks)
        return records_template

    def top_goals_per_game(self, random_number):
        records_template = self.get_records_template(random_number)
        sql_top_goals_per_game = ""
        with open(f"SQL Queries/{constants.SQL_TOP_GOALS_PER_GAME}" , "r") as file:
            sql_top_goals_per_game = file.read()
        top_goals_per_game_from_db = database.execute_sql_query_return_many(sql_top_goals_per_game)
        text_top_goals_per_game = command_records.format_top_goals(top_goals_per_game_from_db)
        records_template = fill_records_template(records_template, constants.SQL_TOP_GOALS_PER_GAME, text_top_goals_per_game)
        return records_template

    def top_goals_alltime(self, random_number):
        records_template = self.get_records_template(random_number)
        sql_top_goals_alltime = ""
        with open(f"SQL Queries/{constants.SQL_TOP_GOALS_ALLTIME}" , "r") as file:
            sql_top_goals_alltime = file.read()
        top_goals_alltime_from_db = database.execute_sql_query_return_many(sql_top_goals_alltime)
        text_top_goals_alltime = command_records.format_most_goals(top_goals_alltime_from_db)
        records_template = fill_records_template(records_template, constants.SQL_TOP_GOALS_ALLTIME, text_top_goals_alltime)
        return records_template

    def top_assists_per_game(self, random_number):
        records_template = self.get_records_template(random_number)
        sql_top_assists_per_game = ""
        with open(f"SQL Queries/{constants.SQL_TOP_ASSISTS_PER_GAME}" , "r") as file:
            sql_top_assists_per_game = file.read()
        top_assists_per_game_from_db = database.execute_sql_query_return_many(sql_top_assists_per_game)
        text_top_assists_per_game = command_records.format_top_goals(top_assists_per_game_from_db)
        records_template = fill_records_template(records_template, constants.SQL_TOP_ASSISTS_PER_GAME, text_top_assists_per_game)
        return records_template

    def top_assists_alltime(self, random_number):
        records_template = self.get_records_template(random_number)
        sql_top_assists_alltime = ""
        with open(f"SQL Queries/{constants.SQL_TOP_ASSISTS_ALLTIME}" , "r") as file:
            sql_top_assists_alltime = file.read()
        top_assists_alltime_from_db = database.execute_sql_query_return_many(sql_top_assists_alltime)
        text_top_assists_alltime = command_records.format_most_goals(top_assists_alltime_from_db)
        records_template = fill_records_template(records_template, constants.SQL_TOP_ASSISTS_ALLTIME, text_top_assists_alltime)
        return records_template

    def top_own_goals_per_game(self, random_number):
        records_template = self.get_records_template(random_number)
        sql_top_own_goals_per_game = ""
        with open(f"SQL Queries/{constants.SQL_TOP_OWN_GOALS_PER_GAME}" , "r") as file:
            sql_top_own_goals_per_game = file.read()
        top_own_goals_per_game_from_db = database.execute_sql_query_return_many(sql_top_own_goals_per_game)
        text_top_own_goals_per_game = command_records.format_top_goals(top_own_goals_per_game_from_db)
        records_template = fill_records_template(records_template, constants.SQL_TOP_OWN_GOALS_PER_GAME, text_top_own_goals_per_game)
        return records_template

    def who_scored_most_own_goals(self, random_number):
        records_template = self.get_records_template(random_number)
        sql_who_scored_most_own_goals = ""
        with open(f"SQL Queries/{constants.SQL_WHO_SCORED_MOST_OWN_GOALS}" , "r") as file:
            sql_who_scored_most_own_goals = file.read()
        who_scored_most_own_goals_from_db = database.execute_sql_query_return_many(sql_who_scored_most_own_goals)
        text_who_scored_most_own_goals = command_records.format_most_goals(who_scored_most_own_goals_from_db)
        records_template = fill_records_template(records_template, constants.SQL_WHO_SCORED_MOST_OWN_GOALS, text_who_scored_most_own_goals)
        return records_template

    def who_has_the_higher_win_rate(self, random_number):
        records_template = self.get_records_template(random_number)
        sql_who_has_the_higher_win_rate = ""
        with open(f"SQL Queries/{constants.SQL_WHO_HAS_THE_HIGHER_WIN_RATE}" , "r") as file:
            sql_who_has_the_higher_win_rate = file.read()
        who_has_the_higher_win_rate_from_db = database.execute_sql_query_return_many(sql_who_has_the_higher_win_rate)
        text_who_has_the_higher_win_rate = command_records.format_win_rate(who_has_the_higher_win_rate_from_db)
        records_template = fill_records_template(records_template, constants.SQL_WHO_HAS_THE_HIGHER_WIN_RATE, text_who_has_the_higher_win_rate)
        return records_template

    def who_paid_the_most_money(self, random_number):
        records_template = self.get_records_template(random_number)
        sql_who_paid_the_most_money = ""
        with open(f"SQL Queries/{constants.SQL_WHO_PAID_THE_MOST_MONEY}" , "r") as file:
            sql_who_paid_the_most_money = file.read()
        who_paid_the_most_money_from_db = database.execute_sql_query_return_many(sql_who_paid_the_most_money)
        text_who_paid_the_most_money = command_records.format_who_paid_most_money(who_paid_the_most_money_from_db)
        records_template = fill_records_template(records_template, constants.SQL_WHO_PAID_THE_MOST_MONEY, text_who_paid_the_most_money)
        return records_template

    def who_played_the_most_games_for_corn(self, random_number):
        records_template = self.get_records_template(random_number)
        sql_who_played_the_most_games_for_corn = ""
        with open(f"SQL Queries/{constants.SQL_WHO_PLAYED_THE_MOST_GAMES_FOR_CORN}" , "r") as file:
            sql_who_played_the_most_games_for_corn = file.read()
        who_played_the_most_games_for_corn_from_db = database.execute_sql_query_return_many(sql_who_played_the_most_games_for_corn)
        text_who_played_the_most_games_for_corn = command_records.format_who_player_most_games_corn(who_played_the_most_games_for_corn_from_db)
        records_template = fill_records_template(records_template, constants.SQL_WHO_PLAYED_THE_MOST_GAMES_FOR_CORN, text_who_played_the_most_games_for_corn)
        return records_template

    def who_played_the_most_games_for_tomato(self, random_number):
        records_template = self.get_records_template(random_number)
        sql_who_played_the_most_games_for_tomato = ""
        with open(f"SQL Queries/{constants.SQL_WHO_PLAYED_THE_MOST_GAMES_FOR_TOMATO}" , "r") as file:
            sql_who_played_the_most_games_for_tomato = file.read()
        who_played_the_most_games_for_tomato_from_db = database.execute_sql_query_return_many(sql_who_played_the_most_games_for_tomato)
        text_who_played_the_most_games_for_tomato = command_records.format_who_player_most_games_tomato(who_played_the_most_games_for_tomato_from_db)
        records_template = fill_records_template(records_template, constants.SQL_WHO_PLAYED_THE_MOST_GAMES_FOR_TOMATO, text_who_played_the_most_games_for_tomato)
        return records_template

    def who_sat_on_a_chair_the_most_times(self, random_number):
        records_template = self.get_records_template(random_number)
        sql_who_sat_on_a_chair_the_most_times = ""
        with open(f"SQL Queries/{constants.SQL_WHO_SAT_ON_A_CHAIR_THE_MOST_TIMES}" , "r") as file:
            sql_who_sat_on_a_chair_the_most_times = file.read()
        who_sat_on_a_chair_the_most_times_from_db = database.execute_sql_query_return_many(sql_who_sat_on_a_chair_the_most_times)
        text_who_sat_on_a_chair_the_most_times = command_records.format_most_chair(who_sat_on_a_chair_the_most_times_from_db)
        records_template = fill_records_template(records_template, constants.SQL_WHO_SAT_ON_A_CHAIR_THE_MOST_TIMES, text_who_sat_on_a_chair_the_most_times)
        return records_template

    def top_player_pairs(self, random_number):
        records_template = self.get_records_template(random_number)
        sql_top_player_pairs = ""
        with open(f"SQL Queries/{constants.SQL_TOP_PLAYER_PAIRS}" , "r") as file:
            sql_top_player_pairs = file.read()
        top_player_pairs_from_db = database.execute_sql_query_return_many(sql_top_player_pairs)
        text_top_player_pairs = command_records.format_player_pairs(top_player_pairs_from_db)
        records_template = fill_records_template(records_template, constants.SQL_TOP_PLAYER_PAIRS, text_top_player_pairs)
        return records_template
    
    def average_age_and_height(self, random_number):
        records_template = self.get_records_template(random_number)
        sql_average_age_and_height = ""
        with open(f"SQL Queries/{constants.SQL_AVERAGE_AGE_AND_HEIGHT}" , "r") as file:
            sql_average_age_and_height = file.read()
        average_age_and_height_from_db = database.execute_sql_query_return_many(sql_average_age_and_height)
        if len(average_age_and_height_from_db) > 0:
            text_average_age_and_height = command_records.format_average_age_and_height(average_age_and_height_from_db[0])
        else:
            text_average_age_and_height = "Нет данных сегодня. Что-то ляснулось."
        records_template = fill_records_template(records_template, constants.SQL_AVERAGE_AGE_AND_HEIGHT, text_average_age_and_height)
        return records_template

    def attendance_streaks(self, random_number):
        records_template = self.get_records_template(random_number)
        sql_attendance_streaks = ""
        with open(f"SQL Queries/{constants.SQL_ATTENDANCE_STREAKS}" , "r") as file:
            sql_attendance_streaks = file.read()
        attendance_streaks_from_db = database.execute_sql_query_return_many(sql_attendance_streaks)
        text_attendance_streaks = command_records.format_attendance_streaks(attendance_streaks_from_db)
        records_template = fill_records_template(records_template, constants.SQL_ATTENDANCE_STREAKS, text_attendance_streaks)
        return records_template

    def games_with_max_goal_difference(self, random_number):
        records_template = self.get_records_template(random_number)
        sql_max_goal_difference = ""
        with open(f"SQL Queries/{constants.SQL_MAX_GOAL_DIFFERENCE}" , "r") as file:
            sql_max_goal_difference = file.read()
        max_goal_difference_from_db = database.execute_sql_query_return_many(sql_max_goal_difference)
        text_max_goal_difference = command_records.format_max_goal_difference(max_goal_difference_from_db)
        records_template = fill_records_template(records_template, constants.SQL_MAX_GOAL_DIFFERENCE, text_max_goal_difference)
        return records_template

    def most_goals_scored_per_game_by_corn(self, random_number):
        records_template = self.get_records_template(random_number)
        sql_most_goals_scored_per_game_by_corn = ""
        with open(f"SQL Queries/{constants.SQL_MOST_GOALS_SCORED_PER_GAME_BY_CORN}" , "r") as file:
            sql_most_goals_scored_per_game_by_corn = file.read()
        most_goals_scored_per_game_by_corn_from_db = database.execute_sql_query_return_many(sql_most_goals_scored_per_game_by_corn)
        text_most_goals_scored_per_game_by_corn = command_records.format_most_goals_scored_per_game_by_team(most_goals_scored_per_game_by_corn_from_db)
        records_template = fill_records_template(records_template, constants.SQL_MOST_GOALS_SCORED_PER_GAME_BY_CORN, text_most_goals_scored_per_game_by_corn)
        return records_template
    
    def most_goals_scored_per_game_by_tomato(self, random_number):
        records_template = self.get_records_template(random_number)
        sql_most_goals_scored_per_game_by_tomato = ""
        with open(f"SQL Queries/{constants.SQL_MOST_GOALS_SCORED_PER_GAME_BY_TOMATO}" , "r") as file:
            sql_most_goals_scored_per_game_by_tomato = file.read()
        most_goals_scored_per_game_by_tomato_from_db = database.execute_sql_query_return_many(sql_most_goals_scored_per_game_by_tomato)
        text_most_goals_scored_per_game_by_tomato = command_records.format_most_goals_scored_per_game_by_team(most_goals_scored_per_game_by_tomato_from_db)
        records_template = fill_records_template(records_template, constants.SQL_MOST_GOALS_SCORED_PER_GAME_BY_TOMATO, text_most_goals_scored_per_game_by_tomato)
        return records_template

    def individual_stats_random_player(self):    
        random_player = database.get_random_player()
        player_id = random_player[0]
        friendly_first_name = random_player[1]
        friendly_last_name = random_player[2]
        log(f"Hot stats player: {player_id}, {friendly_first_name} {friendly_last_name}")
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