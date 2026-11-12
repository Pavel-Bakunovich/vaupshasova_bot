WITH ranked_games AS (
    SELECT
        g.id,
        EXISTS (
            SELECT 1
            FROM Matchday AS m
            WHERE m.Game_ID = g.id
              AND m.Player_ID = %s
              AND m.Type = 'add'
        ) AS attended,
        ROW_NUMBER() OVER (ORDER BY g.Game_Date DESC, g.id DESC) AS game_rank
    FROM Games AS g
    WHERE g.Played = TRUE
      AND g.Game_Date <= CURRENT_DATE
),
latest_game AS (
    SELECT attended
    FROM ranked_games
    WHERE game_rank = 1
),
streak_boundary AS (
    SELECT
        latest.attended,
        COALESCE(
            MIN(game.game_rank) FILTER (
                WHERE game.attended IS DISTINCT FROM latest.attended
            ),
            MAX(game.game_rank) + 1
        ) AS first_different_game_rank
    FROM latest_game AS latest
    CROSS JOIN ranked_games AS game
    GROUP BY latest.attended
)
SELECT
    boundary.attended,
    COUNT(*) AS streak_length
FROM streak_boundary AS boundary
JOIN ranked_games AS game
  ON game.game_rank < boundary.first_different_game_rank
GROUP BY boundary.attended;
