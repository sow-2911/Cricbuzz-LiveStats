-- Question 1
-- Select the full name and playing details of players
-- from the players table who are from India.
SELECT full_name, role, batting_style, bowling_style
FROM players 
WHERE country = 'India';  -- filter: only players whose country column equals 'India'

-- Question 2
-- Select match description and related home/away team names,
-- venue name and city, and the date of the match.
SELECT m.description, 
       ht.name as home_team, 
       at.name as away_team,
       v.name as venue_name,
       v.city,
       m.date
FROM matches m
-- join to get the name of the home team using the home_team_id foreign key
JOIN teams ht ON m.home_team_id = ht.team_id
-- join to get the name of the away team using the away_team_id foreign key
JOIN teams at ON m.away_team_id = at.team_id
-- join to get the venue info for the match
JOIN venues v ON m.venue_id = v.venue_id
-- filter to only matches in the last 30 days
WHERE m.date >= DATE_SUB(CURRENT_DATE, INTERVAL 30 DAY)
-- and only include matches that are completed
AND m.status = 'completed'
-- sort the results with the most recent match first
ORDER BY m.date DESC;

-- Question 3
-- Select top ODI run-scorers: player name, runs, average, centuries.
SELECT p.full_name, 
       pa.runs as total_runs,
       pa.avg as batting_average,
       pa.hundreds as centuries
FROM player_aggregates pa
-- join to get player full name
JOIN players p ON pa.player_id = p.player_id
-- consider only ODI format aggregates
WHERE pa.format = 'ODI'
-- order by runs descending to get highest scorers
ORDER BY pa.runs DESC
-- show only top 10
LIMIT 10;

-- Question 4
-- Select name, city, country and seating capacity from venues
-- for stadiums with capacity greater than 50,000.
SELECT name, city, country, capacity
FROM venues 
WHERE capacity > 50000
-- order by capacity highest first
ORDER BY capacity DESC;

-- Question 5
-- For each team, count the number of completed matches they won.
SELECT t.name as team_name, 
       COUNT(m.winner_team_id) as wins
FROM teams t
-- left join matches on winner_team_id so teams with zero wins are included
LEFT JOIN matches m ON t.team_id = m.winner_team_id
-- only count matches that are completed
WHERE m.status = 'completed'
-- group by team to aggregate wins per team
GROUP BY t.team_id, t.name
-- order by number of wins descending
ORDER BY wins DESC;

-- Question 6
-- Count how many players belong to each playing role.
SELECT role, COUNT(*) as player_count
FROM players
-- exclude NULL roles to get meaningful counts
WHERE role IS NOT NULL
-- group by role to aggregate counts
GROUP BY role
-- order by the most common role first
ORDER BY player_count DESC;

-- Question 7
-- Find the highest individual batting score recorded in each format.
SELECT format, MAX(high_score) as highest_score
FROM player_aggregates
-- limit to these three common formats
WHERE format IN ('Test', 'ODI', 'T20')
-- group by format to get one row per format
GROUP BY format;

-- Question 8
-- Show series that started in 2024: name, host country, format, start date, planned matches.
SELECT name, host_country, format, start_date, planned_matches
FROM series
-- extract the year from start_date and keep only 2024
WHERE EXTRACT(YEAR FROM start_date) = 2024;

-- Question 9
-- Find all-rounders with >1000 runs and >50 wickets in ODI and Test.
-- First part: ODI all-rounders
SELECT p.full_name,
       SUM(CASE WHEN pa.format = 'ODI' THEN pa.runs ELSE 0 END) as total_runs,
       SUM(CASE WHEN pa.format = 'ODI' THEN pa.wickets ELSE 0 END) as total_wickets,
       'ODI' as format
FROM players p
JOIN player_aggregates pa ON p.player_id = pa.player_id
-- only consider players with role All-rounder and format ODI in this subquery
WHERE p.role = 'All-rounder'
  AND pa.format = 'ODI'
GROUP BY p.player_id, p.full_name
-- having clause filters groups after aggregation to ensure the thresholds are met
HAVING SUM(CASE WHEN pa.format = 'ODI' THEN pa.runs ELSE 0 END) > 1000
   AND SUM(CASE WHEN pa.format = 'ODI' THEN pa.wickets ELSE 0 END) > 50

UNION ALL

-- Second part: Test all-rounders (same logic, different format)
SELECT p.full_name,
       SUM(CASE WHEN pa.format = 'Test' THEN pa.runs ELSE 0 END) as total_runs,
       SUM(CASE WHEN pa.format = 'Test' THEN pa.wickets ELSE 0 END) as total_wickets,
       'Test' as format
FROM players p
JOIN player_aggregates pa ON p.player_id = pa.player_id
WHERE p.role = 'All-rounder'
  AND pa.format = 'Test'
GROUP BY p.player_id, p.full_name
HAVING SUM(CASE WHEN pa.format = 'Test' THEN pa.runs ELSE 0 END) > 1000
   AND SUM(CASE WHEN pa.format = 'Test' THEN pa.wickets ELSE 0 END) > 50;

-- Question 10
-- Get last 20 completed matches with teams, winner, margin/type and venue.
SELECT m.description,
       ht.name as home_team,
       at.name as away_team,
       wt.name as winning_team,
       m.victory_margin,
       m.victory_type,
       v.name as venue_name
FROM matches m
-- join to resolve home team name
JOIN teams ht ON m.home_team_id = ht.team_id
-- join to resolve away team name
JOIN teams at ON m.away_team_id = at.team_id
-- join to resolve winning team name
JOIN teams wt ON m.winner_team_id = wt.team_id
-- join to resolve venue name
JOIN venues v ON m.venue_id = v.venue_id
-- only completed matches
WHERE m.status = 'completed'
-- sort by most recent matches first
ORDER BY m.date DESC
-- limit to last 20 matches
LIMIT 20;

-- Question 11
-- Compare players across formats (Test, ODI, T20): runs per format and overall average.
WITH format_stats AS (
    -- gather per-player aggregates from player_aggregates
    SELECT p.player_id,
           p.full_name,
           pa.format,
           pa.runs,
           pa.avg
    FROM players p
    JOIN player_aggregates pa ON p.player_id = pa.player_id
    -- only keep formats where the player has scored runs
    WHERE pa.runs > 0
),
multi_format_players AS (
    -- find players who have played in at least 2 distinct formats
    SELECT player_id, full_name
    FROM format_stats
    GROUP BY player_id, full_name
    HAVING COUNT(DISTINCT format) >= 2
)
-- For players who played multiple formats, produce one row per player
SELECT mfp.full_name,
       -- CASE expressions pivot runs into separate columns by format
       MAX(CASE WHEN fs.format = 'Test' THEN fs.runs END) as test_runs,
       MAX(CASE WHEN fs.format = 'ODI' THEN fs.runs END) as odi_runs,
       MAX(CASE WHEN fs.format = 'T20' THEN fs.runs END) as t20_runs,
       -- overall average computed as average of the per-format averages
       ROUND(AVG(fs.avg), 2) as overall_avg
FROM multi_format_players mfp
JOIN format_stats fs ON mfp.player_id = fs.player_id
-- group by player to collapse multiple format rows into a single row per player
GROUP BY mfp.player_id, mfp.full_name;

-- Question 12
-- Count home wins vs away wins for each team by comparing venue country and team country.
SELECT t.name as team_name,
       -- count cases where venue country equals team country (home wins)
       COUNT(CASE WHEN v.country = t.country THEN m.winner_team_id END) as home_wins,
       -- count cases where venue country differs from team country (away wins)
       COUNT(CASE WHEN v.country != t.country THEN m.winner_team_id END) as away_wins
FROM teams t
-- left join to include teams even if they have zero wins
LEFT JOIN matches m ON t.team_id = m.winner_team_id
-- bring venue country info to determine home/away
LEFT JOIN venues v ON m.venue_id = v.venue_id
-- consider only completed matches
WHERE m.status = 'completed'
-- group results per team for aggregation
GROUP BY t.team_id, t.name
-- order by total wins (home + away) descending
ORDER BY (home_wins + away_wins) DESC;

-- Question 13
-- List partnerships of 100 or more runs with player names and innings number.
SELECT p1.full_name as player_a,
       p2.full_name as player_b,
       p.runs as partnership_runs,
       i.innings_no
FROM partnerships p
-- join to resolve first batsman name
JOIN players p1 ON p.player_a = p1.player_id
-- join to resolve second batsman name
JOIN players p2 ON p.player_b = p2.player_id
-- join to get innings_no (which innings the partnership occurred in)
JOIN innings i ON p.innings_id = i.innings_id
-- filter only partnerships worth 100 runs or more
WHERE p.runs >= 100
-- show biggest partnerships first
ORDER BY p.runs DESC;

-- Question 14
-- Bowler performance per venue: matches played, average economy and total wickets.
SELECT 
    p.full_name,
    v.name as venue_name,
    v.city,
    v.country,
    -- count distinct matches the bowler played at the venue
    COUNT(DISTINCT m.match_id) as matches_played,
    -- average economy for the bowler at the venue
    ROUND(AVG(b.economy), 2) as avg_economy,
    -- total wickets taken by the bowler at the venue
    SUM(b.wickets) as total_wickets
FROM bowling b
-- join to find which innings the bowling record belongs to
JOIN innings i ON b.innings_id = i.innings_id
-- join to find the match for that innings
JOIN matches m ON i.match_id = m.match_id
-- join to get the venue of the match
JOIN venues v ON m.venue_id = v.venue_id
-- join to get player full name
JOIN players p ON b.player_id = p.player_id
-- only consider bowling spells where the bowler bowled at least 4 overs
WHERE b.overs >= 4
-- group by player and venue so we compute per-player-per-venue stats
GROUP BY p.player_id, p.full_name, v.venue_id, v.name, v.city, v.country
-- only include bowlers who appeared in at least 3 matches at this venue
HAVING COUNT(DISTINCT m.match_id) >= 3
-- order by best economy (lowest first)
ORDER BY avg_economy ASC;

-- Question 15
-- Identify performers in close matches: average runs, matches played and wins when batting.
WITH close_matches AS (
    -- select match ids for completed matches decided by small margins
    SELECT match_id
    FROM matches
    WHERE status = 'completed'
    AND (
        (victory_type = 'runs' AND victory_margin < 50) 
        OR (victory_type = 'wickets' AND victory_margin < 5)
    )
),
player_batting_in_close_matches AS (
    -- for each batting record in those close matches, capture player runs and whether batting team won
    SELECT 
        b.player_id,
        i.match_id,
        b.runs,
        -- team_won_when_batted = 1 if batting team equals winner_team_id, else 0
        CASE WHEN m.winner_team_id = i.batting_team_id THEN 1 ELSE 0 END as team_won_when_batted,
        t.team_id as batting_team_id
    FROM batting b
    JOIN innings i ON b.innings_id = i.innings_id
    JOIN matches m ON i.match_id = m.match_id
    JOIN teams t ON i.batting_team_id = t.team_id
    -- only keep records that belong to close matches
    WHERE m.match_id IN (SELECT match_id FROM close_matches)
),
player_stats AS (
    -- aggregate per player: total close matches, average runs, matches won when batting, win percentage
    SELECT 
        p.player_id,
        p.full_name,
        COUNT(DISTINCT pbc.match_id) as total_close_matches_played,
        ROUND(AVG(pbc.runs), 2) as avg_runs_in_close_matches,
        SUM(pbc.team_won_when_batted) as close_matches_won_when_batted,
        -- win percentage when batted = wins_when_batted / total_close_matches * 100
        ROUND(SUM(pbc.team_won_when_batted) * 100.0 / COUNT(DISTINCT pbc.match_id), 2) as win_percentage_when_batted
    FROM player_batting_in_close_matches pbc
    JOIN players p ON pbc.player_id = p.player_id
    GROUP BY p.player_id, p.full_name
    -- include only players who played at least 2 close matches (adjustable threshold)
    HAVING COUNT(DISTINCT pbc.match_id) >= 2
)
-- final selection with a performance category assigned based on thresholds
SELECT 
    full_name,
    total_close_matches_played,
    avg_runs_in_close_matches,
    close_matches_won_when_batted,
    win_percentage_when_batted,
    CASE 
        WHEN avg_runs_in_close_matches >= 50 AND win_percentage_when_batted >= 60 THEN 'Exceptional Performer'
        WHEN avg_runs_in_close_matches >= 35 AND win_percentage_when_batted >= 50 THEN 'Strong Performer'
        WHEN avg_runs_in_close_matches >= 25 THEN 'Good Performer'
        ELSE 'Average Performer'
    END as performance_category
FROM player_stats
-- order by average runs then win percentage to surface best clutch performers
ORDER BY avg_runs_in_close_matches DESC, win_percentage_when_batted DESC;

-- Question 16
-- Compute per-player yearly stats (matches played, average runs) since 2020.
WITH yearly_stats AS (
    SELECT p.player_id,
           EXTRACT(YEAR FROM m.date) as year,
           COUNT(DISTINCT m.match_id) as matches_played,
           AVG(b.runs) as avg_runs
    FROM batting b
    JOIN innings i ON b.innings_id = i.innings_id
    JOIN matches m ON i.match_id = m.match_id
    JOIN players p ON b.player_id = p.player_id
    -- consider matches from 2020-01-01 onwards
    WHERE m.date >= '2020-01-01'
    GROUP BY p.player_id, EXTRACT(YEAR FROM m.date)
    -- optionally ensure a minimum number of matches per year (not present here)
)
SELECT p.full_name,
       ys.year,
       ys.matches_played,
       ROUND(ys.avg_runs, 2) as avg_runs_per_match
FROM yearly_stats ys
JOIN players p ON ys.player_id = p.player_id
-- order by player name and year for readability
ORDER BY p.full_name, ys.year;

-- Question 17
-- Analyze the effect of toss decision: whether teams that chose to bat or bowl won more often.
SELECT toss_decision,
       COUNT(*) as total_matches,
       -- wins_after_toss counts matches where toss winner also became match winner
       COUNT(CASE WHEN winner_team_id = toss_winner_id THEN 1 END) as wins_after_toss,
       -- win percentage after toss winner chooses that decision
       ROUND(COUNT(CASE WHEN winner_team_id = toss_winner_id THEN 1 END) * 100.0 / COUNT(*), 2) as win_percentage
FROM matches
-- only completed matches and where toss decision is recorded
WHERE status = 'completed'
  AND toss_decision IS NOT NULL
GROUP BY toss_decision;  -- group by the toss decision (e.g., bat or bowl)

-- Question 18
-- List bowlers (ODI/T20) with decent match counts and non-zero wickets, showing economy and wickets.
SELECT p.full_name,
       pa.format,
       pa.matches as total_matches,
       ROUND(pa.economy, 2) as economy_rate,
       pa.wickets as total_wickets,
       pa.bowling_avg
FROM player_aggregates pa
JOIN players p ON pa.player_id = p.player_id
-- focus on limited over formats and experienced bowlers
WHERE pa.format IN ('ODI', 'T20')
  AND pa.matches >= 10
  AND pa.wickets > 0
-- order by economy ascending to show the most economical bowlers first
ORDER BY pa.economy ASC;

-- Question 19
-- Player consistency: average runs, standard deviation and a consistency ratio since 2022 for innings with >= 10 balls.
WITH player_consistency AS (
    SELECT p.player_id,
           p.full_name,
           AVG(b.runs) as avg_runs,
           STDDEV(b.runs) as std_dev_runs,
           COUNT(*) as innings_played
    FROM batting b
    JOIN innings i ON b.innings_id = i.innings_id
    JOIN matches m ON i.match_id = m.match_id
    JOIN players p ON b.player_id = p.player_id
    -- consider recent time window and meaningful innings only
    WHERE m.date >= '2022-01-01'
      AND b.balls >= 10
    GROUP BY p.player_id, p.full_name
    -- require at least 5 innings to compute a stable metric
    HAVING COUNT(*) >= 5
)
SELECT full_name,
       ROUND(avg_runs, 2) as average_runs,
       ROUND(std_dev_runs, 2) as standard_deviation,
       innings_played,
       -- consistency ratio: std_dev / avg, NULL-safe
       ROUND(std_dev_runs / NULLIF(avg_runs, 0), 2) as consistency_ratio
FROM player_consistency
-- sort by lowest standard deviation first (most consistent)
ORDER BY std_dev_runs ASC;

-- Question 20
-- Show player involvement counts and per-format averages mapped from series -> matches -> batting -> player aggregates.
SELECT p.full_name,
       COUNT(DISTINCT CASE WHEN s.format = 'Test' THEN m.match_id END) as test_matches,
       MAX(CASE WHEN pa.format = 'Test' THEN pa.avg END) as test_avg,
       COUNT(DISTINCT CASE WHEN s.format = 'ODI' THEN m.match_id END) as odi_matches,
       MAX(CASE WHEN pa.format = 'ODI' THEN pa.avg END) as odi_avg,
       COUNT(DISTINCT CASE WHEN s.format = 'T20' THEN m.match_id END) as t20_matches,
       MAX(CASE WHEN pa.format = 'T20' THEN pa.avg END) as t20_avg,
       COUNT(DISTINCT m.match_id) as total_matches
FROM players p
JOIN batting b ON p.player_id = b.player_id
JOIN innings i ON b.innings_id = i.innings_id
JOIN matches m ON i.match_id = m.match_id
JOIN series s ON m.series_id = s.series_id
-- left join to bring in per-format career aggregates if available
LEFT JOIN player_aggregates pa ON p.player_id = pa.player_id AND pa.format = s.format
GROUP BY p.player_id, p.full_name
-- require a minimum number of distinct matches to keep stats relevant
HAVING COUNT(DISTINCT m.match_id) >= 15
-- order by most total matches played
ORDER BY total_matches DESC;

-- Question 21
-- Compute a combined performance score per player using weighted batting, bowling and fielding metrics.
WITH performance_scores AS (
    SELECT p.player_id,
           p.full_name,
           pa.format,
           -- batting points combine runs, avg and strike rate with weights
           (pa.runs * 0.01) + 
           (COALESCE(pa.avg, 0) * 0.5) + 
           (COALESCE(pa.strike_rate, 0) * 0.3) as batting_points,
           -- bowling points use wickets, bowling average and economy with weights
           (COALESCE(pa.wickets, 0) * 2) + 
           ((50 - COALESCE(pa.bowling_avg, 50)) * 0.5) + 
           ((6 - COALESCE(pa.economy, 6)) * 2) as bowling_points,
           -- fielding points from catches and stumpings
           (COALESCE(pa.catches, 0) * 0.5) + 
           (COALESCE(pa.stumpings, 0) * 1) as fielding_points,
           pa.runs,
           pa.avg,
           pa.strike_rate,
           pa.wickets,
           pa.bowling_avg,
           pa.economy
    FROM player_aggregates pa
    JOIN players p ON pa.player_id = p.player_id
    -- only include players with enough matches to be meaningful
    WHERE pa.matches >= 10
)
SELECT full_name,
       format,
       -- total score = batting + bowling + fielding points
       ROUND(batting_points + bowling_points + fielding_points, 2) as total_score,
       ROUND(batting_points, 2) as batting_score,
       ROUND(bowling_points, 2) as bowling_score,
       ROUND(fielding_points, 2) as fielding_score,
       runs,
       avg as batting_avg,
       strike_rate,
       wickets
FROM performance_scores
-- show highest scoring players per format first
ORDER BY format, total_score DESC;

-- Question 22
-- Head-to-head summary for team pairs: total matches and wins per side, using LEAST/GREATEST to canonicalize pair ordering.
WITH head_to_head AS (
    SELECT 
        -- canonicalize team pair so team1_id < team2_id for consistent grouping
        LEAST(m.home_team_id, m.away_team_id) AS team1_id,
        GREATEST(m.home_team_id, m.away_team_id) AS team2_id,
        t1.name AS team1_name,
        t2.name AS team2_name,
        COUNT(*) AS total_matches,
        -- count wins for team1 by comparing winner_team_id to canonical team1 id
        COUNT(CASE WHEN m.winner_team_id = LEAST(m.home_team_id, m.away_team_id) THEN 1 END) AS team1_wins,
        -- count wins for team2 similarly
        COUNT(CASE WHEN m.winner_team_id = GREATEST(m.home_team_id, m.away_team_id) THEN 1 END) AS team2_wins,
        -- average margin when team1 won (NULL if never)
        AVG(CASE WHEN m.winner_team_id = LEAST(m.home_team_id, m.away_team_id) THEN m.victory_margin END) AS team1_avg_margin,
        -- average margin when team2 won
        AVG(CASE WHEN m.winner_team_id = GREATEST(m.home_team_id, m.away_team_id) THEN m.victory_margin END) AS team2_avg_margin
    FROM matches m
    JOIN teams t1 ON LEAST(m.home_team_id, m.away_team_id) = t1.team_id
    JOIN teams t2 ON GREATEST(m.home_team_id, m.away_team_id) = t2.team_id
    -- only completed matches to ensure valid results
    WHERE m.status = 'completed'
      AND m.date >= CURRENT_DATE - INTERVAL 3 YEAR  -- limit to recent 3 years
    GROUP BY 
        LEAST(m.home_team_id, m.away_team_id), 
        GREATEST(m.home_team_id, m.away_team_id), 
        t1.name, t2.name
    -- keep only pairs with at least 5 matches for meaningful stats
    HAVING COUNT(*) >= 5
)
SELECT 
    team1_name,
    team2_name,
    total_matches,
    team1_wins,
    team2_wins,
    ROUND(team1_avg_margin, 1) AS team1_avg_victory_margin,
    ROUND(team2_avg_margin, 1) AS team2_avg_victory_margin,
    ROUND(team1_wins * 100.0 / total_matches, 1) AS team1_win_percentage,
    ROUND(team2_wins * 100.0 / total_matches, 1) AS team2_win_percentage
FROM head_to_head
-- show pairs with the most encounters first
ORDER BY total_matches DESC;

-- Question 23
-- Recent form: compute average of last 5 matches for each player using window functions.
WITH recent_matches AS (
    SELECT b.player_id,
           m.date,
           b.runs,
           b.strike_rate,
           -- assign a rank per player ordered by date descending (most recent = 1)
           ROW_NUMBER() OVER (PARTITION BY b.player_id ORDER BY m.date DESC) as match_rank
    FROM batting b
    JOIN innings i ON b.innings_id = i.innings_id
    JOIN matches m ON i.match_id = m.match_id
),
player_stats AS (
    -- average runs over last 5 matches (we will use match_rank <= 5)
    SELECT player_id,
           AVG(CASE WHEN match_rank <= 5 THEN runs END) as avg_last_5,
           AVG(CASE WHEN match_rank <= 10 THEN runs END) as avg_last_10,
           AVG(CASE WHEN match_rank <= 10 THEN strike_rate END) as avg_sr_last_10,
           COUNT(CASE WHEN match_rank <= 10 AND runs >= 50 THEN 1 END) as scores_above_50,
           STDDEV(CASE WHEN match_rank <= 10 THEN runs END) as consistency_std
    FROM recent_matches
    WHERE match_rank <= 10
    GROUP BY player_id
    HAVING COUNT(*) >= 5  -- ensure at least 5 recent matches to compute metrics
)
SELECT p.full_name,
       ROUND(ps.avg_last_5, 2) as avg_last_5_matches,
       ROUND(ps.avg_last_10, 2) as avg_last_10_matches,
       ROUND(ps.avg_sr_last_10, 2) as avg_strike_rate,
       ps.scores_above_50,
       ROUND(ps.consistency_std, 2) as consistency_score,
       CASE 
           WHEN ps.avg_last_5 > 45 AND ps.scores_above_50 >= 3 THEN 'Excellent Form'
           WHEN ps.avg_last_5 > 35 AND ps.scores_above_50 >= 2 THEN 'Good Form'
           WHEN ps.avg_last_5 > 25 THEN 'Average Form'
           ELSE 'Poor Form'
       END as form_category
FROM player_stats ps
JOIN players p ON ps.player_id = p.player_id
-- sort by the best recent average first
ORDER BY ps.avg_last_5 DESC;

-- Question 24
-- Partnership statistics: average partnership, highest partnership and counts per pair.
WITH partnership_stats AS (
    SELECT p.player_a,
           p.player_b,
           COUNT(*) as total_partnerships,
           AVG(p.runs) as avg_partnership,
           MAX(p.runs) as highest_partnership,
           COUNT(CASE WHEN p.runs >= 50 THEN 1 END) as partnerships_50_plus,
           -- success rate of 50+ partnerships as a percentage
           ROUND(COUNT(CASE WHEN p.runs >= 50 THEN 1 END) * 100.0 / COUNT(*), 2) as success_rate
    FROM partnerships p
    GROUP BY p.player_a, p.player_b
    HAVING COUNT(*) >= 5  -- include only pairs with at least 5 partnerships
)
SELECT p1.full_name as player_a,
       p2.full_name as player_b,
       ps.total_partnerships,
       ROUND(ps.avg_partnership, 2) as avg_runs,
       ps.highest_partnership,
       ps.partnerships_50_plus,
       ps.success_rate
FROM partnership_stats ps
-- join to get player names for IDs
JOIN players p1 ON ps.player_a = p1.player_id
JOIN players p2 ON ps.player_b = p2.player_id
-- order by highest success rate and average partnership
ORDER BY ps.success_rate DESC, ps.avg_partnership DESC;

-- Question 25
-- Quarterly time-series: aggregate player performance per quarter and compute trends.
WITH quarterly_stats_raw AS (
    -- aggregate per player per quarter: number of matches, average runs and strike rate
    SELECT 
        p.player_id,
        YEAR(m.date) AS yr,
        QUARTER(m.date) AS qtr,
        COUNT(DISTINCT m.match_id) AS matches_played,
        AVG(b.runs) AS avg_runs,
        AVG(b.strike_rate) AS avg_sr
    FROM batting b
    JOIN innings i ON b.innings_id = i.innings_id
    JOIN matches m ON i.match_id = m.match_id
    JOIN players p ON b.player_id = p.player_id
    WHERE m.status = 'completed'
    GROUP BY p.player_id, YEAR(m.date), QUARTER(m.date)
    HAVING COUNT(DISTINCT m.match_id) >= 3  -- require minimum matches per quarter
),
qualified_players AS (
    -- keep only players who appear in at least 6 quarters
    SELECT player_id
    FROM quarterly_stats_raw
    GROUP BY player_id
    HAVING COUNT(*) >= 6
),
quarterly_stats AS (
    -- add quarter label and numeric index to help compute trends
    SELECT 
        qs.player_id,
        CONCAT(qs.yr, '-Q', qs.qtr) AS quarter_label,
        (qs.yr * 4 + qs.qtr) AS quarter_index,
        qs.avg_runs,
        qs.avg_sr
    FROM quarterly_stats_raw qs
    JOIN qualified_players qp ON qs.player_id = qp.player_id
),
quarterly_comparison AS (
    -- compare each quarter with the previous quarter using LAG
    SELECT 
        player_id,
        quarter_label,
        quarter_index,
        avg_runs,
        avg_sr,
        LAG(avg_runs) OVER (PARTITION BY player_id ORDER BY quarter_index) AS prev_avg_runs,
        LAG(avg_sr) OVER (PARTITION BY player_id ORDER BY quarter_index) AS prev_avg_sr
    FROM quarterly_stats
),
career_trajectory_avg AS (
    -- precompute averages per player needed for slope calculation
    SELECT 
        player_id,
        AVG(quarter_index) AS avg_q_index,
        AVG(avg_runs) AS avg_runs_avg,
        AVG(avg_sr) AS avg_sr_avg
    FROM quarterly_stats
    GROUP BY player_id
),
career_trajectory AS (
    -- compute linear trend (slope) for average runs and strike rate across quarters
    SELECT 
        q.player_id,
        SUM((q.quarter_index - c.avg_q_index) * (q.avg_runs - c.avg_runs_avg)) / SUM(POW(q.quarter_index - c.avg_q_index, 2)) AS runs_trend,
        SUM((q.quarter_index - c.avg_q_index) * (q.avg_sr - c.avg_sr_avg)) / SUM(POW(q.quarter_index - c.avg_q_index, 2)) AS sr_trend
    FROM quarterly_stats q
    JOIN career_trajectory_avg c ON q.player_id = c.player_id
    GROUP BY q.player_id
)
-- Final output: per-quarter changes plus career trend classification
SELECT 
    p.full_name,
    qc.quarter_label,
    ROUND(qc.avg_runs, 2) AS quarterly_avg_runs,
    ROUND(qc.avg_sr, 2) AS quarterly_avg_sr,
    ROUND(qc.avg_runs - qc.prev_avg_runs, 2) AS runs_change,
    ROUND(qc.avg_sr - qc.prev_avg_sr, 2) AS sr_change,
    CASE
        WHEN (qc.avg_runs - qc.prev_avg_runs) > 10 AND (qc.avg_sr - qc.prev_avg_sr) > 5 THEN 'Improving'
        WHEN (qc.avg_runs - qc.prev_avg_runs) < -10 AND (qc.avg_sr - qc.prev_avg_sr) < -5 THEN 'Declining'
        ELSE 'Stable'
    END AS performance_trend,
    CASE
        WHEN ct.runs_trend > 0.3 AND ct.sr_trend > 0.2 THEN 'Career Ascending'
        WHEN ct.runs_trend < -0.3 AND ct.sr_trend < -0.2 THEN 'Career Declining'
        ELSE 'Career Stable'
    END AS career_phase
FROM quarterly_comparison qc
JOIN career_trajectory ct ON qc.player_id = ct.player_id
JOIN players p ON qc.player_id = p.player_id
-- only include quarter rows which have a previous quarter to compare against
WHERE qc.prev_avg_runs IS NOT NULL
-- order by player name and quarter for a readable timeline
ORDER BY p.full_name, qc.quarter_label;
