WITH player_squad_games AS (
    SELECT 
        p.id AS player_id,
        p.Friendly_First_Name || ' ' || COALESCE(p.Friendly_Last_Name, '') AS player_name,
        m.Game_ID,
        m.Squad,
        g.Score_Tomato,
        g.Score_Corn,
        CASE 
            WHEN (m.Squad = 'Tomato' AND g.Score_Tomato > g.Score_Corn) OR
                 (m.Squad = 'Corn' AND g.Score_Corn > g.Score_Tomato) THEN TRUE
            WHEN g.Score_Tomato = g.Score_Corn THEN NULL  -- Draw
            ELSE FALSE
        END AS is_win
    FROM Players p
    JOIN Matchday m ON p.id = m.Player_ID
    JOIN Games g ON m.Game_ID = g.id
    WHERE g.Played = TRUE OR g.Played IS NULL
),

player_pairs AS (
    SELECT 
        a.player_id AS player1_id,
        a.player_name AS player1_name,
        b.player_id AS player2_id,
        b.player_name AS player2_name,
        a.Game_ID,
        a.Squad,
        a.is_win
    FROM player_squad_games a
    JOIN player_squad_games b ON 
        a.Game_ID = b.Game_ID AND 
        a.Squad = b.Squad AND 
        a.player_id < b.player_id
),

pair_stats AS (
    SELECT 
        player1_name,
        player2_name,
        player1_id,
        player2_id,
        squad,
        COUNT(*) AS games_played_together,
        COUNT(CASE WHEN is_win = TRUE THEN 1 END) AS wins,
        COUNT(CASE WHEN is_win = FALSE THEN 1 END) AS losses,
        COUNT(CASE WHEN is_win IS NULL THEN 1 END) AS draws
    FROM player_pairs
    GROUP BY player1_name, player2_name, player1_id, player2_id, squad
)

SELECT 
    player1_name,
    player2_name,
    games_played_together,
    wins,
    losses,
    draws,
    squad,
    CASE 
        WHEN games_played_together > 0 
        THEN ROUND((wins::numeric / games_played_together) * 100, 1) 
        ELSE 0 
    END AS win_percentage
FROM pair_stats
ORDER BY games_played_together DESC, win_percentage DESC
LIMIT 10