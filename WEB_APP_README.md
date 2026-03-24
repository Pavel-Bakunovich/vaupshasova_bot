# Telegram Mini-App Web Implementation

## Overview
A comprehensive, mobile-optimized web app for the Telegram mini-app that allows players to view their stats and register for matchdays.

## Features Implemented

### 1. Home Page
- **Player Information Card**: Displays player name with quick stats
- **Personal Stats Summary**: Shows games played, goals, assists, and own goals
- **Next Matchday Squad List**: Displays all players registered for the upcoming match with their teams
- **Registration Buttons**: Quick action buttons to register for next matchday:
  - ✅ **Приду** (Add - I'll play)
  - ❌ **Не приду** (Remove - I won't play)
  - 🪑 **Стану** (Chair - I'll referee)
  - ❓ **Может** (Maybe - I'm unsure)

### 2. Detailed Stats Screens
Accessible via navigation buttons from the home page:

#### **📊 Full Personal Stats**
- Complete lifetime statistics
- Total games, goals, assists, own goals
- Games played for each team (Corn/Tomato)

#### **📈 Season-by-Season Stats**
- Table view of stats for each season
- Games played, goals, assists, and own goals per season
- Historical data comparison

#### **🌟 All-Time Stats**
- Comprehensive lifetime statistics
- Current win/loss streaks
- Team distribution (games for Corn vs Tomato)

#### **💰 Financial Balance**
- Player's financial balance
- Color-coded display (green for positive, red for negative)
- Shows financial status relative to other players

#### **🏅 Records** 
- Ready for integration with detailed records queries
- Placeholder for personal achievement records

## Technical Architecture

### Backend API Endpoints

All endpoints are implemented in `telegram_mini_app.py` using Flask:

```
GET  /                                    - Serve the main web app
GET  /api/player/<telegram_id>            - Get player info and all-time stats
GET  /api/next-matchday-squad/<telegram_id> - Get next matchday squad list
GET  /api/player/<player_id>/season-stats - Get season-by-season statistics
GET  /api/player/<player_id>/streaks      - Get active win/loss streaks
GET  /api/player/<player_id>/balance      - Get player's financial balance
POST /api/register-player-action          - Register player action for next matchday
```

### Frontend Architecture

**File**: `templates/index.html`
- Single-page application (SPA) with client-side routing
- Telegram WebApp API integration for theme and user data
- Responsive CSS Grid layout
- Modern, smooth screen transitions

### Key Features

1. **Telegram Integration**
   - Automatically detects user from Telegram WebApp
   - Theme-aware styling (dark/light mode)
   - No authentication needed (secure via Telegram)

2. **Responsive Design**
   - Mobile-optimized for Telegram mini-app
   - Works on all screen sizes
   - Touch-friendly button sizes

3. **Real-time Data**
   - Fetches live stats from PostgreSQL database
   - Shows current squad registrations
   - Updates on player actions

4. **Fast Navigation**
   - No page reloads - smooth transitions between screens
   - Instant response to user actions
   - Animated screen transitions

## Database Integration

The app leverages existing database functions:

- `get_player_by_telegram_id()` - Player lookup
- `get_individual_stats()` - Lifetime stats
- `get_individual_stats_by_season()` - Season breakdown
- `get_squad()` - Next matchday roster
- `get_individual_balance()` - Financial data
- `get_active_win_streak_by_player()` - Win streaks
- `get_active_loss_streak_by_player()` - Loss streaks
- `register_player_matchday()` - New registration
- `update_registraion_player_matchday()` - Update registration
- `find_registraion_player_matchday()` - Check existing registration

## Running the App

### Prerequisites
- Python 3.9+
- Flask with all dependencies from `requirements.txt`
- PostgreSQL database with populated game data
- Environment variables: `DATABASE_URL`, `TELEGRAM_API_TOKEN`

### Start the Web App
```bash
python3 telegram_mini_app.py
```

The app will start on `http://0.0.0.0:5000/`

### Telegram Configuration
1. Point your Telegram mini-app to: `https://your-domain.com/` 
2. The app will automatically detect the user and load their data

## Future Enhancements

Potential features to add:
1. **Records Screen**: Display personal achievement records
2. **Team Stats**: Show squad aggregate statistics
3. **Leaderboard**: Display player rankings
4. **Match History**: Show detailed game history with stats
5. **Notifications**: Push notifications for matchday updates
6. **Player Search**: Find other players' stats

## File Structure

```
/workspaces/vaupshasova_bot/
├── telegram_mini_app.py          # Flask backend with API endpoints
├── templates/
│   └── index.html               # Single-page web app frontend
├── mini-app/
│   └── app.js                   # Legacy reference file
└── WEB_APP_README.md            # This file
```

## Notes

- The web app uses raw SQL queries via the existing `psycopg2` connection pool
- All player lookups are based on Telegram ID for security
- The app respects Telegram theme settings automatically
- State is managed client-side for instant UI updates
- All data is fetched asynchronously to prevent blocking

## Troubleshooting

**App not loading**: 
- Check `DATABASE_URL` environment variable is set
- Verify PostgreSQL is running and accessible
- Check Flask logs for database errors

**Stats not showing**:
- Ensure player exists in database
- Check player has games recorded
- Verify SQL query functions are working

**Registration not working**:
- Check player is trying to register for next matchday
- Verify game_id for next matchday exists
- Check database transaction logs

## Contact
For issues or feature requests, refer to the main bot documentation.
