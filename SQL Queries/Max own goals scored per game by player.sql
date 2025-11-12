SELECT 
    p.id AS player_id,
    p.Friendly_First_Name,
    p.Friendly_Last_Name,
    g.Game_Date,
    m.own_goals AS max_own_goals,
    g.Score_Tomato,
    g.Score_Corn,
    m.Squad
FROM Players p
JOIN Matchday m ON p.id = m.Player_ID
JOIN Games g ON m.Game_ID = g.id
WHERE p.id = {Player_ID}
AND m.own_goals = (
    SELECT MAX(own_goals) 
    FROM Matchday m2 
    WHERE m2.Player_ID = p.id
)
ORDER BY g.Game_Date DESC;