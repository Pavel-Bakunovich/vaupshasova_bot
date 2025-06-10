SELECT Friendly_First_Name || ' ' || Friendly_Last_Name AS player_name, SUM(money_given) as total_money_given FROM Matchday
INNER JOIN Players ON Players.ID = Matchday.Player_ID
GROUP BY Matchday.Player_Id, Players.Friendly_First_Name, Players.Friendly_Last_Name
HAVING SUM(money_given) >= 0
ORDER BY total_money_given DESC
LIMIT 3