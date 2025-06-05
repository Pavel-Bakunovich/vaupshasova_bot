SELECT Players.Friendly_First_Name, Players.Friendly_Last_Name, Own_Goals, Game_Date FROM Matchday
INNER JOIN Players ON Players.ID = Matchday.Player_ID
INNER JOIN Games ON Games.ID = Matchday.Game_ID
WHERE Own_Goals >= 1
ORDER BY Own_Goals DESC