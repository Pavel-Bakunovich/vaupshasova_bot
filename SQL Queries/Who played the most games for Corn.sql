SELECT 
    Friendly_First_Name || ' ' || Friendly_Last_Name AS player_name,
    SUM(CASE  
            WHEN Squad = 'Corn'
            THEN 1 ELSE 0 END) as Games_played_for_Corn
FROM 
    Matchday
	
INNER JOIN Games ON Games.id = Matchday.Game_ID
INNER JOIN Players ON Players.id = Matchday.Player_Id
where Matchday.type like 'add'
	and Games.game_date <= current_date
	and Games.Played = TRUE
GROUP BY 
    Players.Id, Player_Id,Players.Friendly_First_Name, Players.Friendly_Last_Name
ORDER BY 
    Games_played_for_Corn DESC
LIMIT 5