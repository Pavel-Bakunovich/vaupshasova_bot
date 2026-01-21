WITH played_games AS (
    -- Get all played games ordered by date
    SELECT 
        g.id,
        g.Game_Date,
        ROW_NUMBER() OVER (ORDER BY g.Game_Date) AS game_sequence
    FROM Games g
    WHERE g.Played = TRUE
),
player_participation AS (
    -- Get players and their participation in played games
    SELECT 
        p.id,
        CONCAT(p.Friendly_First_Name, ' ', p.Friendly_Last_Name) AS player_name,
        pg.Game_Date,
        pg.game_sequence,
        CASE WHEN m.id IS NOT NULL THEN 1 ELSE 0 END AS participated
    FROM Players p
    CROSS JOIN played_games pg
    LEFT JOIN Matchday m ON p.id = m.Player_ID 
        AND pg.id = m.Game_ID 
        AND m.Type = 'add'
),
streak_groups AS (
    -- Identify streak groups
    SELECT 
        id,
        player_name,
        Game_Date,
        participated,
        game_sequence - ROW_NUMBER() OVER (PARTITION BY id, participated ORDER BY game_sequence) AS streak_id
    FROM player_participation
    WHERE participated = 1
),
streak_counts AS (
    -- Count consecutive games in each streak
    SELECT 
        id,
        player_name,
        streak_id,
        COUNT(*) AS games_at_row,
        MIN(Game_Date) AS streak_start,
        MAX(Game_Date) AS streak_end,
        ROW_NUMBER() OVER (PARTITION BY id ORDER BY COUNT(*) DESC) AS rank
    FROM streak_groups
    GROUP BY id, player_name, streak_id
)
SELECT 
    player_name AS "Player Name",
    games_at_row AS "Max Games-at-row Streak",
    streak_start AS "Date Streak Started",
    streak_end AS "Date Streak Ended"
FROM streak_counts
WHERE rank = 1 and games_at_row > 10
ORDER BY games_at_row DESC