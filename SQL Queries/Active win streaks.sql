WITH player_game_results AS (
    SELECT 
        m.Player_ID,
        g.Game_Date,
        g.id as game_id,
        CASE 
            WHEN m.Squad = 'Tomato' AND g.Score_Tomato > g.Score_Corn THEN 'win'
            WHEN m.Squad = 'Corn' AND g.Score_Corn > g.Score_Tomato THEN 'win'
            WHEN m.Squad = 'Tomato' AND g.Score_Tomato < g.Score_Corn THEN 'loss'
            WHEN m.Squad = 'Corn' AND g.Score_Corn < g.Score_Tomato THEN 'loss'
            ELSE 'draw'
        END as result
    FROM Matchday m
    JOIN Games g ON m.Game_ID = g.id
    WHERE g.Played = TRUE
    AND m.Type = 'add'  -- Only include games where player actually played
    AND g.Game_Date <= CURRENT_DATE
),
-- Get chronological sequence of games where player actually played
player_games_sequence AS (
    SELECT 
        pgr.Player_ID,
        pgr.Game_Date,
        pgr.game_id,
        pgr.result,
        ROW_NUMBER() OVER (PARTITION BY pgr.Player_ID ORDER BY pgr.Game_Date DESC, pgr.game_id DESC) as reverse_order,
        ROW_NUMBER() OVER (PARTITION BY pgr.Player_ID ORDER BY pgr.Game_Date ASC, pgr.game_id ASC) as forward_order
    FROM player_game_results pgr
),
-- Identify streak-breaking games (non-wins)
streak_breakers AS (
    SELECT 
        pgs.Player_ID,
        pgs.Game_Date,
        pgs.game_id,
        pgs.reverse_order,
        pgs.forward_order
    FROM player_games_sequence pgs
    WHERE pgs.result != 'win'
),
-- For each player's game, find the most recent streak breaker
recent_streak_breakers AS (
    SELECT 
        pgs.Player_ID,
        pgs.Game_Date,
        pgs.game_id,
        pgs.result,
        pgs.reverse_order,
        pgs.forward_order,
        COALESCE(MAX(sb.forward_order) OVER (
            PARTITION BY pgs.Player_ID 
            ORDER BY pgs.forward_order
            ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
        ), 0) as last_breaker_order
    FROM player_games_sequence pgs
    LEFT JOIN streak_breakers sb 
        ON pgs.Player_ID = sb.Player_ID 
        AND pgs.forward_order >= sb.forward_order
),
-- Calculate win streaks
win_streaks AS (
    SELECT 
        rsb.Player_ID,
        rsb.Game_Date,
        rsb.game_id,
        rsb.result,
        rsb.reverse_order,
        rsb.forward_order - rsb.last_breaker_order as streak_length,
        MIN(rsb.Game_Date) OVER (
            PARTITION BY rsb.Player_ID, rsb.last_breaker_order
        ) as streak_start_date,
        MAX(rsb.Game_Date) OVER (
            PARTITION BY rsb.Player_ID, rsb.last_breaker_order
        ) as streak_end_date
    FROM recent_streak_breakers rsb
    WHERE rsb.result = 'win'
),
-- Get current active win streak for each player
current_streaks AS (
    SELECT DISTINCT
        ws.Player_ID,
        ws.streak_length as win_streak,
        ws.streak_start_date,
        ws.streak_end_date as most_recent_win_date
    FROM win_streaks ws
    WHERE ws.reverse_order = 1  -- Most recent game
    AND ws.result = 'win'       -- That was a win
)
SELECT 
    p.id as player_id,
    COALESCE(p.Friendly_First_Name, p.Telegram_First_Name) as first_name,
    COALESCE(p.Friendly_Last_Name, p.Telegram_Last_Name) as last_name,
    COALESCE(cs.win_streak, 0) as active_win_streak,
    cs.streak_start_date,
    cs.most_recent_win_date
FROM Players p
LEFT JOIN current_streaks cs ON p.id = cs.Player_ID
ORDER BY active_win_streak DESC, first_name, last_name;