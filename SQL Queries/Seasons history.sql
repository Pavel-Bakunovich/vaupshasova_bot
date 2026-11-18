WITH seasons AS (
    SELECT EXTRACT(YEAR FROM Game_Date)::int AS season,
        SUM(CASE WHEN Played = TRUE AND Game_Date <= current_date AND Score_Corn > Score_Tomato THEN 1 ELSE 0 END) AS corn_wins,
        SUM(CASE WHEN Played = TRUE AND Game_Date <= current_date AND Score_Tomato > Score_Corn THEN 1 ELSE 0 END) AS tomato_wins,
        SUM(CASE WHEN Played = TRUE AND Game_Date <= current_date AND Score_Tomato = Score_Corn THEN 1 ELSE 0 END) AS draws,
        SUM(CASE WHEN Played = FALSE THEN 1 ELSE 0 END) AS cancelled
    FROM Games
    WHERE Game_Date IS NOT NULL
    GROUP BY season
),
player_totals AS (
    SELECT EXTRACT(YEAR FROM Games.Game_Date)::int AS season,
        Players.Friendly_First_Name || ' ' || Players.Friendly_Last_Name AS player_name,
        COALESCE(SUM(Matchday.Goals), 0) AS goals,
        COALESCE(SUM(Matchday.Assists), 0) AS assists,
        COALESCE(SUM(Matchday.Own_Goals), 0) AS own_goals,
        COUNT(DISTINCT Matchday.Game_ID) AS games_played
    FROM Matchday
    INNER JOIN Players ON Players.id = Matchday.Player_ID
    INNER JOIN Games ON Games.id = Matchday.Game_ID
    WHERE Matchday.Type = 'add'
        AND Games.Played = TRUE
        AND Games.Game_Date <= current_date
    GROUP BY season, player_name
),
ranked AS (
    SELECT *,
        RANK() OVER (PARTITION BY season ORDER BY goals DESC) AS goals_rank,
        RANK() OVER (PARTITION BY season ORDER BY assists DESC) AS assists_rank,
        RANK() OVER (PARTITION BY season ORDER BY own_goals DESC) AS own_goals_rank,
        RANK() OVER (PARTITION BY season ORDER BY games_played DESC) AS games_rank
    FROM player_totals
),
leaders AS (
    SELECT season,
        STRING_AGG(player_name, ', ' ORDER BY player_name) FILTER (WHERE goals_rank = 1 AND goals > 0) AS top_scorers,
        MAX(goals) AS top_goals,
        STRING_AGG(player_name, ', ' ORDER BY player_name) FILTER (WHERE assists_rank = 1 AND assists > 0) AS top_assistants,
        MAX(assists) AS top_assists,
        STRING_AGG(player_name, ', ' ORDER BY player_name) FILTER (WHERE own_goals_rank = 1 AND own_goals > 0) AS top_own_goal_scorers,
        MAX(own_goals) AS top_own_goals,
        STRING_AGG(player_name, ', ' ORDER BY player_name) FILTER (WHERE games_rank = 1 AND games_played > 0) AS top_games_players,
        MAX(games_played) AS top_games
    FROM ranked
    GROUP BY season
)
SELECT seasons.season, seasons.corn_wins, seasons.tomato_wins, seasons.draws,
    leaders.top_scorers, leaders.top_goals,
    leaders.top_assistants, leaders.top_assists,
    leaders.top_own_goal_scorers, leaders.top_own_goals,
    seasons.cancelled,
    leaders.top_games_players, leaders.top_games
FROM seasons
LEFT JOIN leaders ON leaders.season = seasons.season
WHERE seasons.season <= EXTRACT(YEAR FROM current_date)
ORDER BY seasons.season DESC;
