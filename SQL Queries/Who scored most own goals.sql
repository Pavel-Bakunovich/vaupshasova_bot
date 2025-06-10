SELECT Friendly_First_Name || ' ' || Friendly_Last_Name AS player_name, SUM(own_goals) as total_own_goals FROM Matchday
INNER JOIN Players ON Players.ID = Matchday.Player_ID
GROUP BY Matchday.Player_Id, Players.Friendly_First_Name, Players.Friendly_Last_Name
HAVING SUM(own_goals) >= 0
ORDER BY total_own_goals DESC
LIMIT 3