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
-- Identify streak-breaking games (non-losses break a loss streak)
streak_breakers AS (
    SELECT 
        pgs.Player_ID,
        pgs.Game_Date,
        pgs.game_id,
        pgs.reverse_order,
        pgs.forward_order
    FROM player_games_sequence pgs
    WHERE pgs.result != 'loss'
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
-- Calculate loss streaks
loss_streaks AS (
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
    WHERE rsb.result = 'loss'
),
-- Get current active loss streak for each player
current_loss_streaks AS (
    SELECT DISTINCT
        ls.Player_ID,
        ls.streak_length as loss_streak,
        ls.streak_start_date,
        ls.streak_end_date as most_recent_loss_date
    FROM loss_streaks ls
    WHERE ls.reverse_order = 1  -- Most recent game
      AND ls.result = 'loss'    -- That was a loss
)
SELECT 
    p.id as player_id,
    COALESCE(p.Friendly_First_Name, p.Telegram_First_Name) as first_name,
    COALESCE(p.Friendly_Last_Name, p.Telegram_Last_Name) as last_name,
    COALESCE(cls.loss_streak, 0) as active_loss_streak,
    cls.streak_start_date,
    cls.most_recent_loss_date
FROM Players p
LEFT JOIN current_loss_streaks cls ON p.id = cls.Player_ID
WHERE COALESCE(cls.loss_streak, 0) > 1
ORDER BY active_loss_streak DESC, first_name, last_name;