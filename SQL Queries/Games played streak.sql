WITH
  -- Step 1: Get all games that were actually played and assign a dense universal rank.
  -- We filter out cancelled games (Played = FALSE) immediately, as they don't affect streaks.
  Played_Games_Ranked AS (
    SELECT
      ID,
      Game_Date,
      ROW_NUMBER() OVER (ORDER BY Game_Date) AS universal_game_rank
    FROM
      Games
    WHERE
      Played = TRUE
  ),
  
  -- Step 2: For each player, find their games and assign a player-specific rank.
  -- The difference between the universal rank and the player rank will be constant
  -- for any single, unbroken streak of games.
  Player_Game_Streaks AS (
    SELECT
      md.Player_ID,
      pgr.Game_Date,
      -- This calculation creates the "streak group" identifier.
      (pgr.universal_game_rank - ROW_NUMBER() OVER (PARTITION BY md.Player_ID ORDER BY pgr.Game_Date)) AS streak_group
    FROM
      Matchday AS md
      JOIN Played_Games_Ranked AS pgr
        ON md.Game_ID = pgr.ID
  ),
  
  -- Step 3: Group by the player and the streak identifier to calculate the length,
  -- start, and end of each individual streak.
  Streak_Details AS (
    SELECT
      Player_ID,
      COUNT(*) AS streak_length,
      MIN(Game_Date) AS streak_start,
      MAX(Game_Date) AS streak_end
    FROM
      Player_Game_Streaks
    GROUP BY
      Player_ID,
      streak_group
  ),
  
  -- Step 4: Rank each player's streaks to find their longest one.
  -- In case of a tie in length, the most recent streak is chosen.
  Ranked_Player_Streaks AS (
    SELECT
      Player_ID,
      streak_length,
      streak_start,
      streak_end,
      ROW_NUMBER() OVER (PARTITION BY Player_ID ORDER BY streak_length DESC, streak_end DESC) AS rank_num
    FROM
      Streak_Details
  )
  
-- Final Step: Select the top-ranked streak for each player and join to get their name.
SELECT
  p.Friendly_First_Name,
  p.Friendly_Last_name,
  rps.streak_length AS top_streak,
  rps.streak_start,
  rps.streak_end
FROM
  Ranked_Player_Streaks AS rps
  JOIN Players AS p
    ON rps.Player_ID = p.ID
WHERE
  rps.rank_num = 1
ORDER BY
  top_streak DESC,
  p.Friendly_Last_name;