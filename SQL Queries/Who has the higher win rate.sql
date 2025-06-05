SELECT 
    Players.Friendly_First_Name, Players.Friendly_Last_Name,
    COUNT(Matchday.Player_ID) as Games_Played,
    SUM(CASE 
        WHEN (Squad = 'Corn' AND Games.score_corn > Games.score_tomato) OR
             (Squad = 'Tomato' AND Games.score_tomato > Games.score_corn)
        THEN 1 ELSE 0 END) AS wins,
    ROUND(
        SUM(CASE 
            WHEN (Squad = 'Corn' AND Games.score_corn > Games.score_tomato) OR
                 (Squad = 'Tomato' AND Games.score_tomato > Games.score_corn)
            THEN 1 ELSE 0 END) * 100.0 / COUNT(*),
        2
    ) AS win_rate_percentage
FROM 
    Matchday
	
INNER JOIN Games ON Games.id = Matchday.Game_ID
INNER JOIN Players ON Players.id = Matchday.Player_Id
where Matchday.type like 'add'
	and Games.game_date <= current_date
	and Games.Played = TRUE
GROUP BY 
    Players.Id, Player_Id,Players.Friendly_First_Name, Players.Friendly_Last_Name
HAVING COUNT(*) > 5
ORDER BY 
    win_rate_percentage DESC
LIMIT 5