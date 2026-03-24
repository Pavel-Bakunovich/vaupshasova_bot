from flask import Flask, render_template, request, jsonify, send_from_directory
import os
from datetime import datetime, timedelta

app = Flask(__name__, template_folder='mini-app/templates', static_folder='mini-app/static')

# Define the new relative or absolute paths for your folders
custom_template_dir = 'web/templates'
custom_static_dir = 'web/static'

# Mock data for demo purposes
MOCK_PLAYERS = {
    123456789: {
        'id': 1,
        'telegram_id': 123456789,
        'first_name': 'Иван',
        'last_name': 'Петров',
        'username': 'ivan_petrov',
        'friendly_first_name': 'Иван',
        'friendly_last_name': 'Петров',
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
        'telegram_id': 123456789,
        'first_name': 'Иван',
        'last_name': 'Петров',
        'username': 'ivan_petrov',
        'friendly_first_name': 'Иван',
        'friendly_last_name': 'Петров',
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

MOCK_BALANCE = {
    1: {'balance': 150, 'total_paid': 350},
    2: {'balance': -50, 'total_paid': 250}
}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/player/<int:telegram_id>')
def get_player(telegram_id):
    """Get player info by Telegram ID (mock data)"""
    # Default to first player if not found
    player_data = MOCK_PLAYERS.get(telegram_id, MOCK_PLAYERS.get(123456789))
    
    if not player_data:
        return jsonify({'success': False, 'error': 'Player not found'}), 404
    
    player_id = player_data['id']
    stats = MOCK_STATS.get(player_id, {
        'games_played': 0,
        'goals': 0,
        'assists': 0,
        'own_goals': 0,
        'games_for_corn': 0,
        'games_for_tomato': 0,
    })
    
    return jsonify({
        'success': True,
        'player': player_data,
        'stats': stats
    })

@app.route('/api/next-matchday-squad/<int:telegram_id>')
def get_next_matchday_squad(telegram_id):
    """Get list of players registered for next matchday (mock data)"""
    next_matchday = (datetime.now() + timedelta(days=7)).strftime('%Y-%m-%d')
    
    return jsonify({
        'success': True,
        'squad': MOCK_SQUAD,
        'next_matchday_date': next_matchday
    })

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

@app.route('/api/player/<int:player_id>/balance')
def get_player_balance(player_id):
    """Get player's financial balance (mock data)"""
    balance_data = MOCK_BALANCE.get(player_id, {'balance': 0, 'total_paid': 0})
    
    return jsonify({
        'success': True,
        'balance': balance_data['balance'],
        'total_paid': balance_data['total_paid'],
    })

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
            'message': f'Action "{action}" registered successfully'
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
