SELECT Players.Friendly_First_Name, Players.Friendly_Last_Name, COUNT(Type) FROM Matchday
INNER JOIN Players ON Players.ID = Matchday.Player_ID
WHERE Type like 'chair'
GROUP BY Matchday.Player_ID, Players.Friendly_First_Name, Players.Friendly_Last_Name
LIMIT 3