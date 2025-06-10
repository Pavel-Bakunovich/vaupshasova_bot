SELECT Friendly_First_Name || ' ' || Friendly_Last_Name AS player_name, COUNT(Type) FROM Matchday
INNER JOIN Players ON Players.ID = Matchday.Player_ID
WHERE Type like 'chair'
GROUP BY Matchday.Player_ID, Players.Friendly_First_Name, Players.Friendly_Last_Name
ORDER BY COUNT(Type) DESC
LIMIT 3