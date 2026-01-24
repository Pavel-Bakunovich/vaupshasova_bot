SELECT 
    Game_Date,
    Score_Corn,
    Score_Tomato,
    ABS(Score_Corn + Score_Tomato) AS Total_Goals
FROM Games
WHERE Played = TRUE AND ABS(Score_Corn + Score_Tomato) IS NOT NULL AND ABS(Score_Corn + Score_Tomato) > 52
ORDER BY Total_Goals DESC