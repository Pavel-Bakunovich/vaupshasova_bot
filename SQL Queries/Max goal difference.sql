SELECT 
    Game_Date,
    Score_Corn,
    Score_Tomato,
    ABS(Score_Corn - Score_Tomato) AS Goal_Difference
FROM Games
WHERE Played = TRUE AND ABS(Score_Corn - Score_Tomato) IS NOT NULL AND ABS(Score_Corn - Score_Tomato) > 17
ORDER BY Goal_Difference DESC