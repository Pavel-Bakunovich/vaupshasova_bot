from flask import Flask, render_template, request, jsonify, send_from_directory
import os
from datetime import datetime, timedelta
import database
import helpers
import constants

app = Flask(__name__, template_folder='mini-app/templates', static_folder='mini-app/static')

# Define the new relative or absolute paths for your folders
custom_template_dir = 'web/templates'
custom_static_dir = 'web/static'

# Mock data for demo purposes
MOCK_PLAYERS = {
    343151297: {
        'id': 1,
        'telegram_id': 343151297,
        'first_name': 'Иван',
        'last_name': 'Шмарловский',
        'username': 'ivan_petrov',
        'friendly_first_name': 'Иван',
        'friendly_last_name': 'Шмарловский',
        'informal_first_name': 'Ваня',
    },
    987654321: {
        'id': 2,
        'telegram_id': 987654321,
        'first_name': 'Мария',
        'last_name': 'Сидорова',
        'username': 'maria_sidorova',
        'friendly_first_name': 'Мария',
        'friendly_last_name': 'Сидорова',
        'informal_first_name': 'Маша',
    }
}

MOCK_SQUAD = [
    {
        'id': 1,
        'telegram_id': 343151297,
        'first_name': 'Иван',
        'last_name': 'Шмарловский',
        'username': 'ivan_petrov',
        'friendly_first_name': 'Иван',
        'friendly_last_name': 'Шмарловский',
        'informal_first_name': 'Ваня',
        'squad': '🌽',
        'registration_type': 'add',
        'wokeup': True
    },
    {
        'id': 2,
        'telegram_id': 987654321,
        'first_name': 'Мария',
        'last_name': 'Сидорова',
        'username': 'maria_sidorova',
        'friendly_first_name': 'Мария',
        'friendly_last_name': 'Сидорова',
        'informal_first_name': 'Маша',
        'squad': '🍅',
        'registration_type': 'add',
        'wokeup': True
    },
    {
        'id': 3,
        'telegram_id': 111111111,
        'first_name': 'Даниил',
        'last_name': 'Ivanov',
        'username': 'dan_iv',
        'friendly_first_name': 'Даниил',
        'friendly_last_name': 'Иванов',
        'informal_first_name': 'Даня',
        'squad': '🌽',
        'registration_type': 'add',
        'wokeup': True
    }
]

MOCK_STATS = {
    1: {
        'games_played': 24,
        'goals': 7,
        'assists': 12,
        'own_goals': 1,
        'games_for_corn': 15,
        'games_for_tomato': 9,
    },
    2: {
        'games_played': 18,
        'goals': 5,
        'assists': 8,
        'own_goals': 0,
        'games_for_corn': 9,
        'games_for_tomato': 9,
    }
}

MOCK_SEASON_STATS = {
    1: [
        {'season': 2024, 'games_played': 12, 'goals': 4, 'assists': 6, 'own_goals': 0},
        {'season': 2023, 'games_played': 12, 'goals': 3, 'assists': 6, 'own_goals': 1},
    ],
    2: [
        {'season': 2024, 'games_played': 10, 'goals': 3, 'assists': 5, 'own_goals': 0},
        {'season': 2023, 'games_played': 8, 'goals': 2, 'assists': 3, 'own_goals': 0},
    ]
}

MOCK_STREAKS = {
    1: {'win_streak': 3, 'loss_streak': 1},
    2: {'win_streak': 1, 'loss_streak': 2}
}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/player/<int:telegram_id>')
def get_player(telegram_id):
    player = database.find_player(telegram_id)
    player_id = player[7] if player else None

    individual_stats = database.get_individual_stats(player_id)
    season_stats_all = database.get_individual_stats_by_season(player_id)
    current_year = datetime.now().year

    season_stats = None
    for stat in season_stats_all:
        if stat[0] == current_year:
            season_stats = stat
            break

    if season_stats:
        season_stats_dict = {
            'games_played': season_stats[1] if season_stats[1] is not None else 0,
            'goals': season_stats[2] if season_stats[2] is not None else 0,
            'assists': season_stats[3] if season_stats[3] is not None else 0,
            'own_goals': season_stats[4] if season_stats[4] is not None else 0,
        }
    else:
        season_stats_dict = {
            'games_played': 0,
            'goals': 0,
            'assists': 0,
            'own_goals': 0,
        }

    individual_balance = database.get_individual_balance(player_id)
    attendance_streak = database.get_active_attendance_streak(player_id) if player_id is not None else None
    
    stats =  {
        'games_played': individual_stats[0] if individual_stats[1] is not None else 0,
        'goals': individual_stats[1] if individual_stats[1] is not None else 0,
        'assists': individual_stats[2] if individual_stats[2] is not None else 0,
        'own_goals': individual_stats[3] if individual_stats[3] is not None else 0,
        'games_for_corn': individual_stats[4] if individual_stats[4] is not None else 0,
        'games_for_tomato': individual_stats[5] if individual_stats[5] is not None else 0,
    }
    
    return jsonify({
        'success': True,
        'player':
            {
                'id': player[7] if player else None,
                'telegram_id': player [3] if player else None,
                'first_name': player[0] if player else None,
                'last_name': player[1] if player else None,
                'username': player[2] if player else None,
                'friendly_first_name': player[4] if player else None,
                'friendly_last_name': player[5] if player else None,
                'informal_first_name': player[6] if player else None
            },
        'stats': stats,
        'season_stats': season_stats_dict,
        'current_year': current_year,
        'balance': individual_balance[0] if individual_balance else 0,
        'attendance_streak': {
            'played': attendance_streak[0],
            'count': attendance_streak[1]
        } if attendance_streak else None
    })

@app.route('/api/next-matchday-squad/<int:telegram_id>')
def get_next_matchday_squad(telegram_id):
    """Get list of players registered for next matchday with proper staging"""
    try:
        # Get squad data from database
        next_matchday_date = helpers.get_next_matchday()
        squad_data = database.get_squad(next_matchday_date)
        
        # Format squad data
        formatted_squad = {
            'add': [],
            'chair': [],
            'maybe': [],
            'remove': []
        }
        
        current_player_id = telegram_id
        
        for player in squad_data:
            registration_type = player[1]  # Matchday.Type
            squad = player[10]  # Matchday.Squad
            
            player_info = {
                'id': player[0],
                'telegram_id': player[6],
                'first_name': player[3],
                'last_name': player[4],
                'username': player[5],
                'friendly_first_name': player[7],
                'friendly_last_name': player[8],
                'informal_first_name': player[9],
                'squad': squad,
                'registration_type': registration_type,
                'is_current_user': player[6] == current_player_id,  # Check if this is current user
                'time_stamp': player[11]
            }
            
            # Convert squad to emoji
            if squad == constants.SQUAD_CORN:
                player_info['squad_emoji'] = constants.SQUAD_CORN_EMOJI
            elif squad == constants.SQUAD_TOMATO:
                player_info['squad_emoji'] = constants.SQUAD_TOMATO_EMOJI
            else:
                player_info['squad_emoji'] = None
            
            if registration_type in formatted_squad:
                formatted_squad[registration_type].append(player_info)
        
        return jsonify({
            'success': True,
            'squad_add': formatted_squad['add'],
            'squad_chair': formatted_squad['chair'],
            'squad_maybe': formatted_squad['maybe'],
            'squad_remove': formatted_squad['remove'],
            'next_matchday_date': helpers.get_next_matchday_formatted()
        })
    except Exception as e:
        print(f"Error in get_next_matchday_squad: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/player/<int:player_id>/season-stats')
def get_player_season_stats(player_id):
    """Get player's season-by-season stats (mock data)"""
    season_stats = MOCK_SEASON_STATS.get(player_id, [
        {'season': 2024, 'games_played': 10, 'goals': 2, 'assists': 3, 'own_goals': 0},
        {'season': 2023, 'games_played': 8, 'goals': 1, 'assists': 2, 'own_goals': 0},
    ])
    
    return jsonify({
        'success': True,
        'season_stats': season_stats
    })

@app.route('/api/player/<int:player_id>/streaks')
def get_player_streaks(player_id):
    """Get player's win/loss streaks (mock data)"""
    streaks = MOCK_STREAKS.get(player_id, {'win_streak': 0, 'loss_streak': 0})
    
    return jsonify({
        'success': True,
        'win_streak': streaks['win_streak'],
        'loss_streak': streaks['loss_streak'],
    })

def _money(value):
    """Convert DB numeric (Decimal/None) to a JSON-friendly number"""
    if value is None:
        return 0
    value = float(value)
    return int(value) if value.is_integer() else round(value, 2)

@app.route('/api/player/<int:player_id>/balance')
def get_player_balance(player_id):
    """Get player's current balance, total paid and recent payments history"""
    try:
        individual_balance = database.get_individual_balance(player_id)
        history = []
        for payment in database.get_payments_history(player_id):
            history.append({
                'date': helpers.format_date(payment[0]) if payment[0] else None,
                'money_given': _money(payment[1]),
                'balance_change': _money(payment[2]),
                'balance_by_date': _money(payment[3]),
            })

        return jsonify({
            'success': True,
            'balance': _money(individual_balance[0]) if individual_balance else 0,
            'total_paid': _money(individual_balance[1]) if individual_balance else 0,
            'history': history,
        })
    except Exception as e:
        print(f"Error in get_player_balance: {str(e)}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/player/<int:player_id>/last-games-performance')
def get_player_last_games_performance(player_id):
    """Get player's last 10 games performance as W/D/L string"""
    try:
        # Get last individual games
        last_games = database.get_last_individual_games(player_id)
        
        # Take last 10 games, reverse to show oldest first
        recent_games = last_games[:10][::-1]
        
        performance = []
        for stat in recent_games:
            squad = stat[6]
            score_corn = stat[1]
            score_tomato = stat[2]
            
            if squad is None or score_corn is None or score_tomato is None:
                continue  # Skip invalid games
            
            if squad == constants.SQUAD_CORN:
                if score_corn > score_tomato:
                    performance.append('W')
                elif score_corn < score_tomato:
                    performance.append('L')
                else:
                    performance.append('D')
            elif squad == constants.SQUAD_TOMATO:
                if score_corn < score_tomato:
                    performance.append('W')
                elif score_corn > score_tomato:
                    performance.append('L')
                else:
                    performance.append('D')
        
        # Join into string
        performance_str = ''.join(performance)
        
        return jsonify({
            'success': True,
            'performance': performance_str
        })
    except Exception as e:
        print(f"Error in get_player_last_games_performance: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/current-season-stats')
def get_current_season_stats():
    """Get current season stats overview"""
    try:
        current_year = datetime.now().year
        season_score = database.get_season_score(current_year)
        season_stats = database.get_season_stats(current_year, 100)
        
        # Format season stats
        players = []
        for i, player in enumerate(season_stats, 1):
            players.append({
                'rank': i,
                'first_name': player[0],
                'last_name': player[1],
                'games_played': player[2],
                'goals': player[3],
                'assists': player[4],
                'own_goals': player[5]
            })
        
        return jsonify({
            'success': True,
            'season_score': {
                'corn_wins': season_score[1],
                'draws': season_score[2],
                'tomato_wins': season_score[0]
            },
            'players': players,
            'year': current_year
        })
    except Exception as e:
        print(f"Error in get_current_season_stats: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/alltime-stats')
def get_alltime_stats():
    """Get alltime stats and header info for alltime stats screen"""
    try:
        stats = database.get_alltime_stats(1000)
        stats_goals_games = database.get_alltime_stats_games_goal()
        players = []
        for player in stats:
            players.append({
                'first_name': player[0],
                'last_name': player[1],
                'games_played': player[2],
                'goals': player[3],
                'assists': player[4],
                'own_goals': player[5],
                'avg_goals': player[6],
                'wins': player[7],
                'win_rate': player[8],
            })
        return jsonify({
            'success': True,
            'stats': players,
            'stats_goals_games': stats_goals_games
        })
    except Exception as e:
        print(f"Error in get_alltime_stats: {str(e)}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/games-log')
def get_games_log():
    """Get list of all played games with score and top scorer(s)"""
    try:
        player_id = request.args.get('player_id', type=int)
        games = []
        for game in database.get_games_log(player_id):
            games.append({
                'date': f"{helpers.format_date(game[0])}",
                'score_corn': game[1],
                'score_tomato': game[2],
                'top_scorers': game[3],
                'top_goals': game[4],
                'player_played': bool(game[6]),
                'player_squad_emoji': constants.SQUAD_CORN_EMOJI if game[5] == constants.SQUAD_CORN
                    else constants.SQUAD_TOMATO_EMOJI if game[5] == constants.SQUAD_TOMATO else None,
            })
        return jsonify({'success': True, 'games': games})
    except Exception as e:
        print(f"Error in get_games_log: {str(e)}")
        return jsonify({'success': False, 'error': str(e)}), 500

def _record_number(value):
    """DB numeric (int/Decimal/float) -> JSON number: 1704.0 -> 1704, 66.67 -> 66.67"""
    if value is None:
        return 0
    number = float(value)
    return int(number) if number.is_integer() else round(number, 2)

def _record_date(value):
    return helpers.format_date(value) if value else None

def _record_squad_emoji(squad):
    if squad == constants.SQUAD_CORN:
        return constants.SQUAD_CORN_EMOJI
    if squad == constants.SQUAD_TOMATO:
        return constants.SQUAD_TOMATO_EMOJI
    return None

def _record_streak(row, emoji):
    # name, length, start date, end date
    return {'type': 'player', 'emoji': emoji, 'name': row[0], 'value': _record_number(row[1]),
            'unit': None, 'detail': f"{_record_date(row[2])} - {_record_date(row[3])}"}

def _record_per_game(row, emoji='⚽️'):
    # name, count, game date
    return {'type': 'player', 'emoji': emoji, 'name': row[0], 'value': _record_number(row[1]),
            'unit': None, 'detail': _record_date(row[2])}

def _record_total(emoji, unit=None, value_index=1):
    def build(row):
        return {'type': 'player', 'emoji': emoji, 'name': row[0],
                'value': _record_number(row[value_index]), 'unit': unit, 'detail': None}
    return build

def _record_pair(row):
    # player 1, player 2, games together, ..., squad
    return {'type': 'pair', 'emoji': _record_squad_emoji(row[6]) or '🤝', 'names': [row[0], row[1]],
            'value': _record_number(row[2]), 'unit': 'игр'}

def _record_game(detail_label=None):
    # game date, corn score, tomato score[, difference / total goals]
    def build(row):
        return {'type': 'game', 'emoji': '🔝', 'date': _record_date(row[0]),
                'score_corn': row[1], 'score_tomato': row[2],
                'detail': f"{detail_label} {row[3]}" if detail_label else None}
    return build

# Same sections, order and SQL queries as records_template.txt / command_records.build_records_text()
RECORD_SECTIONS = [
    ('Самые длинные победные серии', constants.SQL_WIN_STREAKS, lambda r: _record_streak(r, '🙌')),
    ('Самые длинные серии поражений', constants.SQL_LOSING_STREAKS, lambda r: _record_streak(r, '🙌')),
    ('Активные победные серии', constants.SQL_ACTIVE_WIN_STREAKS, lambda r: _record_streak(r, '🙌')),
    ('Активные серии поражений', constants.SQL_ACTIVE_LOSS_STREAKS, lambda r: _record_streak(r, '🙌')),
    ('Активные серии сыгранных игр подряд без пропуска', constants.SQL_GAMES_PLAYED_STREAK_ACTIVE, lambda r: _record_streak(r, '🙌')),
    ('Наибольшее количество голов за одну игру', constants.SQL_TOP_GOALS_PER_GAME, _record_per_game),
    ('Наибольшее количество голов за всю историю', constants.SQL_TOP_GOALS_ALLTIME, _record_total('⚽️')),
    ('Наибольшее количество асистов за одну игру', constants.SQL_TOP_ASSISTS_PER_GAME, _record_per_game),
    ('Наибольшее количество асистов за всю историю', constants.SQL_TOP_ASSISTS_ALLTIME, _record_total('⚽️')),
    ('Наибольшее количество автоголов за одну игру', constants.SQL_TOP_OWN_GOALS_PER_GAME, _record_per_game),
    ('Наибольшее количество автоголов за всю историю', constants.SQL_WHO_SCORED_MOST_OWN_GOALS, _record_total('⚽️')),
    ('Самый высокий процент побед', constants.SQL_WHO_HAS_THE_HIGHER_WIN_RATE, _record_total('🔥', '%', value_index=3)),
    ('Наибольшее количество денег, которые сдал игрок за всю историю', constants.SQL_WHO_PAID_THE_MOST_MONEY, _record_total('💲', 'р.')),
    ('Кто сыграл больше всего игр за Кукурузу', constants.SQL_WHO_PLAYED_THE_MOST_GAMES_FOR_CORN, _record_total('🌽')),
    ('Кто сыграл больше всего игр за Помидоры', constants.SQL_WHO_PLAYED_THE_MOST_GAMES_FOR_TOMATO, _record_total('🍅')),
    ('Кто сидел на стуле наибольшее количество раз', constants.SQL_WHO_SAT_ON_A_CHAIR_THE_MOST_TIMES, _record_total('🪑')),
    ('Пары игроков, которые сыграли больше всего игр вместе', constants.SQL_TOP_PLAYER_PAIRS, _record_pair),
    ('Средние показатели лиги', constants.SQL_AVERAGE_AGE_AND_HEIGHT, None),
    ('Наибольшее количество сыгранных игр подряд без пропусков', constants.SQL_ATTENDANCE_STREAKS, lambda r: _record_streak(r, '🔁')),
    ('Топ игр с наиболее разгромным счетом', constants.SQL_MAX_GOAL_DIFFERENCE, _record_game('разница')),
    ('Топ игр с наибольшим количеством голов', constants.SQL_MAX_TOTAL_GOALS_PER_GAME_BY_TWO_TEAMS, _record_game('всего голов')),
    ('Топ игр, где Кукурузы забили наибольшее количество голов за игру', constants.SQL_MOST_GOALS_SCORED_PER_GAME_BY_CORN, _record_game()),
    ('Топ игр, где Помидоры забили наибольшее количество голов за игру', constants.SQL_MOST_GOALS_SCORED_PER_GAME_BY_TOMATO, _record_game()),
]

def _read_records_sql(file_name):
    with open(os.path.join('SQL Queries', file_name), 'r') as file:
        return file.read()

def _average_age_and_height_items(rows):
    if not rows or rows[0][0] is None:
        return []
    height, age = rows[0][0], rows[0][1]
    return [
        {'type': 'stat', 'emoji': '👢', 'label': 'Средний рост', 'value': f"{height:.2f} см"},
        {'type': 'stat', 'emoji': '👴', 'label': 'Средний возраст', 'value': f"{age:.2f} лет"},
    ]

@app.route('/api/records')
def get_records():
    """League records: same SQL queries as the /records bot command (command_records.py)"""
    try:
        summary = [
            {'label': 'Общее количество игр, которое мы сыграли',
             'value': _record_number(database.execute_sql_query_return_one(_read_records_sql(constants.SQL_HOW_MANY_GAMES_WE_PLAYED)))},
            {'label': 'Общее количество игр, которое было отменено',
             'value': _record_number(database.execute_sql_query_return_one(_read_records_sql(constants.SQL_HOW_MANY_GAMES_WERE_CANCELLED)))},
        ]

        sections = []
        for title, sql_file, build_item in RECORD_SECTIONS:
            rows = database.execute_sql_query_return_many(_read_records_sql(sql_file))
            if build_item is None:
                items = _average_age_and_height_items(rows)
            else:
                items = [build_item(row) for row in rows]
            sections.append({'title': title, 'items': items})

        return jsonify({'success': True, 'summary': summary, 'sections': sections})
    except Exception as e:
        print(f"Error in get_records: {str(e)}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/register-player-action', methods=['POST'])
def register_player_action():
    """Register player action (mock implementation)"""
    try:
        data = request.get_json()
        action = data.get('action')
        
        # Validate action
        if action not in ['add', 'remove', 'chair', 'maybe']:
            return jsonify({'success': False, 'error': 'Invalid action'}), 400
        
        # For demo, always succeed
        return jsonify({
            'success': True,
            'message': f'Эта кнопка пока не работает ❌'
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
