WITH
  Played_Games_Ranked AS (
    SELECT
      id,
      Game_Date,
      ROW_NUMBER() OVER (ORDER BY Game_Date, id) AS universal_game_rank
    FROM Games
    WHERE Played = TRUE and Game_Date <= CURRENT_DATE
  ),

  Player_Game_Streaks AS (
    SELECT
      md.Player_ID,
      pgr.Game_Date,
      pgr.universal_game_rank,
      ROW_NUMBER() OVER (PARTITION BY md.Player_ID ORDER BY pgr.Game_Date, pgr.id) AS player_game_rank,
      (pgr.universal_game_rank - ROW_NUMBER() OVER (PARTITION BY md.Player_ID ORDER BY pgr.Game_Date, pgr.id)) AS streak_group
    FROM Matchday AS md
    JOIN Played_Games_Ranked AS pgr
      ON md.Game_ID = pgr.id
    WHERE md.Type = 'add'
  ),

  Streak_Details AS (
    SELECT
      Player_ID,
      streak_group,
      COUNT(*) AS streak_length,
      MIN(Game_Date) AS streak_start,
      MAX(Game_Date) AS streak_end,
      MAX(universal_game_rank) AS streak_end_rank
    FROM Player_Game_Streaks
    GROUP BY Player_ID, streak_group
  ),

  Latest_Played_Rank AS (
    SELECT MAX(universal_game_rank) AS latest_game_rank
    FROM Played_Games_Ranked
  ),

  Current_Played_Streaks AS (
    SELECT
      sd.Player_ID,
      sd.streak_length,
      sd.streak_start,
      sd.streak_end
    FROM Streak_Details AS sd
    JOIN Latest_Played_Rank AS lpr
      ON sd.streak_end_rank = lpr.latest_game_rank
  )

SELECT
  p.Friendly_First_Name || ' ' || p.Friendly_Last_Name AS player_name,
  cps.streak_length AS active_games_played_streak,
  cps.streak_start,
  cps.streak_end
FROM Current_Played_Streaks AS cps
JOIN Players AS p
  ON cps.Player_ID = p.ID
WHERE cps.streak_length > 3
ORDER BY
  cps.streak_length DESC,
  p.Friendly_Last_Name,
  p.Friendly_First_Name;