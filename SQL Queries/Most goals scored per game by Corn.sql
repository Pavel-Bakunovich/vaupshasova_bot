SELECT 
    Game_Date,
    Score_Corn,
    Score_Tomato
FROM Games
WHERE Played = TRUE and Score_Corn > 30
ORDER BY Score_Corn DESC