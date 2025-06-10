WITH game_outcomes AS (
    -- Determine if each player won or lost each game they participated in
    SELECT 
        m.Player_ID,
        p.Friendly_First_Name || ' ' || p.Friendly_Last_Name AS player_name,
        g.id AS game_id,
        g.Game_Date,
        CASE 
            WHEN (m.Squad = 'Tomato' AND g.Score_Tomato < g.Score_Corn) OR 
                 (m.Squad = 'Corn' AND g.Score_Corn < g.Score_Tomato) THEN 1
            ELSE 0
        END AS is_loss
    FROM Matchday m
    JOIN Games g ON m.Game_ID = g.id
    JOIN Players p ON m.Player_ID = p.id
    WHERE g.Played = TRUE
    ORDER BY m.Player_ID, g.Game_Date
),

streaks AS (
    -- Calculate losing streaks by identifying when the loss/win status changes
    SELECT 
        Player_ID,
        player_name,
        game_id,
        Game_Date,
        is_loss,
        SUM(CASE WHEN is_loss = 0 THEN 1 ELSE 0 END) OVER (PARTITION BY Player_ID ORDER BY Game_Date) AS streak_group
    FROM game_outcomes
),

streak_lengths AS (
    -- Count the length of each losing streak
    SELECT 
        Player_ID,
        player_name,
        streak_group,
        COUNT(*) AS streak_length,
        MIN(Game_Date) AS streak_start,
        MAX(Game_Date) AS streak_end
    FROM streaks
    WHERE is_loss = 1
    GROUP BY Player_ID, player_name, streak_group
    HAVING COUNT(*) > 0
)

-- Get the longest losing streak for each player
SELECT 
    player_name,
    MAX(streak_length) AS losing_streak,
    streak_start,
    streak_end
FROM streak_lengths
GROUP BY Player_ID, player_name, streak_start, streak_end
HAVING MAX(streak_length) > 6
ORDER BY losing_streak DESC, player_name;