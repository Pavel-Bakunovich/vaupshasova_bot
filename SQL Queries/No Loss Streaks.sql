WITH player_games AS (
    SELECT 
        p.id AS player_id,
        p.Friendly_First_Name AS first_name,
        p.Friendly_Last_Name AS last_name,
        g.id AS game_id,
        g.Game_Date,
        -- Determine if player didn't lose (won or draw)
        CASE 
            WHEN m.Squad = 'Tomato' AND g.Score_Tomato > g.Score_Corn THEN TRUE
            WHEN m.Squad = 'Corn' AND g.Score_Corn > g.Score_Tomato THEN TRUE
            WHEN g.Score_Tomato = g.Score_Corn THEN TRUE  -- Draw is no loss
            ELSE FALSE
        END AS no_loss
    FROM Players p
    JOIN Matchday m ON p.id = m.Player_ID
    JOIN Games g ON m.Game_ID = g.id
    WHERE g.Played = TRUE AND type='add' -- Only count played games
    ORDER BY p.id, g.Game_Date
),

streak_groups AS (
    SELECT 
        player_id,
        first_name,
        last_name,
        game_id,
        Game_Date,
        no_loss,
        -- Create streak groups: new streak starts when no_loss changes from TRUE to FALSE
        SUM(CASE WHEN no_loss = FALSE THEN 1 ELSE 0 END) 
            OVER (PARTITION BY player_id ORDER BY Game_Date, game_id) AS streak_group
    FROM player_games
),

streaks AS (
    SELECT 
        player_id,
        first_name,
        last_name,
        streak_group,
        MIN(Game_Date) AS streak_start,
        MAX(Game_Date) AS streak_end,
        COUNT(*) AS streak_duration,
        -- Check if this is the most recent streak for the player (ongoing)
        MAX(Game_Date) = MAX(MAX(Game_Date)) OVER (PARTITION BY player_id) AS is_current_streak
    FROM streak_groups
    WHERE no_loss = TRUE  -- Only include no-loss games in streaks
    GROUP BY player_id, first_name, last_name, streak_group
)

SELECT 
    first_name AS "Player First Name",
    last_name AS "Player Last Name",
    streak_duration AS "Streak Duration (games)",
    streak_start AS "Date when streak started",
    CASE 
        WHEN is_current_streak THEN NULL  -- Ongoing streak has no end date
        ELSE streak_end 
    END AS "Date when streak ended"
FROM streaks
WHERE streak_duration > 0 --AND is_current_streak is TRUE-- Only include actual streaks
ORDER BY streak_duration DESC, last_name, first_name;