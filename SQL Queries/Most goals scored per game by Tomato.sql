SELECT 
    Game_Date,
    Score_Corn,
    Score_Tomato
FROM Games
WHERE Played = TRUE and Score_Tomato > 30
ORDER BY Score_Tomato DESC