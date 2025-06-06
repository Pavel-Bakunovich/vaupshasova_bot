SELECT Friendly_First_Name || ' ' || Friendly_Last_Name AS player_name, Goals, Game_Date FROM Matchday
INNER JOIN Players ON Players.ID = Matchday.Player_ID
INNER JOIN Games ON Games.ID = Matchday.Game_ID
WHERE Goals >= 11
ORDER BY Goals DESC