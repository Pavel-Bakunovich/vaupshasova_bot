WITH player_games AS (
  SELECT
    g.game_date,
    g.id AS game_id,
    CASE
      WHEN m.squad = 'Tomato' AND g.score_tomato  > g.score_corn THEN 'win'
      WHEN m.squad = 'Corn'   AND g.score_corn    > g.score_tomato THEN 'win'
      WHEN g.score_tomato = g.score_corn THEN 'draw'
      ELSE 'loss'
    END AS result
  FROM matchday m
  JOIN games g ON m.game_id = g.id
  WHERE m.player_id = {player_id}
    AND g.played = TRUE
    AND g.game_date <= CURRENT_DATE
    AND m.type = 'add'
  ORDER BY g.game_date DESC, g.id DESC
),
annotated AS (
  SELECT
    *,
    CASE WHEN result = 'loss' THEN 0 ELSE 1 END AS not_loss,
    SUM(CASE WHEN result = 'loss' THEN 0 ELSE 1 END)
      OVER (ORDER BY game_date DESC, game_id DESC ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS sum_not_loss
  FROM player_games
),
trailing_losses AS (
  -- rows that belong to the current (most recent) contiguous block of losses
  SELECT * FROM annotated WHERE sum_not_loss = 0
)
SELECT
  p.id AS player_id,
  COALESCE((SELECT COUNT(*) FROM trailing_losses), 0) AS streak_length,
  (SELECT MIN(game_date) FROM trailing_losses) AS streak_start_date,
  (SELECT MAX(game_date) FROM trailing_losses) AS streak_end_date
FROM players p
WHERE p.id = {player_id}