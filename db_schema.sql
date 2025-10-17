
-- db_schema.sql

CREATE TABLE teams (
  team_id SERIAL PRIMARY KEY,
  name TEXT NOT NULL,
  country TEXT,
  short_name TEXT, 
  logo_url TEXT 
);

CREATE TABLE venues (
  venue_id SERIAL PRIMARY KEY,
  name TEXT NOT NULL,
  city TEXT,
  country TEXT,
  capacity INTEGER,
  established INTEGER 
);

CREATE TABLE series (
  series_id SERIAL PRIMARY KEY,
  name TEXT NOT NULL,
  host_country TEXT,
  format TEXT, -- 'Test','ODI','T20'
  start_date DATE,
  planned_matches INTEGER
);

CREATE TABLE matches (
  match_id SERIAL PRIMARY KEY,
  series_id INTEGER REFERENCES series(series_id),
  description TEXT, -- e.g. "IND vs AUS, 2nd ODI"
  date DATE,
  venue_id INTEGER REFERENCES venues(venue_id),
  home_team_id INTEGER REFERENCES teams(team_id),
  away_team_id INTEGER REFERENCES teams(team_id),
  winner_team_id INTEGER REFERENCES teams(team_id),
  toss_winner_id INTEGER REFERENCES teams(team_id),
  toss_decision TEXT, -- 'bat'/'bowl'
  victory_type TEXT, -- 'runs'/'wickets' or NULL
  victory_margin INTEGER, -- number of runs or wickets
  status TEXT -- 'upcoming','live','completed'
);

CREATE TABLE players (
  player_id SERIAL PRIMARY KEY,
  full_name TEXT NOT NULL,
  short_name TEXT,
  team_id INTEGER REFERENCES teams(team_id),
  country TEXT,
  role TEXT, -- 'Batsman','Bowler','All-rounder','Wicket-keeper'
  batting_style TEXT,
  bowling_style TEXT,
  dob DATE
);

-- Each innings record per match
CREATE TABLE innings (
  innings_id SERIAL PRIMARY KEY,
  match_id INTEGER REFERENCES matches(match_id),
  batting_team_id INTEGER REFERENCES teams(team_id),
  bowling_team_id INTEGER REFERENCES teams(team_id),
  innings_no INTEGER, -- 1 or 2 (or 3/4 for Tests)
  total_runs INTEGER,
  wickets INTEGER,
  overs REAL
);

CREATE TABLE batting (
  batting_id SERIAL PRIMARY KEY,
  innings_id INTEGER REFERENCES innings(innings_id),
  player_id INTEGER REFERENCES players(player_id),
  runs INTEGER,
  balls INTEGER,
  fours INTEGER,
  sixes INTEGER,
  dismissal TEXT, -- 'bowled','caught', etc.
  batting_position INTEGER,
  strike_rate REAL
);

CREATE TABLE bowling (
  bowling_id SERIAL PRIMARY KEY,
  innings_id INTEGER REFERENCES innings(innings_id),
  player_id INTEGER REFERENCES players(player_id),
  overs REAL,
  maidens INTEGER,
  runs INTEGER,
  wickets INTEGER,
  economy REAL
);

CREATE TABLE partnerships (
  partnership_id SERIAL PRIMARY KEY,
  innings_id INTEGER REFERENCES innings(innings_id),
  player_a INTEGER REFERENCES players(player_id),
  player_b INTEGER REFERENCES players(player_id),
  runs INTEGER,
  wicket_number INTEGER
);

-- player_aggregates holds aggregated career and format-specific numbers:
CREATE TABLE player_aggregates (
  id SERIAL PRIMARY KEY,
  player_id INTEGER REFERENCES players(player_id),
  format TEXT, -- 'Test','ODI','T20'
  matches INTEGER,
  innings INTEGER,
  runs INTEGER,
  high_score INTEGER,
  avg REAL,
  strike_rate REAL,
  hundreds INTEGER,
  fifties INTEGER,
  wickets INTEGER,
  bowling_avg REAL,
  economy REAL,
  catches INTEGER,
  stumpings INTEGER
);
