SELECT Players.Friendly_First_Name, Players.Friendly_Last_Name, SUM(money_given) as total_money_given FROM Matchday
INNER JOIN Players ON Players.ID = Matchday.Player_ID
GROUP BY Matchday.Player_Id, Players.Friendly_First_Name, Players.Friendly_Last_Name
HAVING SUM(money_given) >= 0
ORDER BY total_money_given DESC