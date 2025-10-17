-- Insert teams
INSERT INTO teams (name, country, short_name, logo_url) VALUES
('India', 'India', 'IND', 'https://example.com/india.png'),
('Australia', 'Australia', 'AUS', 'https://example.com/australia.png'),
('England', 'England', 'ENG', 'https://example.com/england.png'),
('New Zealand', 'New Zealand', 'NZ', 'https://example.com/newzealand.png'),
('South Africa', 'South Africa', 'SA', 'https://example.com/southafrica.png'),
('Pakistan', 'Pakistan', 'PAK', 'https://example.com/pakistan.png'),
('West Indies', 'West Indies', 'WI', 'https://example.com/westindies.png'),
('Sri Lanka', 'Sri Lanka', 'SL', 'https://example.com/srilanka.png'),
('Bangladesh', 'Bangladesh', 'BAN', 'https://example.com/bangladesh.png'),
('Afghanistan', 'Afghanistan', 'AFG', 'https://example.com/afghanistan.png');

-- Insert venues 
INSERT INTO venues (name, city, country, capacity, established) VALUES
('Eden Gardens', 'Kolkata', 'India', 68000, 1864),
('Melbourne Cricket Ground', 'Melbourne', 'Australia', 100024, 1853),
('Lord''s Cricket Ground', 'London', 'England', 30000, 1814),
('Sydney Cricket Ground', 'Sydney', 'Australia', 48000, 1848),
('Wankhede Stadium', 'Mumbai', 'India', 33000, 1974),
('The Oval', 'London', 'England', 25500, 1845),
('Newlands Cricket Ground', 'Cape Town', 'South Africa', 25000, 1888),
('Gaddafi Stadium', 'Lahore', 'Pakistan', 27000, 1959),
('Bay Oval', 'Mount Maunganui', 'New Zealand', 10000, 2005),
('Sher-e-Bangla Stadium', 'Dhaka', 'Bangladesh', 26000, 2006),
('Narendra Modi Stadium', 'Ahmedabad', 'India', 132000, 2020),
('Dubai International Stadium', 'Dubai', 'UAE', 25000, 2009),
('Sharjah Cricket Stadium', 'Sharjah', 'UAE', 27000, 1982);

-- Insert series
INSERT INTO series (name, host_country, format, start_date, planned_matches) VALUES
('India vs Australia 2024', 'India', 'ODI', '2024-09-01', 5),
('Ashes 2024', 'England', 'Test', '2024-06-01', 5),
('T20 World Cup 2024', 'West Indies', 'T20', '2024-06-10', 45),
('South Africa vs England 2024', 'South Africa', 'ODI', '2024-01-15', 3),
('New Zealand Tour 2024', 'New Zealand', 'Test', '2024-02-01', 2),
('Asia Cup 2024', 'Pakistan', 'ODI', '2024-08-15', 13),
('Border-Gavaskar Trophy 2023', 'India', 'Test', '2023-02-09', 4),
('England vs Pakistan 2023', 'England', 'T20', '2023-08-30', 7),
('ICC World Cup 2023', 'India', 'ODI', '2023-10-05', 48),
('West Indies vs India 2023', 'West Indies', 'T20', '2023-07-28', 5);

-- Insert players
INSERT INTO players (full_name, short_name, team_id, country, role, batting_style, bowling_style, dob) VALUES
-- Indian players
('Virat Kohli', 'V Kohli', 1, 'India', 'Batsman', 'Right-handed', 'Right-arm medium', '1988-11-05'),
('Rohit Sharma', 'R Sharma', 1, 'India', 'Batsman', 'Right-handed', 'Right-arm offbreak', '1987-04-30'),
('Jasprit Bumrah', 'J Bumrah', 1, 'India', 'Bowler', 'Right-handed', 'Right-arm fast', '1993-12-06'),
('Ravindra Jadeja', 'RA Jadeja', 1, 'India', 'All-rounder', 'Left-handed', 'Left-arm orthodox', '1988-12-06'),
('Rishabh Pant', 'RR Pant', 1, 'India', 'Wicket-keeper', 'Left-handed', NULL, '1997-10-04'),
('KL Rahul', 'KL Rahul', 1, 'India', 'Batsman', 'Right-handed', NULL, '1992-04-18'),

-- Australian players
('Steve Smith', 'SPD Smith', 2, 'Australia', 'Batsman', 'Right-handed', 'Right-arm legbreak', '1989-06-02'),
('Pat Cummins', 'PJ Cummins', 2, 'Australia', 'Bowler', 'Right-handed', 'Right-arm fast', '1993-05-08'),
('Glenn Maxwell', 'GJ Maxwell', 2, 'Australia', 'All-rounder', 'Right-handed', 'Right-arm offbreak', '1988-10-14'),
('David Warner', 'DA Warner', 2, 'Australia', 'Batsman', 'Left-handed', 'Right-arm legbreak', '1986-10-27'),
('Mitchell Starc', 'MA Starc', 2, 'Australia', 'Bowler', 'Left-handed', 'Left-arm fast', '1990-01-30'),
('Alex Carey', 'AT Carey', 2, 'Australia', 'Wicket-keeper', 'Left-handed', NULL, '1991-08-27'),

-- Other teams players
('Joe Root', 'JE Root', 3, 'England', 'Batsman', 'Right-handed', 'Right-arm offbreak', '1990-12-30'),
('Ben Stokes', 'BA Stokes', 3, 'England', 'All-rounder', 'Left-handed', 'Right-arm fast-medium', '1991-06-04'),
('Jofra Archer', 'JC Archer', 3, 'England', 'Bowler', 'Right-handed', 'Right-arm fast', '1995-04-01'),
('Jos Buttler', 'JC Buttler', 3, 'England', 'Wicket-keeper', 'Right-handed', NULL, '1990-09-08'),

('Kane Williamson', 'KS Williamson', 4, 'New Zealand', 'Batsman', 'Right-handed', 'Right-arm offbreak', '1990-08-08'),
('Trent Boult', 'TA Boult', 4, 'New Zealand', 'Bowler', 'Right-handed', 'Left-arm fast-medium', '1989-07-22'),

('Kagiso Rabada', 'K Rabada', 5, 'South Africa', 'Bowler', 'Left-handed', 'Right-arm fast', '1995-05-25'),
('Quinton de Kock', 'Q de Kock', 5, 'South Africa', 'Wicket-keeper', 'Left-handed', NULL, '1992-12-17'),

('Babar Azam', 'Babar Azam', 6, 'Pakistan', 'Batsman', 'Right-handed', 'Right-arm offbreak', '1994-10-15'),
('Shaheen Afridi', 'Shaheen Afridi', 6, 'Pakistan', 'Bowler', 'Left-handed', 'Left-arm fast', '2000-04-06'),

('Shakib Al Hasan', 'Shakib Al Hasan', 9, 'Bangladesh', 'All-rounder', 'Left-handed', 'Left-arm orthodox', '1987-03-24'),
('Rashid Khan', 'Rashid Khan', 10, 'Afghanistan', 'Bowler', 'Right-handed', 'Right-arm legbreak', '1998-09-20'),
('Ross Taylor', 'LRPL Taylor', 4, 'New Zealand', 'Batsman', 'Right-handed', 'Right-arm offbreak', '1984-03-08');

-- Insert matches (40+ matches across different formats and dates)
INSERT INTO matches (series_id, description, date, venue_id, home_team_id, away_team_id, winner_team_id, toss_winner_id, toss_decision, victory_type, victory_margin, status) VALUES
-- Test matches
(2, 'ENG vs AUS, 1st Test', '2024-06-01', 3, 3, 2, 3, 3, 'bat', 'runs', 28, 'completed'),
(2, 'ENG vs AUS, 2nd Test', '2024-06-08', 6, 3, 2, 2, 2, 'bowl', 'wickets', 4, 'completed'),

-- T20 matches
(3, 'WI vs IND, Group Match', '2024-06-10', 7, 7, 1, 1, 7, 'bat', 'wickets', 7, 'completed'),
(3, 'AUS vs ENG, Group Match', '2024-06-12', 8, 2, 3, 2, 2, 'bowl', 'runs', 35, 'completed'),

-- More matches for statistics
(4, 'SA vs ENG, 1st ODI', '2024-01-15', 7, 5, 3, 5, 5, 'bat', 'runs', 17, 'completed'),
(4, 'SA vs ENG, 2nd ODI', '2024-01-18', 7, 5, 3, 3, 3, 'bowl', 'wickets', 3, 'completed'),
(5, 'NZ vs IND, 1st Test', '2024-02-01', 9, 4, 1, 4, 4, 'bat', 'runs', 62, 'completed'),

-- Close matches for Question 15
(6, 'IND vs PAK, Close Match 1', '2024-03-01', 11, 1, 6, 1, 1, 'bat', 'runs', 3, 'completed'),
(6, 'AUS vs ENG, Close Match 2', '2024-03-05', 2, 2, 3, 2, 2, 'bowl', 'wickets', 1, 'completed'),
(6, 'SA vs NZ, Close Match 3', '2024-03-10', 7, 5, 4, 5, 5, 'bat', 'runs', 12, 'completed'),

-- More matches for bowling statistics
(7, 'IND vs AUS, Test 1', '2023-02-09', 1, 1, 2, 1, 1, 'bat', 'runs', 125, 'completed'),
(7, 'IND vs AUS, Test 2', '2023-02-17', 5, 1, 2, 2, 2, 'bowl', 'wickets', 6, 'completed'),

-- T20 matches for format comparison
(8, 'ENG vs PAK, 1st T20', '2023-08-30', 3, 3, 6, 3, 3, 'bat', 'runs', 42, 'completed'),
(8, 'ENG vs PAK, 2nd T20', '2023-09-01', 6, 3, 6, 6, 6, 'bowl', 'wickets', 5, 'completed'),

-- World Cup matches
(9, 'IND vs AUS, WC Match', '2023-10-08', 11, 1, 2, 1, 2, 'bowl', 'runs', 36, 'completed'),
(9, 'ENG vs SA, WC Match', '2023-10-10', 7, 3, 5, 3, 3, 'bat', 'wickets', 4, 'completed'),

-- More matches to satisfy 10+ matches condition for bowlers
(1, 'IND vs AUS, 4th ODI', '2024-09-10', 5, 1, 2, 2, 2, 'bowl', 'runs', 18, 'completed'),
(1, 'IND vs AUS, 5th ODI', '2024-09-13', 1, 1, 2, 1, 1, 'bat', 'wickets', 3, 'completed'),
(3, 'WI vs AUS, T20', '2024-06-15', 7, 7, 2, 2, 2, 'bowl', 'runs', 25, 'completed'),
(3, 'ENG vs NZ, T20', '2024-06-18', 3, 3, 4, 3, 3, 'bat', 'wickets', 6, 'completed'),
(8, 'ENG vs PAK, 3rd T20', '2023-09-03', 6, 3, 6, 3, 3, 'bat', 'runs', 15, 'completed'),
-- More matches at Eden Gardens for Bumrah
(1, 'IND vs AUS, ODI 4', '2024-09-15', 1, 1, 2, 1, 1, 'bat', 'runs', 25, 'completed'),
(1, 'IND vs AUS, ODI 5', '2024-09-18', 1, 1, 2, 2, 2, 'bowl', 'wickets', 4, 'completed'),

-- More matches at MCG for Cummins
(2, 'ENG vs AUS, Test 3', '2024-06-15', 2, 3, 2, 2, 2, 'bowl', 'runs', 45, 'completed'),
(2, 'ENG vs AUS, Test 4', '2024-06-22', 2, 3, 2, 3, 3, 'bat', 'wickets', 3, 'completed'),

-- More matches at Lord's for Archer
(8, 'ENG vs PAK, T20 4', '2023-09-05', 3, 3, 6, 3, 3, 'bat', 'runs', 18, 'completed'),
(8, 'ENG vs PAK, T20 5', '2023-09-08', 3, 3, 6, 6, 6, 'bowl', 'wickets', 2, 'completed'),
-- Close matches (victory_margin < 50 runs)
(1, 'IND vs AUS, Close ODI 1', '2024-08-01', 1, 1, 2, 1, 1, 'bat', 'runs', 12, 'completed'),
(1, 'IND vs AUS, Close ODI 2', '2024-08-05', 5, 1, 2, 2, 2, 'bowl', 'runs', 8, 'completed'),
(4, 'SA vs ENG, Close ODI', '2024-02-10', 7, 5, 3, 5, 5, 'bat', 'runs', 25, 'completed'),

-- Close matches (victory_margin < 5 wickets)
(1, 'IND vs AUS, Close ODI 3', '2024-08-10', 1, 1, 2, 1, 1, 'bat', 'wickets', 2, 'completed'),
(3, 'WI vs IND, Close T20', '2024-06-20', 7, 7, 1, 1, 7, 'bat', 'wickets', 1, 'completed'),
(8, 'ENG vs PAK, Close T20', '2023-09-12', 3, 3, 6, 3, 3, 'bat', 'wickets', 3, 'completed'),
-- 2020 matches
(10, 'IND vs AUS 2020 ODI 1', '2020-01-14', 1, 1, 2, 1, 1, 'bat', 'runs', 36, 'completed'),
(10, 'IND vs AUS 2020 ODI 2', '2020-01-17', 5, 1, 2, 2, 2, 'bowl', 'wickets', 4, 'completed'),
(10, 'IND vs AUS 2020 ODI 3', '2020-01-19', 1, 1, 2, 1, 1, 'bat', 'runs', 25, 'completed'),
(10, 'IND vs AUS 2020 ODI 4', '2020-01-22', 5, 1, 2, 1, 2, 'bowl', 'runs', 18, 'completed'),
(10, 'IND vs AUS 2020 ODI 5', '2020-01-25', 1, 1, 2, 2, 1, 'bat', 'wickets', 3, 'completed'),

-- 2021 matches
(11, 'ENG vs IND 2021 ODI 1', '2021-03-23', 3, 3, 1, 3, 3, 'bat', 'runs', 42, 'completed'),
(11, 'ENG vs IND 2021 ODI 2', '2021-03-26', 6, 3, 1, 1, 1, 'bowl', 'wickets', 5, 'completed'),
(11, 'ENG vs IND 2021 ODI 3', '2021-03-28', 3, 3, 1, 3, 3, 'bat', 'runs', 28, 'completed'),
(11, 'ENG vs IND 2021 ODI 4', '2021-03-31', 6, 3, 1, 1, 1, 'bowl', 'runs', 15, 'completed'),
(11, 'ENG vs IND 2021 ODI 5', '2021-04-03', 3, 3, 1, 3, 3, 'bat', 'wickets', 2, 'completed'),

-- 2022 matches
(12, 'IND vs SA 2022 ODI 1', '2022-06-10', 1, 1, 5, 1, 1, 'bat', 'runs', 32, 'completed'),
(12, 'IND vs SA 2022 ODI 2', '2022-06-13', 5, 1, 5, 5, 5, 'bowl', 'wickets', 4, 'completed'),
(12, 'IND vs SA 2022 ODI 3', '2022-06-16', 1, 1, 5, 1, 1, 'bat', 'runs', 22, 'completed'),
(12, 'IND vs SA 2022 ODI 4', '2022-06-19', 5, 1, 5, 5, 5, 'bowl', 'runs', 18, 'completed'),
(12, 'IND vs SA 2022 ODI 5', '2022-06-22', 1, 1, 5, 1, 1, 'bat', 'wickets', 3, 'completed'),

-- 2023 matches
(13, 'AUS vs IND 2023 ODI 1', '2023-09-22', 2, 2, 1, 2, 2, 'bat', 'runs', 38, 'completed'),
(13, 'AUS vs IND 2023 ODI 2', '2023-09-25', 4, 2, 1, 1, 1, 'bowl', 'wickets', 4, 'completed'),
(13, 'AUS vs IND 2023 ODI 3', '2023-09-28', 2, 2, 1, 2, 2, 'bat', 'runs', 26, 'completed'),
(13, 'AUS vs IND 2023 ODI 4', '2023-10-01', 4, 2, 1, 1, 1, 'bowl', 'runs', 19, 'completed'),
(13, 'AUS vs IND 2023 ODI 5', '2023-10-04', 2, 2, 1, 2, 2, 'bat', 'wickets', 2, 'completed'),
-- ODI matches
(1, 'IND vs AUS ODI 6', '2024-09-20', 1, 1, 2, 1, 1, 'bat', 'runs', 28, 'completed'),
(1, 'IND vs AUS ODI 7', '2024-09-23', 5, 1, 2, 2, 2, 'bowl', 'wickets', 3, 'completed'),
(1, 'IND vs AUS ODI 8', '2024-09-26', 1, 1, 2, 1, 1, 'bat', 'runs', 35, 'completed'),
(1, 'IND vs AUS ODI 9', '2024-09-29', 5, 1, 2, 2, 2, 'bowl', 'wickets', 2, 'completed'),
(1, 'IND vs AUS ODI 10', '2024-10-02', 1, 1, 2, 1, 1, 'bat', 'runs', 22, 'completed'),

-- T20 matches
(3, 'WI vs IND T20 2', '2024-06-25', 7, 7, 1, 1, 7, 'bat', 'wickets', 4, 'completed'),
(3, 'WI vs IND T20 3', '2024-06-28', 8, 7, 1, 7, 7, 'bowl', 'runs', 18, 'completed'),
(3, 'WI vs IND T20 4', '2024-07-01', 7, 7, 1, 1, 1, 'bat', 'wickets', 3, 'completed'),
(3, 'WI vs IND T20 5', '2024-07-04', 8, 7, 1, 7, 7, 'bowl', 'runs', 12, 'completed'),

-- More T20 matches for variety
(8, 'ENG vs PAK T20 6', '2023-09-15', 3, 3, 6, 3, 3, 'bat', 'runs', 25, 'completed'),
(8, 'ENG vs PAK T20 7', '2023-09-18', 6, 3, 6, 6, 6, 'bowl', 'wickets', 4, 'completed'),
-- Test matches 2023-2024
(2, 'ENG vs AUS Test 3', '2024-06-15', 2, 3, 2, 2, 2, 'bowl', 'runs', 45, 'completed'),
(2, 'ENG vs AUS Test 4', '2024-06-22', 6, 3, 2, 3, 3, 'bat', 'wickets', 3, 'completed'),
(2, 'ENG vs AUS Test 5', '2024-06-29', 3, 3, 2, 2, 2, 'bowl', 'runs', 28, 'completed'),

(7, 'IND vs AUS Test 3', '2023-02-24', 5, 1, 2, 1, 1, 'bat', 'runs', 75, 'completed'),
(7, 'IND vs AUS Test 4', '2023-03-03', 1, 1, 2, 2, 2, 'bowl', 'wickets', 5, 'completed'),

-- More Test matches for other teams
(14, 'SA vs IND Test 1', '2023-12-10', 7, 5, 1, 5, 5, 'bat', 'runs', 68, 'completed'),
(14, 'SA vs IND Test 2', '2023-12-17', 7, 5, 1, 1, 1, 'bowl', 'wickets', 4, 'completed'),
(15, 'NZ vs PAK Test 1', '2023-11-05', 9, 4, 6, 4, 4, 'bat', 'runs', 52, 'completed'),
(15, 'NZ vs PAK Test 2', '2023-11-12', 9, 4, 6, 6, 6, 'bowl', 'wickets', 3, 'completed'),
-- ODI matches 2023-2024
(1, 'IND vs AUS ODI 11', '2024-10-05', 5, 1, 2, 2, 2, 'bowl', 'runs', 19, 'completed'),
(1, 'IND vs AUS ODI 12', '2024-10-08', 1, 1, 2, 1, 1, 'bat', 'wickets', 4, 'completed'),
(1, 'IND vs AUS ODI 13', '2024-10-11', 5, 1, 2, 2, 2, 'bowl', 'runs', 24, 'completed'),

(16, 'IND vs ENG ODI 1', '2023-07-10', 1, 1, 3, 1, 1, 'bat', 'runs', 32, 'completed'),
(16, 'IND vs ENG ODI 2', '2023-07-13', 5, 1, 3, 3, 3, 'bowl', 'wickets', 3, 'completed'),
(16, 'IND vs ENG ODI 3', '2023-07-16', 1, 1, 3, 1, 1, 'bat', 'runs', 28, 'completed'),

(17, 'AUS vs SA ODI 1', '2023-08-05', 2, 2, 5, 2, 2, 'bat', 'runs', 35, 'completed'),
(17, 'AUS vs SA ODI 2', '2023-08-08', 4, 2, 5, 5, 5, 'bowl', 'wickets', 2, 'completed'),
(17, 'AUS vs SA ODI 3', '2023-08-11', 2, 2, 5, 2, 2, 'bat', 'runs', 22, 'completed'),
-- T20 matches 2023-2024
(3, 'WI vs IND T20 6', '2024-07-07', 7, 7, 1, 1, 1, 'bat', 'wickets', 5, 'completed'),
(3, 'WI vs IND T20 7', '2024-07-10', 8, 7, 1, 7, 7, 'bowl', 'runs', 16, 'completed'),
(3, 'WI vs IND T20 8', '2024-07-13', 7, 7, 1, 1, 1, 'bat', 'wickets', 4, 'completed'),

(8, 'ENG vs PAK T20 8', '2023-09-21', 6, 3, 6, 3, 3, 'bat', 'runs', 21, 'completed'),
(8, 'ENG vs PAK T20 9', '2023-09-24', 3, 3, 6, 6, 6, 'bowl', 'wickets', 3, 'completed'),
(8, 'ENG vs PAK T20 10', '2023-09-27', 6, 3, 6, 3, 3, 'bat', 'runs', 18, 'completed'),

(18, 'IND vs AUS T20 1', '2023-10-15', 1, 1, 2, 1, 1, 'bat', 'runs', 25, 'completed'),
(18, 'IND vs AUS T20 2', '2023-10-18', 5, 1, 2, 2, 2, 'bowl', 'wickets', 4, 'completed'),
(18, 'IND vs AUS T20 3', '2023-10-21', 1, 1, 2, 1, 1, 'bat', 'runs', 19, 'completed');

-- Insert innings (2 innings per match)
INSERT INTO innings (match_id, batting_team_id, bowling_team_id, innings_no, total_runs, wickets, overs) VALUES
-- For recent ODI matches
(1, 1, 2, 1, 325, 8, 50.0), (1, 2, 1, 2, 280, 10, 48.3),
(2, 1, 2, 1, 245, 9, 50.0), (2, 2, 1, 2, 246, 5, 47.2),
(3, 1, 2, 1, 312, 7, 50.0), (3, 2, 1, 2, 300, 9, 49.5),

-- For Test matches
(4, 3, 2, 1, 387, 10, 110.2), (4, 2, 3, 2, 359, 10, 105.5),
(5, 3, 2, 1, 285, 10, 85.0), (5, 2, 3, 2, 289, 6, 82.3),

-- For T20 matches
(6, 7, 1, 1, 165, 8, 20.0), (6, 1, 7, 2, 166, 3, 18.2),
(7, 2, 3, 1, 182, 6, 20.0), (7, 3, 2, 2, 147, 10, 18.5),

-- More innings for statistics
(8, 5, 3, 1, 278, 9, 50.0), (8, 3, 5, 2, 261, 10, 49.1),
(9, 5, 3, 1, 245, 8, 50.0), (9, 3, 5, 2, 246, 7, 49.3),
-- For new matches
(26, 1, 2, 1, 295, 7, 50.0), (26, 2, 1, 2, 270, 9, 48.5),
(27, 1, 2, 1, 265, 8, 50.0), (27, 2, 1, 2, 266, 5, 49.2),
(28, 3, 2, 1, 325, 9, 95.0), (28, 2, 3, 2, 280, 10, 87.3),
(29, 3, 2, 1, 285, 8, 90.0), (29, 2, 3, 2, 287, 6, 85.4),
(30, 3, 6, 1, 175, 6, 20.0), (30, 6, 3, 2, 157, 8, 19.3),
(31, 3, 6, 1, 182, 7, 20.0), (31, 6, 3, 2, 183, 5, 19.5),
-- For close matches
(32, 1, 2, 1, 285, 8, 50.0), (32, 2, 1, 2, 273, 9, 50.0),
(33, 1, 2, 1, 245, 9, 50.0), (33, 2, 1, 2, 237, 8, 49.3),
(34, 5, 3, 1, 265, 7, 50.0), (34, 3, 5, 2, 240, 10, 48.2),
(35, 1, 2, 1, 312, 6, 50.0), (35, 2, 1, 2, 310, 4, 49.4),
(36, 7, 1, 1, 165, 7, 20.0), (36, 1, 7, 2, 164, 3, 19.5),
(37, 3, 6, 1, 182, 5, 20.0), (37, 6, 3, 2, 179, 8, 20.0),
-- 2020 matches
(38, 1, 2, 1, 285, 7, 50.0), (39, 2, 1, 2, 249, 9, 50.0),
(40, 1, 2, 1, 312, 6, 50.0), (41, 2, 1, 2, 287, 8, 50.0),
(42, 1, 2, 1, 265, 8, 50.0), (43, 2, 1, 2, 262, 7, 49.3),
(44, 1, 2, 1, 278, 6, 50.0), (45, 2, 1, 2, 260, 9, 49.1),
(46, 1, 2, 1, 245, 9, 50.0), (47, 2, 1, 2, 246, 7, 49.4),

-- 2021 matches
(48, 3, 1, 1, 295, 8, 50.0), (49, 1, 3, 2, 253, 10, 48.2),
(50, 3, 1, 1, 285, 7, 50.0), (51, 1, 3, 2, 286, 5, 49.3),
(52, 3, 1, 1, 272, 6, 50.0), (53, 1, 3, 2, 244, 9, 49.1),
(54, 3, 1, 1, 258, 8, 50.0), (55, 1, 3, 2, 243, 10, 48.5),
(56, 3, 1, 1, 265, 7, 50.0), (57, 1, 3, 2, 266, 8, 49.4),

-- 2022 matches
(58, 1, 5, 1, 312, 5, 50.0), (59, 5, 1, 2, 280, 9, 50.0),
(60, 1, 5, 1, 285, 6, 50.0), (61, 5, 1, 2, 286, 4, 49.5),
(62, 1, 5, 1, 298, 7, 50.0), (63, 5, 1, 2, 276, 8, 50.0),
(64, 1, 5, 1, 265, 8, 50.0), (65, 5, 1, 2, 247, 10, 48.3),
(66, 1, 5, 1, 278, 6, 50.0), (67, 5, 1, 2, 279, 7, 49.5),

-- 2023 matches
(68, 2, 1, 1, 295, 7, 50.0), (69, 1, 2, 2, 257, 9, 50.0),
(70, 2, 1, 1, 285, 6, 50.0), (71, 1, 2, 2, 286, 5, 49.4),
(72, 2, 1, 1, 272, 8, 50.0), (73, 1, 2, 2, 246, 10, 48.2),
(74, 2, 1, 1, 265, 7, 50.0), (75, 1, 2, 2, 246, 9, 49.1),
(76, 2, 1, 1, 278, 6, 50.0), (77, 1, 2, 2, 279, 8, 49.5),
-- ODI innings
(78, 1, 2, 1, 285, 7, 50.0), (79, 2, 1, 2, 257, 9, 50.0),
(80, 1, 2, 1, 295, 6, 50.0), (81, 2, 1, 2, 260, 8, 49.3),
(82, 1, 2, 1, 278, 8, 50.0), (83, 2, 1, 2, 256, 10, 48.5),
(84, 1, 2, 1, 265, 7, 50.0), (85, 2, 1, 2, 243, 9, 49.2),
(86, 1, 2, 1, 272, 6, 50.0), (87, 2, 1, 2, 250, 8, 49.4),

-- T20 innings
(88, 7, 1, 1, 165, 7, 20.0), (89, 1, 7, 2, 161, 3, 19.2),
(90, 7, 1, 1, 158, 8, 20.0), (91, 1, 7, 2, 140, 10, 18.5),
(92, 7, 1, 1, 172, 6, 20.0), (93, 1, 7, 2, 169, 5, 19.4),
(94, 7, 1, 1, 155, 9, 20.0), (95, 1, 7, 2, 143, 8, 19.3),
(96, 3, 6, 1, 182, 5, 20.0), (97, 6, 3, 2, 157, 9, 19.5),
(98, 3, 6, 1, 175, 7, 20.0), (99, 6, 3, 2, 150, 10, 19.2);

-- Insert batting records (extensive data for all queries)
INSERT INTO batting (innings_id, player_id, runs, balls, fours, sixes, dismissal, batting_position, strike_rate) VALUES
-- Recent performances for form analysis
(1, 1, 120, 110, 12, 3, 'caught', 3, 109.09), (1, 2, 85, 90, 8, 2, 'bowled', 1, 94.44),
(2, 4, 95, 105, 9, 1, 'lbw', 3, 90.48), (2, 6, 65, 55, 5, 3, 'run out', 5, 118.18),
(3, 1, 78, 85, 7, 1, 'caught', 3, 91.76), (3, 2, 45, 50, 4, 1, 'bowled', 1, 90.00),

-- Test match performances
(4, 7, 145, 210, 16, 2, 'bowled', 3, 69.05), (4, 8, 82, 125, 9, 1, 'caught', 4, 65.60),
(5, 10, 112, 145, 12, 3, 'lbw', 1, 77.24), (5, 11, 67, 98, 7, 0, 'caught', 2, 68.37),

-- T20 performances
(6, 1, 68, 42, 6, 3, 'caught', 3, 161.90), (6, 2, 54, 38, 5, 2, 'bowled', 1, 142.11),
(7, 13, 89, 52, 8, 5, 'not out', 4, 171.15), (7, 14, 45, 32, 4, 2, 'run out', 5, 140.63),

-- More performances for statistics
(8, 17, 78, 85, 7, 1, 'caught', 3, 91.76), (8, 18, 45, 50, 4, 1, 'bowled', 1, 90.00),
(9, 19, 112, 125, 10, 3, 'lbw', 2, 89.60), (9, 20, 67, 88, 6, 1, 'caught', 4, 76.14),
-- Virat Kohli in close matches
(43, 1, 95, 108, 8, 2, 'caught', 3, 87.96),  -- Match 32
(45, 1, 78, 85, 6, 1, 'bowled', 3, 91.76),   -- Match 33
(47, 1, 112, 120, 10, 3, 'not out', 3, 93.33), -- Match 35
(49, 1, 68, 45, 5, 3, 'caught', 3, 151.11),  -- Match 36

-- Rohit Sharma in close matches
(43, 2, 65, 70, 5, 2, 'lbw', 1, 92.86),      -- Match 32
(45, 2, 42, 50, 4, 1, 'caught', 1, 84.00),   -- Match 33
(47, 2, 85, 90, 7, 2, 'run out', 1, 94.44),  -- Match 35
(49, 2, 54, 38, 4, 3, 'bowled', 1, 142.11),  -- Match 36

-- Steve Smith in close matches
(44, 7, 88, 95, 7, 1, 'caught', 3, 92.63),   -- Match 32
(46, 7, 62, 75, 5, 0, 'lbw', 3, 82.67),      -- Match 33
(48, 7, 45, 50, 4, 0, 'bowled', 3, 90.00),   -- Match 35

-- Joe Root in close matches
(50, 13, 76, 68, 6, 2, 'not out', 4, 111.76), -- Match 37
(52, 13, 58, 52, 5, 1, 'caught', 4, 111.54), -- Additional match

-- Ben Stokes in close matches
(50, 14, 45, 32, 3, 2, 'run out', 5, 140.63), -- Match 37
(52, 14, 68, 45, 5, 3, 'not out', 5, 151.11), -- Additional match
-- Virat Kohli 2020-2023
(38, 1, 112, 120, 10, 2, 'caught', 3, 93.33), (40, 1, 85, 95, 7, 1, 'bowled', 3, 89.47),
(42, 1, 78, 85, 6, 1, 'lbw', 3, 91.76), (44, 1, 95, 108, 8, 2, 'caught', 3, 87.96),
(46, 1, 65, 70, 5, 1, 'run out', 3, 92.86), (49, 1, 102, 115, 9, 3, 'not out', 3, 88.70),
(51, 1, 88, 95, 7, 2, 'caught', 3, 92.63), (53, 1, 72, 80, 6, 1, 'bowled', 3, 90.00),
(55, 1, 95, 105, 8, 2, 'caught', 3, 90.48), (57, 1, 68, 75, 5, 1, 'lbw', 3, 90.67),
(59, 1, 115, 125, 10, 4, 'caught', 3, 92.00), (61, 1, 82, 90, 7, 1, 'bowled', 3, 91.11),
(63, 1, 78, 85, 6, 2, 'caught', 3, 91.76), (65, 1, 92, 100, 8, 2, 'not out', 3, 92.00),
(67, 1, 65, 70, 5, 1, 'run out', 3, 92.86), (69, 1, 105, 115, 9, 3, 'caught', 3, 91.30),
(71, 1, 88, 95, 7, 2, 'bowled', 3, 92.63), (73, 1, 72, 80, 6, 1, 'caught', 3, 90.00),
(75, 1, 95, 105, 8, 2, 'not out', 3, 90.48), (77, 1, 68, 75, 5, 1, 'lbw', 3, 90.67),

-- Rohit Sharma 2020-2023
(38, 2, 85, 90, 8, 2, 'bowled', 1, 94.44), (40, 2, 78, 85, 7, 1, 'caught', 1, 91.76),
(42, 2, 65, 70, 5, 2, 'lbw', 1, 92.86), (44, 2, 92, 100, 8, 3, 'caught', 1, 92.00),
(46, 2, 58, 65, 5, 1, 'run out', 1, 89.23), (48, 2, 95, 105, 9, 2, 'bowled', 1, 90.48),
(50, 2, 82, 90, 7, 2, 'caught', 1, 91.11), (52, 2, 68, 75, 6, 1, 'lbw', 1, 90.67),
(54, 2, 105, 115, 10, 3, 'caught', 1, 91.30), (56, 2, 78, 85, 7, 1, 'bowled', 1, 91.76),
(58, 2, 112, 120, 10, 4, 'caught', 1, 93.33), (60, 2, 85, 95, 8, 2, 'bowled', 1, 89.47),
(62, 2, 95, 105, 9, 2, 'caught', 1, 90.48), (64, 2, 72, 80, 6, 1, 'lbw', 1, 90.00),
(66, 2, 88, 95, 7, 2, 'run out', 1, 92.63), (68, 2, 102, 115, 9, 3, 'caught', 1, 88.70),
(70, 2, 78, 85, 7, 1, 'bowled', 1, 91.76), (72, 2, 95, 105, 8, 2, 'caught', 1, 90.48),
(74, 2, 65, 70, 5, 1, 'lbw', 1, 92.86), (76, 2, 88, 95, 7, 2, 'not out', 1, 92.63);

-- Insert bowling records (extensive data for economy rate analysis)
INSERT INTO bowling (innings_id, player_id, overs, maidens, runs, wickets, economy) VALUES
-- Recent bowling performances
(1, 3, 10.0, 1, 48, 3, 4.80), (1, 8, 9.3, 0, 52, 2, 5.47),
(2, 9, 10.0, 0, 55, 1, 5.50), (2, 15, 9.0, 1, 42, 3, 4.67),
(3, 3, 9.0, 2, 35, 4, 3.89), (3, 8, 8.5, 0, 45, 2, 5.09),

-- Test bowling
(4, 8, 25.2, 5, 87, 4, 3.43), (4, 11, 23.0, 4, 75, 3, 3.26),
(5, 3, 22.5, 3, 68, 5, 2.98), (5, 15, 20.0, 2, 72, 2, 3.60),

-- T20 bowling
(6, 16, 4.0, 0, 28, 2, 7.00), (6, 20, 3.2, 0, 35, 1, 10.50),
(7, 8, 4.0, 0, 32, 3, 8.00), (7, 11, 3.5, 0, 40, 2, 10.43),
-- Jasprit Bumrah at Eden Gardens (3+ matches)
(1, 3, 9.0, 1, 42, 3, 4.67),
(3, 3, 8.5, 0, 38, 4, 4.32),
(5, 3, 10.0, 2, 35, 5, 3.50),

-- Pat Cummins at MCG (3+ matches)
(2, 8, 9.0, 1, 45, 2, 5.00),
(4, 8, 8.2, 0, 40, 3, 4.80),
(6, 8, 9.5, 1, 48, 2, 4.88),

-- Jofra Archer at Lord's (3+ matches)
(7, 15, 8.0, 0, 36, 3, 4.50),
(9, 15, 9.0, 1, 42, 2, 4.67),
(11, 15, 8.5, 0, 39, 4, 4.47),

-- Trent Boult at Bay Oval (3+ matches)
(8, 20, 9.0, 1, 44, 3, 4.89),
(10, 20, 8.2, 0, 38, 2, 4.56),
(12, 20, 9.5, 2, 35, 4, 3.55),

-- More matches to ensure venue consistency
(13, 3, 9.0, 1, 40, 2, 4.44),  -- Bumrah at Eden Gardens
(15, 3, 8.5, 0, 37, 3, 4.24),  -- Bumrah at Eden Gardens

(14, 8, 9.0, 1, 43, 2, 4.78),  -- Cummins at MCG
(16, 8, 8.2, 0, 39, 3, 4.73),  -- Cummins at MCG
-- More bowling for statistics (10+ matches condition)
(1, 3, 9.5, 1, 42, 2, 4.32), (2, 3, 8.0, 0, 38, 3, 4.75),
(3, 3, 10.0, 2, 35, 4, 3.50), (8, 3, 9.2, 1, 40, 2, 4.29),
(9, 3, 8.0, 0, 45, 1, 5.63), (10, 3, 10.0, 1, 48, 3, 4.80),
(11, 3, 9.5, 0, 52, 2, 5.32), (12, 3, 8.0, 1, 36, 3, 4.50),
(13, 3, 10.0, 2, 34, 4, 3.40), (14, 3, 9.0, 0, 55, 1, 6.11),
-- Jasprit Bumrah - ODI (12 matches)
(1, 3, 9.0, 1, 42, 3, 4.67), (5, 3, 8.5, 0, 38, 4, 4.32),
(25, 3, 9.2, 1, 40, 2, 4.29), (33, 3, 8.0, 1, 35, 3, 4.38),
(35, 3, 9.0, 2, 32, 4, 3.56), (79, 3, 9.5, 1, 45, 2, 4.55),
(81, 3, 8.2, 0, 38, 3, 4.56), (83, 3, 9.0, 1, 42, 2, 4.67),
(85, 3, 8.5, 0, 36, 4, 4.09), (87, 3, 9.0, 2, 34, 3, 3.78),
(89, 3, 4.0, 0, 28, 2, 7.00), (91, 3, 4.0, 1, 25, 3, 6.25),

-- Pat Cummins - ODI (10 matches)
(4, 8, 22.0, 3, 68, 4, 3.09), (6, 8, 20.5, 2, 72, 3, 3.47),
(37, 8, 23.2, 4, 65, 5, 2.78), (39, 8, 21.0, 3, 62, 4, 2.95),
(80, 8, 9.0, 1, 45, 2, 5.00), (82, 8, 9.5, 0, 48, 1, 4.88),
(84, 8, 9.0, 1, 42, 3, 4.67), (86, 8, 9.2, 0, 46, 2, 4.93),
(88, 8, 4.0, 0, 32, 2, 8.00), (90, 8, 4.0, 1, 28, 3, 7.00),

-- Jofra Archer - T20 (12 matches)
(19, 15, 4.0, 0, 28, 2, 7.00), (21, 15, 4.0, 1, 25, 3, 6.25),
(41, 15, 4.0, 0, 30, 2, 7.50), (43, 15, 4.0, 1, 26, 3, 6.50),
(93, 15, 4.0, 0, 35, 1, 8.75), (95, 15, 4.0, 1, 29, 2, 7.25),
(97, 15, 4.0, 0, 32, 2, 8.00), (99, 15, 4.0, 1, 27, 3, 6.75),
(89, 15, 4.0, 0, 31, 1, 7.75), (91, 15, 4.0, 1, 28, 2, 7.00),
(88, 15, 4.0, 0, 34, 1, 8.50), (90, 15, 4.0, 1, 26, 3, 6.50);

-- Insert partnerships (for partnership analysis)
INSERT INTO partnerships (innings_id, player_a, player_b, runs, wicket_number) VALUES
(1, 1, 2, 150, 2),
(1, 1, 5, 85, 3),
(2, 7, 9, 120, 3),
(2, 7, 10, 65, 4),
(3, 1, 2, 110, 2),
(3, 1, 5, 95, 3),
(4, 13, 14, 135, 3),
(4, 13, 16, 80, 4),
-- Kohli & Sharma partnerships (6 partnerships)
(1, 1, 2, 85, 2),   -- Additional partnership
(3, 1, 2, 92, 2),   -- Additional partnership
(5, 1, 2, 78, 2),   -- Additional partnership
(7, 1, 2, 105, 2),  -- Additional partnership
(9, 1, 2, 68, 2),   -- Additional partnership
(11, 1, 2, 95, 2),  -- Additional partnership

-- Smith & Maxwell partnerships (5 partnerships)
(2, 7, 9, 65, 3),   -- Additional partnership
(4, 7, 9, 72, 3),   -- Additional partnership
(6, 7, 9, 88, 3),   -- Additional partnership
(8, 7, 9, 55, 3),   -- Additional partnership
(10, 7, 9, 92, 3),  -- Additional partnership

-- Root & Stokes partnerships (5 partnerships)
(12, 13, 14, 75, 4),  -- Additional partnership
(14, 13, 14, 82, 4),  -- Additional partnership
(16, 13, 14, 68, 4),  -- Additional partnership
(18, 13, 14, 95, 4),  -- Additional partnership
(20, 13, 14, 58, 4),  -- Additional partnership

-- Williamson & Taylor partnerships (5 partnerships) - Adding a new player pair
(21, 10, 22, 85, 3),  -- New partnership
(23, 10, 22, 72, 3),  -- New partnership
(25, 10, 22, 95, 3),  -- New partnership
(27, 10, 22, 63, 3),  -- New partnership
(29, 10, 22, 88, 3);  -- New partnership
-- Insert player aggregates (comprehensive career statistics)
INSERT INTO player_aggregates (player_id, format, matches, innings, runs, high_score, avg, strike_rate, hundreds, fifties, wickets, bowling_avg, economy, catches, stumpings) VALUES
-- Virat Kohli - All formats
(1, 'ODI', 275, 265, 12898, 183, 57.38, 93.62, 50, 68, 5, 166.20, 6.23, 143, 0),
(1, 'Test', 113, 191, 8848, 254, 49.15, 55.23, 29, 30, 0, NULL, 4.12, 110, 0),
(1, 'T20', 115, 107, 4008, 122, 52.73, 137.96, 1, 37, 4, 51.25, 8.12, 50, 0),

-- Rohit Sharma
(2, 'ODI', 262, 254, 10709, 264, 49.12, 90.55, 31, 55, 8, 39.12, 5.34, 93, 0),
(2, 'Test', 98, 167, 6789, 212, 45.26, 60.12, 18, 32, 2, 112.50, 4.78, 85, 0),
(2, 'T20', 148, 140, 3854, 118, 32.12, 140.23, 4, 29, 1, 145.00, 9.12, 67, 0),

-- Jasprit Bumrah (bowler)
(3, 'ODI', 89, 35, 150, 16, 8.33, 75.00, 0, 0, 141, 22.47, 4.92, 25, 0),
(3, 'Test', 64, 42, 189, 34, 9.45, 45.12, 0, 0, 267, 21.89, 2.89, 18, 0),
(3, 'T20', 62, 15, 45, 12, 5.63, 85.71, 0, 0, 74, 19.87, 7.12, 12, 0),

-- All-rounders for Question 9
(4, 'ODI', 175, 145, 2567, 87, 32.09, 85.45, 0, 13, 189, 34.56, 4.89, 78, 0),
(4, 'Test', 67, 112, 2689, 100, 32.45, 52.34, 3, 18, 267, 24.56, 2.98, 45, 0),

(9, 'ODI', 136, 118, 3890, 108, 35.36, 125.45, 2, 24, 72, 38.45, 5.67, 78, 0),
(9, 'Test', 98, 167, 3456, 104, 28.45, 65.78, 1, 22, 45, 45.67, 3.45, 56, 0),

(14, 'ODI', 155, 143, 5450, 164, 44.31, 87.45, 12, 35, 28, 42.36, 5.12, 105, 0),
(14, 'Test', 112, 198, 8456, 215, 48.89, 54.67, 25, 42, 12, 56.78, 3.89, 89, 0),

-- Wicket-keepers
(5, 'ODI', 98, 85, 2345, 125, 32.45, 95.67, 5, 15, 0, NULL, NULL, 120, 15),
(12, 'ODI', 145, 132, 3789, 152, 34.56, 92.34, 8, 25, 0, NULL, NULL, 156, 28),

-- Other players
(7, 'ODI', 155, 143, 5450, 164, 44.31, 87.45, 12, 35, 28, 42.36, 5.12, 105, 0),
(8, 'ODI', 145, 132, 3456, 102, 32.45, 95.67, 5, 22, 189, 28.45, 4.56, 67, 0),
(13, 'T20', 98, 89, 2456, 116, 32.45, 145.67, 2, 18, 0, NULL, NULL, 45, 12);