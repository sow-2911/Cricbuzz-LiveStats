import streamlit as st
from utils.db_connection import get_db_session
from sqlalchemy import text
import pandas as pd
import io

def run_query(sql, params=None):
    with get_db_session() as session:
        result = session.execute(text(sql), params or {})
        cols = result.keys()
        rows = result.fetchall()
    return pd.DataFrame(rows, columns=cols)

def show():
    # Define all questions and queries in a structured list
    sql_questions = [
        {
            "question": "1. Find all players who represent India",
            "query": "SELECT full_name, role, batting_style, bowling_style FROM players WHERE country = 'India';"
        },
        {
            "question": "2. Show recent matches from last 30 days",
            "query": """
                SELECT m.description, 
                       ht.name as home_team, 
                       at.name as away_team,
                       v.name as venue_name,
                       v.city,
                       m.date
                FROM matches m
                JOIN teams ht ON m.home_team_id = ht.team_id
                JOIN teams at ON m.away_team_id = at.team_id
                JOIN venues v ON m.venue_id = v.venue_id
                WHERE m.date >= DATE_SUB(CURRENT_DATE, INTERVAL 30 DAY)
                AND m.status = 'completed'
                ORDER BY m.date DESC;
            """
        },
        {
            "question": "3. Top 10 highest run scorers in ODI cricket",
            "query": """
                SELECT p.full_name, 
                       pa.runs as total_runs,
                       pa.avg as batting_average,
                       pa.hundreds as centuries
                FROM player_aggregates pa
                JOIN players p ON pa.player_id = p.player_id
                WHERE pa.format = 'ODI'
                ORDER BY pa.runs DESC
                LIMIT 10;
            """
        },
        {
            "question": "4. Large capacity venues (50,000+ spectators)",
            "query": "SELECT name, city, country, capacity FROM venues WHERE capacity > 50000 ORDER BY capacity DESC;"
        },
        {
            "question": "5. Team win counts",
            "query": """
                SELECT t.name as team_name, 
                       COUNT(m.winner_team_id) as wins
                FROM teams t
                LEFT JOIN matches m ON t.team_id = m.winner_team_id
                WHERE m.status = 'completed'
                GROUP BY t.team_id, t.name
                ORDER BY wins DESC;
            """
        },
        {
            "question": "6. Player count by role",
            "query": "SELECT role, COUNT(*) as player_count FROM players WHERE role IS NOT NULL GROUP BY role ORDER BY player_count DESC;"
        },
        {
            "question": "7. Highest individual scores by format",
            "query": "SELECT format, MAX(high_score) as highest_score FROM player_aggregates WHERE format IN ('Test', 'ODI', 'T20') GROUP BY format;"
        },
        {
            "question": "8. Series starting in 2024",
            "query": "SELECT name, host_country, format, start_date, planned_matches FROM series WHERE EXTRACT(YEAR FROM start_date) = 2024;"
        },
        {
            "question": "9. All-rounders with 1000+ runs and 50+ wickets",
            "query": """
                SELECT p.full_name,
                       SUM(CASE WHEN pa.format = 'ODI' THEN pa.runs ELSE 0 END) as total_runs,
                       SUM(CASE WHEN pa.format = 'ODI' THEN pa.wickets ELSE 0 END) as total_wickets,
                       'ODI' as format
                FROM players p
                JOIN player_aggregates pa ON p.player_id = pa.player_id
                WHERE p.role = 'All-rounder'
                  AND pa.format = 'ODI'
                GROUP BY p.player_id, p.full_name
                HAVING SUM(CASE WHEN pa.format = 'ODI' THEN pa.runs ELSE 0 END) > 1000
                   AND SUM(CASE WHEN pa.format = 'ODI' THEN pa.wickets ELSE 0 END) > 50
                UNION ALL
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
            """
        },
        {
            "question": "10. Last 20 completed matches",
            "query": """
                SELECT m.description,
                       ht.name as home_team,
                       at.name as away_team,
                       wt.name as winning_team,
                       m.victory_margin,
                       m.victory_type,
                       v.name as venue_name
                FROM matches m
                JOIN teams ht ON m.home_team_id = ht.team_id
                JOIN teams at ON m.away_team_id = at.team_id
                JOIN teams wt ON m.winner_team_id = wt.team_id
                JOIN venues v ON m.venue_id = v.venue_id
                WHERE m.status = 'completed'
                ORDER BY m.date DESC
                LIMIT 20;
            """
        },
        {
            "question": "11. Player performance across formats",
            "query": """
                WITH format_stats AS (
                    SELECT p.player_id,
                           p.full_name,
                           pa.format,
                           pa.runs,
                           pa.avg
                    FROM players p
                    JOIN player_aggregates pa ON p.player_id = pa.player_id
                    WHERE pa.runs > 0
                ),
                multi_format_players AS (
                    SELECT player_id, full_name
                    FROM format_stats
                    GROUP BY player_id, full_name
                    HAVING COUNT(DISTINCT format) >= 2
                )
                SELECT mfp.full_name,
                       MAX(CASE WHEN fs.format = 'Test' THEN fs.runs END) as test_runs,
                       MAX(CASE WHEN fs.format = 'ODI' THEN fs.runs END) as odi_runs,
                       MAX(CASE WHEN fs.format = 'T20' THEN fs.runs END) as t20_runs,
                       ROUND(AVG(fs.avg), 2) as overall_avg
                FROM multi_format_players mfp
                JOIN format_stats fs ON mfp.player_id = fs.player_id
                GROUP BY mfp.player_id, mfp.full_name;
            """
        },
        {
            "question": "12. Team performance home vs away",
            "query": """
                SELECT t.name as team_name,
                       COUNT(CASE WHEN v.country = t.country THEN m.winner_team_id END) as home_wins,
                       COUNT(CASE WHEN v.country != t.country THEN m.winner_team_id END) as away_wins
                FROM teams t
                LEFT JOIN matches m ON t.team_id = m.winner_team_id
                LEFT JOIN venues v ON m.venue_id = v.venue_id
                WHERE m.status = 'completed'
                GROUP BY t.team_id, t.name
                ORDER BY (home_wins + away_wins) DESC;
            """
        },
        {
            "question": "13. 100+ run partnerships",
            "query": """
                SELECT p1.full_name as player_a,
                       p2.full_name as player_b,
                       p.runs as partnership_runs,
                       i.innings_no
                FROM partnerships p
                JOIN players p1 ON p.player_a = p1.player_id
                JOIN players p2 ON p.player_b = p2.player_id
                JOIN innings i ON p.innings_id = i.innings_id
                WHERE p.runs >= 100
                ORDER BY p.runs DESC;
            """
        },
        {
            "question": "14. Bowling performance by venue",
            "query": """
                SELECT 
                    p.full_name,
                    v.name as venue_name,
                    v.city,
                    v.country,
                    COUNT(DISTINCT m.match_id) as matches_played,
                    ROUND(AVG(b.economy), 2) as avg_economy,
                    SUM(b.wickets) as total_wickets,
                    ROUND(AVG(b.overs), 2) as avg_overs_per_match,
                    ROUND(AVG(b.maidens), 2) as avg_maidens_per_match
                FROM bowling b
                JOIN innings i ON b.innings_id = i.innings_id
                JOIN matches m ON i.match_id = m.match_id
                JOIN venues v ON m.venue_id = v.venue_id
                JOIN players p ON b.player_id = p.player_id
                WHERE b.overs >= 4
                GROUP BY p.player_id, p.full_name, v.venue_id, v.name, v.city, v.country
                HAVING COUNT(DISTINCT m.match_id) >= 3
                ORDER BY avg_economy ASC;
            """
        },
        {
            "question": "15. Player performance in close matches",
            "query": """
                WITH close_matches AS (
                    SELECT match_id
                    FROM matches
                    WHERE status = 'completed'
                    AND (
                        (victory_type = 'runs' AND victory_margin < 50) 
                        OR (victory_type = 'wickets' AND victory_margin < 5)
                    )
                ),
                player_batting_in_close_matches AS (
                    SELECT 
                        b.player_id,
                        i.match_id,
                        b.runs,
                        CASE WHEN m.winner_team_id = i.batting_team_id THEN 1 ELSE 0 END as team_won_when_batted,
                        t.team_id as batting_team_id
                    FROM batting b
                    JOIN innings i ON b.innings_id = i.innings_id
                    JOIN matches m ON i.match_id = m.match_id
                    JOIN teams t ON i.batting_team_id = t.team_id
                    WHERE m.match_id IN (SELECT match_id FROM close_matches)
                ),
                player_stats AS (
                    SELECT 
                        p.player_id,
                        p.full_name,
                        COUNT(DISTINCT pbc.match_id) as total_close_matches_played,
                        ROUND(AVG(pbc.runs), 2) as avg_runs_in_close_matches,
                        SUM(pbc.team_won_when_batted) as close_matches_won_when_batted,
                        ROUND(SUM(pbc.team_won_when_batted) * 100.0 / COUNT(DISTINCT pbc.match_id), 2) as win_percentage_when_batted
                    FROM player_batting_in_close_matches pbc
                    JOIN players p ON pbc.player_id = p.player_id
                    GROUP BY p.player_id, p.full_name
                    HAVING COUNT(DISTINCT pbc.match_id) >= 2
                )
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
                ORDER BY avg_runs_in_close_matches DESC, win_percentage_when_batted DESC;
            """
        },
        {
            "question": "16. Yearly batting performance trends",
            "query": """
                WITH yearly_stats AS (
                    SELECT p.player_id,
                           EXTRACT(YEAR FROM m.date) as year,
                           COUNT(DISTINCT m.match_id) as matches_played,
                           AVG(b.runs) as avg_runs,
                           AVG(b.strike_rate) as avg_strike_rate
                    FROM batting b
                    JOIN innings i ON b.innings_id = i.innings_id
                    JOIN matches m ON i.match_id = m.match_id
                    JOIN players p ON b.player_id = p.player_id
                    WHERE m.date >= '2020-01-01'
                    GROUP BY p.player_id, EXTRACT(YEAR FROM m.date)
                    HAVING COUNT(DISTINCT m.match_id) >= 5
                )
                SELECT p.full_name,
                       ys.year,
                       ys.matches_played,
                       ROUND(ys.avg_runs, 2) as avg_runs_per_match,
                       ROUND(ys.avg_strike_rate, 2) as avg_strike_rate
                FROM yearly_stats ys
                JOIN players p ON ys.player_id = p.player_id
                ORDER BY p.full_name, ys.year;
            """
        },
        {
            "question": "17. Toss advantage analysis",
            "query": """
                SELECT toss_decision,
                       COUNT(*) as total_matches,
                       COUNT(CASE WHEN winner_team_id = toss_winner_id THEN 1 END) as wins_after_toss,
                       ROUND(COUNT(CASE WHEN winner_team_id = toss_winner_id THEN 1 END) * 100.0 / COUNT(*), 2) as win_percentage
                FROM matches
                WHERE status = 'completed'
                  AND toss_decision IS NOT NULL
                GROUP BY toss_decision;
            """
        },
        {
            "question": "18. Most economical bowlers in limited-overs",
            "query": """
                SELECT p.full_name,
                       pa.format,
                       pa.matches as total_matches,
                       ROUND(pa.economy, 2) as economy_rate,
                       pa.wickets as total_wickets,
                       pa.bowling_avg
                FROM player_aggregates pa
                JOIN players p ON pa.player_id = p.player_id
                WHERE pa.format IN ('ODI', 'T20')
                  AND pa.matches >= 10
                  AND pa.wickets > 0
                ORDER BY pa.economy ASC;
            """
        },
        {
            "question": "19. Batting consistency analysis",
            "query": """
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
                    WHERE m.date >= '2022-01-01'
                      AND b.balls >= 10
                    GROUP BY p.player_id, p.full_name
                    HAVING COUNT(*) >= 5
                )
                SELECT full_name,
                       ROUND(avg_runs, 2) as average_runs,
                       ROUND(std_dev_runs, 2) as standard_deviation,
                       innings_played,
                       ROUND(std_dev_runs / NULLIF(avg_runs, 0), 2) as consistency_ratio
                FROM player_consistency
                ORDER BY std_dev_runs ASC;
            """
        },
        {
            "question": "20. Player matches and averages by format",
            "query": """
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
                LEFT JOIN player_aggregates pa ON p.player_id = pa.player_id AND pa.format = s.format
                GROUP BY p.player_id, p.full_name
                HAVING COUNT(DISTINCT m.match_id) >= 15
                ORDER BY total_matches DESC;
            """
        },
        {
            "question": "21. Comprehensive player performance ranking",
            "query": """
                WITH performance_scores AS (
                    SELECT p.player_id,
                           p.full_name,
                           pa.format,
                           (pa.runs * 0.01) + 
                           (COALESCE(pa.avg, 0) * 0.5) + 
                           (COALESCE(pa.strike_rate, 0) * 0.3) as batting_points,
                           (COALESCE(pa.wickets, 0) * 2) + 
                           ((50 - COALESCE(pa.bowling_avg, 50)) * 0.5) + 
                           ((6 - COALESCE(pa.economy, 6)) * 2) as bowling_points,
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
                    WHERE pa.matches >= 10
                )
                SELECT full_name,
                       format,
                       ROUND(batting_points + bowling_points + fielding_points, 2) as total_score,
                       ROUND(batting_points, 2) as batting_score,
                       ROUND(bowling_points, 2) as bowling_score,
                       ROUND(fielding_points, 2) as fielding_score,
                       runs,
                       avg as batting_avg,
                       strike_rate,
                       wickets
                FROM performance_scores
                ORDER BY format, total_score DESC;
            """
        },
        {
            "question": "22. Head-to-head team analysis",
            "query": """
                WITH head_to_head AS (
                    SELECT 
                        LEAST(m.home_team_id, m.away_team_id) AS team1_id,
                        GREATEST(m.home_team_id, m.away_team_id) AS team2_id,
                        t1.name AS team1_name,
                        t2.name AS team2_name,
                        COUNT(*) AS total_matches,
                        COUNT(CASE WHEN m.winner_team_id = LEAST(m.home_team_id, m.away_team_id) THEN 1 END) AS team1_wins,
                        COUNT(CASE WHEN m.winner_team_id = GREATEST(m.home_team_id, m.away_team_id) THEN 1 END) AS team2_wins,
                        AVG(CASE WHEN m.winner_team_id = LEAST(m.home_team_id, m.away_team_id) THEN m.victory_margin END) AS team1_avg_margin,
                        AVG(CASE WHEN m.winner_team_id = GREATEST(m.home_team_id, m.away_team_id) THEN m.victory_margin END) AS team2_avg_margin
                    FROM matches m
                    JOIN teams t1 ON LEAST(m.home_team_id, m.away_team_id) = t1.team_id
                    JOIN teams t2 ON GREATEST(m.home_team_id, m.away_team_id) = t2.team_id
                    WHERE m.status = 'completed'
                      AND m.date >= CURRENT_DATE - INTERVAL 3 YEAR
                    GROUP BY 
                        LEAST(m.home_team_id, m.away_team_id), 
                        GREATEST(m.home_team_id, m.away_team_id), 
                        t1.name, t2.name
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
                ORDER BY total_matches DESC;
            """
        },
        {
            "question": "23. Recent player form analysis",
            "query": """
                WITH recent_matches AS (
                    SELECT b.player_id,
                           m.date,
                           b.runs,
                           b.strike_rate,
                           ROW_NUMBER() OVER (PARTITION BY b.player_id ORDER BY m.date DESC) as match_rank
                    FROM batting b
                    JOIN innings i ON b.innings_id = i.innings_id
                    JOIN matches m ON i.match_id = m.match_id
                ),
                player_stats AS (
                    SELECT player_id,
                           AVG(CASE WHEN match_rank <= 5 THEN runs END) as avg_last_5,
                           AVG(CASE WHEN match_rank <= 10 THEN runs END) as avg_last_10,
                           AVG(CASE WHEN match_rank <= 10 THEN strike_rate END) as avg_sr_last_10,
                           COUNT(CASE WHEN match_rank <= 10 AND runs >= 50 THEN 1 END) as scores_above_50,
                           STDDEV(CASE WHEN match_rank <= 10 THEN runs END) as consistency_std
                    FROM recent_matches
                    WHERE match_rank <= 10
                    GROUP BY player_id
                    HAVING COUNT(*) >= 5
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
                ORDER BY ps.avg_last_5 DESC;
            """
        },
        {
            "question": "24. Successful batting partnerships",
            "query": """
                WITH partnership_stats AS (
                    SELECT p.player_a,
                           p.player_b,
                           COUNT(*) as total_partnerships,
                       AVG(p.runs) as avg_partnership,
                       MAX(p.runs) as highest_partnership,
                       COUNT(CASE WHEN p.runs >= 50 THEN 1 END) as partnerships_50_plus,
                       ROUND(COUNT(CASE WHEN p.runs >= 50 THEN 1 END) * 100.0 / COUNT(*), 2) as success_rate
                    FROM partnerships p
                    GROUP BY p.player_a, p.player_b
                    HAVING COUNT(*) >= 5
                )
                SELECT p1.full_name as player_a,
                       p2.full_name as player_b,
                       ps.total_partnerships,
                       ROUND(ps.avg_partnership, 2) as avg_runs,
                       ps.highest_partnership,
                       ps.partnerships_50_plus,
                       ps.success_rate
                FROM partnership_stats ps
                JOIN players p1 ON ps.player_a = p1.player_id
                JOIN players p2 ON ps.player_b = p2.player_id
                ORDER BY ps.success_rate DESC, ps.avg_partnership DESC;
            """
        },
        {
            "question": "25. Player performance time-series analysis",
            "query": """
                WITH quarterly_stats_raw AS (
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
                    HAVING COUNT(DISTINCT m.match_id) >= 3
                ),
                qualified_players AS (
                    SELECT player_id
                    FROM quarterly_stats_raw
                    GROUP BY player_id
                    HAVING COUNT(*) >= 6
                ),
                quarterly_stats AS (
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
                    SELECT 
                        player_id,
                        AVG(quarter_index) AS avg_q_index,
                        AVG(avg_runs) AS avg_runs_avg,
                        AVG(avg_sr) AS avg_sr_avg
                    FROM quarterly_stats
                    GROUP BY player_id
                ),
                career_trajectory AS (
                    SELECT 
                        q.player_id,
                        SUM((q.quarter_index - c.avg_q_index) * (q.avg_runs - c.avg_runs_avg)) / SUM(POW(q.quarter_index - c.avg_q_index, 2)) AS runs_trend,
                        SUM((q.quarter_index - c.avg_q_index) * (q.avg_sr - c.avg_sr_avg)) / SUM(POW(q.quarter_index - c.avg_q_index, 2)) AS sr_trend
                    FROM quarterly_stats q
                    JOIN career_trajectory_avg c ON q.player_id = c.player_id
                    GROUP BY q.player_id
                )
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
                WHERE qc.prev_avg_runs IS NOT NULL
                ORDER BY p.full_name, qc.quarter_label;
            """
        }
    ]

    # --- Streamlit UI ---
    st.set_page_config(page_title="Cricket SQL Dashboard", layout="wide")

    st.title("🏏 Cricket Analytics SQL Dashboard")
    st.write("Select a predefined SQL question to view insights from your cricket database.")

    # Question selection
    selected = st.selectbox("Select a question", [q["question"] for q in sql_questions])
    query = next(q["query"] for q in sql_questions if q["question"] == selected)

    # Display SQL
    with st.expander("📜 View SQL Query"):
        st.code(query, language="sql")

    # Execute query
    if st.button("▶️ Run Query"):
        try:
            df = run_query(query)
            st.success(f"✅ Query executed successfully! {len(df)} rows returned.")
            st.dataframe(df, use_container_width=True)

            # Export options
            csv = df.to_csv(index=False).encode("utf-8")
            st.download_button(
                "⬇️ Download CSV", 
                csv, 
                file_name="query_results.csv", 
                mime="text/csv"
            )

        except Exception as e:
            st.error(f"❌ Error executing query: {e}")

    # Available Tables section
    st.markdown("---")
    st.header("📊 Available Tables")
    
    # Define table descriptions based on your schema
    table_descriptions = {
        "teams": "Contains team information including name, country, and logo.",
        "venues": "Stores cricket venue details like name, city, country, capacity, and establishment year.",
        "series": "Contains cricket series information including name, host country, format, and dates.",
        "matches": "Stores match details including teams, venue, result, toss information, and match status.",
        "players": "Contains player information including personal details, role, batting and bowling styles.",
        "innings": "Records innings data for each match including batting/bowling teams and scores.",
        "batting": "Stores individual batting performances including runs, balls, boundaries, and strike rate.",
        "bowling": "Contains individual bowling performances including overs, maidens, runs, wickets, and economy.",
        "partnerships": "Records batting partnerships between players including runs and wicket number.",
        "player_aggregates": "Stores aggregated career statistics for players across different formats."
    }
    
    # Display tables in a nice format
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Table Name")
        for table_name in table_descriptions.keys():
            st.write(f"• **{table_name}**")
    
    with col2:
        st.subheader("Description")
        for table_name, description in table_descriptions.items():
            st.write(description)

    st.markdown("---")
    st.caption("Built with ❤️ using Streamlit and SQL for Cricket Analytics.")

if __name__ == "__main__":
    show()