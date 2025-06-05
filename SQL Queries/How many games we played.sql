SELECT COUNT(*) FROM Games
WHERE Played = TRUE
      AND current_date >= game_date