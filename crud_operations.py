# pages/crud_operations.py
import streamlit as st
import pandas as pd
from utils.db_connection import get_db_session
from sqlalchemy import text
from datetime import datetime
import io

def run_query(sql, params=None):
    """Execute a SQL query and return results as DataFrame"""
    try:
        with get_db_session() as session:
            result = session.execute(text(sql), params or {})
            cols = result.keys()
            rows = result.fetchall()
        return pd.DataFrame(rows, columns=cols)
    except Exception as e:
        st.error(f"Database query error: {str(e)}")
        return pd.DataFrame()

def run_execute(sql, params=None):
    """Execute a SQL statement and commit changes"""
    try:
        with get_db_session() as session:
            result = session.execute(text(sql), params or {})
            session.commit()
        return result
    except Exception as e:
        st.error(f"Database execution error: {str(e)}")
        raise e

def get_teams():
    """Get teams for dropdowns"""
    return run_query("SELECT team_id, name FROM teams ORDER BY name")

def get_players():
    """Get players for dropdowns"""
    return run_query("SELECT player_id, full_name FROM players ORDER BY full_name")

def get_venues():
    """Get venues for dropdowns"""
    return run_query("SELECT venue_id, name FROM venues ORDER BY name")

def get_series():
    """Get series for dropdowns"""
    return run_query("SELECT series_id, name FROM series ORDER BY name")

def get_innings():
    """Get innings for dropdowns"""
    return run_query("""
        SELECT i.innings_id, m.description as match_info, t.name as team_name 
        FROM innings i 
        JOIN matches m ON i.match_id = m.match_id 
        JOIN teams t ON i.batting_team_id = t.team_id 
        ORDER BY i.innings_id DESC 
        LIMIT 100
    """)

def get_matches():
    """Get matches for dropdowns"""
    return run_query("SELECT match_id, description FROM matches ORDER BY date DESC LIMIT 100")

def show():
    st.title("🏏 Cricket Database Admin Panel")
    st.write("Manage Players, Matches & Statistics with full Create, Read, Update, Delete operations.")

    # Entity selection
    entity_type = st.radio(
        "Select Entity", 
        ["Players", "Matches", "Batting Stats", "Bowling Stats", "Teams", "Venues"], 
        horizontal=True
    )
    
    # Operation selection
    mode = st.radio("Operation", ["Create", "Read", "Update", "Delete"], horizontal=True)

    # PLAYERS CRUD (already improved)
    if entity_type == "Players":
        if mode == "Create":
            st.subheader("➕ Create New Player")
            with st.form("create_player_form"):
                col1, col2 = st.columns(2)
                
                with col1:
                    full_name = st.text_input("Full Name*", placeholder="Virat Kohli")
                    short_name = st.text_input("Short Name", placeholder="V Kohli")
                    
                    teams_df = get_teams()
                    if not teams_df.empty:
                        team_options = {row['name']: row['team_id'] for _, row in teams_df.iterrows()}
                        team_name = st.selectbox("Team*", options=[""] + list(team_options.keys()))
                        team_id = team_options.get(team_name) if team_name else None
                    else:
                        st.warning("No teams available. Please create teams first.")
                        team_id = None
                    
                    country = st.text_input("Country*", placeholder="India")
                
                with col2:
                    role = st.selectbox("Role*", ["", "Batsman", "Bowler", "All-rounder", "Wicket-keeper"])
                    batting_style = st.selectbox("Batting Style", ["", "Right-handed", "Left-handed"])
                    bowling_style = st.selectbox("Bowling Style", ["", "Right-arm fast", "Right-arm medium", "Right-arm offbreak", 
                                                                  "Right-arm legbreak", "Left-arm fast", "Left-arm medium", 
                                                                  "Left-arm orthodox", "Left-arm chinaman"])
                    dob = st.date_input("Date of Birth", value=None, max_value=datetime.now().date())
                
                submitted = st.form_submit_button("Create Player")
                if submitted:
                    if not all([full_name, team_id, country, role]):
                        st.error("Please fill all required fields (*)")
                    else:
                        try:
                            run_execute("""
                                INSERT INTO players (full_name, short_name, team_id, country, role, batting_style, bowling_style, dob)
                                VALUES (:name, :short_name, :team_id, :country, :role, :batting_style, :bowling_style, :dob)
                            """, {
                                "name": full_name.strip(),
                                "short_name": short_name.strip() if short_name else None,
                                "team_id": team_id,
                                "country": country.strip(),
                                "role": role,
                                "batting_style": batting_style or None,
                                "bowling_style": bowling_style or None,
                                "dob": dob
                            })
                            st.success("✅ Player created successfully!")
                            st.rerun()
                        except Exception as e:
                            st.error(f"❌ Error creating player: {str(e)}")
        
        elif mode == "Read":
            st.subheader("👥 View Players")
            
            col1, col2, col3 = st.columns(3)
            with col1:
                search_term = st.text_input("Search players", placeholder="Search by name or country")
            with col2:
                teams_df = get_teams()
                team_options = ["All"] + teams_df['name'].tolist() if not teams_df.empty else ["All"]
                team_filter = st.selectbox("Filter by Team", team_options)
            with col3:
                role_filter = st.selectbox("Filter by Role", ["All", "Batsman", "Bowler", "All-rounder", "Wicket-keeper"])
            
            query = """
                SELECT p.player_id, p.full_name, p.short_name, p.country, p.role, 
                       p.batting_style, p.bowling_style, p.dob, t.name as team_name 
                FROM players p LEFT JOIN teams t ON p.team_id = t.team_id
            """
            params = {}
            
            conditions = []
            if search_term:
                conditions.append("(LOWER(p.full_name) LIKE LOWER(:search) OR LOWER(p.country) LIKE LOWER(:search))")
                params["search"] = f"%{search_term}%"
            if team_filter != "All":
                conditions.append("t.name = :team")
                params["team"] = team_filter
            if role_filter != "All":
                conditions.append("p.role = :role")
                params["role"] = role_filter
            
            if conditions:
                query += " WHERE " + " AND ".join(conditions)
            
            query += " ORDER BY p.full_name LIMIT 200"
            
            df = run_query(query, params)
            
            if not df.empty:
                st.dataframe(df, use_container_width=True)
                
                col1, col2 = st.columns(2)
                with col1:
                    csv = df.to_csv(index=False)
                    st.download_button("📥 Export to CSV", csv, "players.csv", "text/csv")
                with col2:
                    buffer = io.BytesIO()
                    with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
                        df.to_excel(writer, index=False, sheet_name='Players')
                        writer.close()
                    st.download_button("📊 Export to Excel", buffer.getvalue(), "players.xlsx",
                                     "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
            else:
                st.info("No players found matching the criteria")
        
        elif mode == "Update":
            st.subheader("✏️ Update Player")
            
            players_df = get_players()
            if players_df.empty:
                st.info("No players available to update")
                return
                
            player_options = {f"{row['full_name']} (ID: {row['player_id']})": row['player_id'] 
                            for _, row in players_df.iterrows()}
            selected_player = st.selectbox("Select Player to Update", options=list(player_options.keys()))
            pid = player_options[selected_player]
            
            player_data = run_query("""
                SELECT p.*, t.name as team_name 
                FROM players p LEFT JOIN teams t ON p.team_id = t.team_id 
                WHERE p.player_id = :pid
            """, {"pid": pid})
            
            if player_data.empty:
                st.error("Player not found")
                return
                
            player_data = player_data.iloc[0]
            
            with st.form("update_player_form"):
                col1, col2 = st.columns(2)
                
                with col1:
                    full_name = st.text_input("Full Name*", value=player_data['full_name'])
                    short_name = st.text_input("Short Name", value=player_data['short_name'] or "")
                    
                    teams_df = get_teams()
                    current_team_name = player_data.get('team_name', '')
                    team_options = {row['name']: row['team_id'] for _, row in teams_df.iterrows()}
                    team_name = st.selectbox("Team*", 
                                           options=list(team_options.keys()),
                                           index=list(team_options.keys()).index(current_team_name) 
                                           if current_team_name in team_options else 0)
                    team_id = team_options[team_name]
                    
                    country = st.text_input("Country*", value=player_data['country'])
                
                with col2:
                    role = st.selectbox("Role*", ["Batsman", "Bowler", "All-rounder", "Wicket-keeper"], 
                                      index=["Batsman", "Bowler", "All-rounder", "Wicket-keeper"].index(player_data['role']) 
                                      if player_data['role'] in ["Batsman", "Bowler", "All-rounder", "Wicket-keeper"] else 0)
                    
                    batting_options = ["", "Right-handed", "Left-handed"]
                    batting_index = batting_options.index(player_data['batting_style']) if player_data['batting_style'] in batting_options else 0
                    batting_style = st.selectbox("Batting Style", batting_options, index=batting_index)
                    
                    bowling_style = st.text_input("Bowling Style", value=player_data['bowling_style'] or "")
                    dob = st.date_input("Date of Birth", 
                                      value=player_data['dob'] if player_data['dob'] else datetime.now().date(),
                                      max_value=datetime.now().date())
                
                submitted = st.form_submit_button("Update Player")
                if submitted:
                    if not all([full_name, team_id, country, role]):
                        st.error("Please fill all required fields (*)")
                    else:
                        try:
                            run_execute("""
                                UPDATE players SET 
                                    full_name = :name, short_name = :short_name, team_id = :team_id, 
                                    country = :country, role = :role, batting_style = :batting_style, 
                                    bowling_style = :bowling_style, dob = :dob
                                WHERE player_id = :pid
                            """, {
                                "name": full_name.strip(),
                                "short_name": short_name.strip() or None,
                                "team_id": team_id,
                                "country": country.strip(),
                                "role": role,
                                "batting_style": batting_style or None,
                                "bowling_style": bowling_style.strip() if bowling_style else None,
                                "dob": dob,
                                "pid": pid
                            })
                            st.success("✅ Player updated successfully!")
                            st.rerun()
                        except Exception as e:
                            st.error(f"❌ Error updating player: {str(e)}")
        
        elif mode == "Delete":
            st.subheader("🗑️ Delete Player")
            st.warning("⚠️ This action cannot be undone. Please be careful!")
            
            players_df = get_players()
            if players_df.empty:
                st.info("No players available to delete")
                return
                
            player_options = {f"{row['full_name']} (ID: {row['player_id']})": row['player_id'] 
                            for _, row in players_df.iterrows()}
            selected_player = st.selectbox("Select Player to Delete", options=list(player_options.keys()))
            pid = player_options[selected_player]
            
            player_info = run_query("""
                SELECT p.*, t.name as team_name 
                FROM players p LEFT JOIN teams t ON p.team_id = t.team_id 
                WHERE p.player_id = :pid
            """, {"pid": pid})
            
            if not player_info.empty:
                st.write("**Player Details:**")
                st.dataframe(player_info, use_container_width=True)
                
                batting_records = run_query("SELECT COUNT(*) as count FROM batting WHERE player_id = :pid", {"pid": pid})
                bowling_records = run_query("SELECT COUNT(*) as count FROM bowling WHERE player_id = :pid", {"pid": pid})
                
                if batting_records.iloc[0]['count'] > 0 or bowling_records.iloc[0]['count'] > 0:
                    st.warning(f"⚠️ This player has {batting_records.iloc[0]['count']} batting records and {bowling_records.iloc[0]['count']} bowling records. Deleting will remove these associated records.")
                
                if st.button("🚨 Confirm Delete", type="secondary"):
                    try:
                        run_execute("DELETE FROM batting WHERE player_id = :pid", {"pid": pid})
                        run_execute("DELETE FROM bowling WHERE player_id = :pid", {"pid": pid})
                        run_execute("DELETE FROM players WHERE player_id = :pid", {"pid": pid})
                        st.success("✅ Player and associated records deleted successfully!")
                        st.rerun()
                    except Exception as e:
                        st.error(f"❌ Error deleting player: {str(e)}")

    # MATCHES CRUD
    elif entity_type == "Matches":
        if mode == "Create":
            st.subheader("➕ Create New Match")
            with st.form("create_match_form"):
                col1, col2 = st.columns(2)
                
                with col1:
                    series_df = get_series()
                    if not series_df.empty:
                        series_options = {row['name']: row['series_id'] for _, row in series_df.iterrows()}
                        series_name = st.selectbox("Series", options=[""] + list(series_options.keys()))
                        series_id = series_options.get(series_name) if series_name else None
                    else:
                        series_id = st.number_input("Series ID", min_value=1, step=1, value=1)
                    
                    description = st.text_input("Description*", placeholder="IND vs AUS, 1st Test")
                    match_date = st.date_input("Match Date*", value=datetime.now().date())
                    
                    venues_df = get_venues()
                    if not venues_df.empty:
                        venue_options = {row['name']: row['venue_id'] for _, row in venues_df.iterrows()}
                        venue_name = st.selectbox("Venue", options=[""] + list(venue_options.keys()))
                        venue_id = venue_options.get(venue_name) if venue_name else None
                    else:
                        venue_id = st.number_input("Venue ID", min_value=1, step=1, value=1)
                
                with col2:
                    teams_df = get_teams()
                    if not teams_df.empty:
                        team_options = {row['name']: row['team_id'] for _, row in teams_df.iterrows()}
                        home_team = st.selectbox("Home Team*", options=list(team_options.keys()))
                        away_team_options = [t for t in team_options.keys() if t != home_team]
                        away_team = st.selectbox("Away Team*", options=away_team_options) if away_team_options else st.selectbox("Away Team*", options=list(team_options.keys()))
                        home_team_id = team_options[home_team]
                        away_team_id = team_options[away_team]
                    else:
                        st.warning("No teams available. Please create teams first.")
                        home_team_id = st.number_input("Home Team ID*", min_value=1, step=1, value=1)
                        away_team_id = st.number_input("Away Team ID*", min_value=1, step=1, value=2)
                    
                    status = st.selectbox("Status", ["upcoming", "live", "completed"])
                    
                    if status == "completed" and not teams_df.empty:
                        winner_options = ["", home_team, away_team, "Draw/No Result"]
                        winner_team = st.selectbox("Winner Team", options=winner_options)
                        winner_team_id = team_options.get(winner_team) if winner_team and winner_team != "Draw/No Result" else None
                    else:
                        winner_team_id = None
                
                submitted = st.form_submit_button("Create Match")
                if submitted:
                    if not all([description, match_date, home_team_id, away_team_id]):
                        st.error("Please fill all required fields (*)")
                    elif home_team_id == away_team_id:
                        st.error("Home team and Away team cannot be the same")
                    else:
                        try:
                            run_execute("""
                                INSERT INTO matches (series_id, description, date, venue_id, home_team_id, away_team_id, status, winner_team_id)
                                VALUES (:series_id, :description, :date, :venue_id, :home_team_id, :away_team_id, :status, :winner_team_id)
                            """, {
                                "series_id": series_id,
                                "description": description.strip(),
                                "date": match_date,
                                "venue_id": venue_id,
                                "home_team_id": home_team_id,
                                "away_team_id": away_team_id,
                                "status": status,
                                "winner_team_id": winner_team_id
                            })
                            st.success("✅ Match created successfully!")
                            st.rerun()
                        except Exception as e:
                            st.error(f"❌ Error creating match: {str(e)}")
        
        elif mode == "Read":
            st.subheader("📊 View Matches")
            
            col1, col2 = st.columns(2)
            with col1:
                search_term = st.text_input("Search matches", placeholder="Search by description or teams")
            with col2:
                status_filter = st.selectbox("Filter by Status", ["All", "upcoming", "live", "completed"])
            
            df = run_query("""
                SELECT m.match_id, m.description, m.date, m.status,
                       s.name as series_name, v.name as venue_name,
                       ht.name as home_team, at.name as away_team,
                       wt.name as winner
                FROM matches m
                LEFT JOIN series s ON m.series_id = s.series_id
                LEFT JOIN venues v ON m.venue_id = v.venue_id
                LEFT JOIN teams ht ON m.home_team_id = ht.team_id
                LEFT JOIN teams at ON m.away_team_id = at.team_id
                LEFT JOIN teams wt ON m.winner_team_id = wt.team_id
                ORDER BY m.date DESC LIMIT 200
            """)
            
            if not df.empty:
                if search_term:
                    df = df[df.apply(lambda row: search_term.lower() in str(row).lower(), axis=1)]
                if status_filter != "All":
                    df = df[df['status'] == status_filter]
                
                st.dataframe(df, use_container_width=True)
                
                col1, col2 = st.columns(2)
                with col1:
                    csv = df.to_csv(index=False)
                    st.download_button("📥 Export to CSV", csv, "matches.csv", "text/csv")
                with col2:
                    buffer = io.BytesIO()
                    with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
                        df.to_excel(writer, index=False, sheet_name='Matches')
                        writer.close()
                    st.download_button("📊 Export to Excel", buffer.getvalue(), "matches.xlsx",
                                     "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
            else:
                st.info("No matches found")
        
        elif mode == "Update":
            st.subheader("✏️ Update Match")
            
            matches_df = get_matches()
            if matches_df.empty:
                st.info("No matches available to update")
                return
                
            match_options = {f"{row['description']} (ID: {row['match_id']})": row['match_id'] for _, row in matches_df.iterrows()}
            selected_match = st.selectbox("Select Match to Update", options=list(match_options.keys()))
            match_id = match_options[selected_match]
            
            match_data = run_query("""
                SELECT m.*, s.name as series_name, v.name as venue_name,
                       ht.name as home_team, at.name as away_team, wt.name as winner_team
                FROM matches m
                LEFT JOIN series s ON m.series_id = s.series_id
                LEFT JOIN venues v ON m.venue_id = v.venue_id
                LEFT JOIN teams ht ON m.home_team_id = ht.team_id
                LEFT JOIN teams at ON m.away_team_id = at.team_id
                LEFT JOIN teams wt ON m.winner_team_id = wt.team_id
                WHERE m.match_id = :match_id
            """, {"match_id": match_id})
            
            if match_data.empty:
                st.error("Match not found")
                return
                
            match_data = match_data.iloc[0]
            
            with st.form("update_match_form"):
                col1, col2 = st.columns(2)
                
                with col1:
                    series_df = get_series()
                    current_series = match_data.get('series_name', '')
                    series_options = {row['name']: row['series_id'] for _, row in series_df.iterrows()}
                    series_name = st.selectbox("Series", options=[""] + list(series_options.keys()),
                                            index=list(series_options.keys()).index(current_series) + 1 
                                            if current_series in series_options else 0)
                    series_id = series_options.get(series_name) if series_name else None
                    
                    description = st.text_input("Description*", value=match_data['description'])
                    match_date = st.date_input("Match Date*", value=match_data['date'])
                    
                    venues_df = get_venues()
                    current_venue = match_data.get('venue_name', '')
                    venue_options = {row['name']: row['venue_id'] for _, row in venues_df.iterrows()}
                    venue_name = st.selectbox("Venue", options=[""] + list(venue_options.keys()),
                                           index=list(venue_options.keys()).index(current_venue) + 1 
                                           if current_venue in venue_options else 0)
                    venue_id = venue_options.get(venue_name) if venue_name else None
                
                with col2:
                    teams_df = get_teams()
                    current_home_team = match_data.get('home_team', '')
                    current_away_team = match_data.get('away_team', '')
                    team_options = {row['name']: row['team_id'] for _, row in teams_df.iterrows()}
                    
                    home_team = st.selectbox("Home Team*", options=list(team_options.keys()),
                                           index=list(team_options.keys()).index(current_home_team) 
                                           if current_home_team in team_options else 0)
                    away_team_options = [t for t in team_options.keys() if t != home_team]
                    away_team = st.selectbox("Away Team*", options=away_team_options,
                                           index=away_team_options.index(current_away_team) 
                                           if current_away_team in away_team_options else 0)
                    
                    home_team_id = team_options[home_team]
                    away_team_id = team_options[away_team]
                    
                    status = st.selectbox("Status", ["upcoming", "live", "completed"],
                                        index=["upcoming", "live", "completed"].index(match_data['status']))
                    
                    if status == "completed":
                        current_winner = match_data.get('winner_team', '')
                        winner_options = ["", home_team, away_team, "Draw/No Result"]
                        winner_index = winner_options.index(current_winner) if current_winner in winner_options else 0
                        winner_team = st.selectbox("Winner Team", options=winner_options, index=winner_index)
                        winner_team_id = team_options.get(winner_team) if winner_team and winner_team != "Draw/No Result" else None
                    else:
                        winner_team_id = None
                
                submitted = st.form_submit_button("Update Match")
                if submitted:
                    if not all([description, match_date, home_team_id, away_team_id]):
                        st.error("Please fill all required fields (*)")
                    elif home_team_id == away_team_id:
                        st.error("Home team and Away team cannot be the same")
                    else:
                        try:
                            run_execute("""
                                UPDATE matches SET 
                                    series_id = :series_id, description = :description, date = :date, 
                                    venue_id = :venue_id, home_team_id = :home_team_id, 
                                    away_team_id = :away_team_id, status = :status, winner_team_id = :winner_team_id
                                WHERE match_id = :match_id
                            """, {
                                "series_id": series_id,
                                "description": description.strip(),
                                "date": match_date,
                                "venue_id": venue_id,
                                "home_team_id": home_team_id,
                                "away_team_id": away_team_id,
                                "status": status,
                                "winner_team_id": winner_team_id,
                                "match_id": match_id
                            })
                            st.success("✅ Match updated successfully!")
                            st.rerun()
                        except Exception as e:
                            st.error(f"❌ Error updating match: {str(e)}")
        
        elif mode == "Delete":
            st.subheader("🗑️ Delete Match")
            st.warning("⚠️ This action cannot be undone. Please be careful!")
            
            matches_df = get_matches()
            if matches_df.empty:
                st.info("No matches available to delete")
                return
                
            match_options = {f"{row['description']} (ID: {row['match_id']})": row['match_id'] for _, row in matches_df.iterrows()}
            selected_match = st.selectbox("Select Match to Delete", options=list(match_options.keys()))
            match_id = match_options[selected_match]
            
            match_info = run_query("""
                SELECT m.*, ht.name as home_team, at.name as away_team, v.name as venue_name
                FROM matches m
                LEFT JOIN teams ht ON m.home_team_id = ht.team_id
                LEFT JOIN teams at ON m.away_team_id = at.team_id
                LEFT JOIN venues v ON m.venue_id = v.venue_id
                WHERE m.match_id = :match_id
            """, {"match_id": match_id})
            
            if not match_info.empty:
                st.write("**Match Details:**")
                st.dataframe(match_info, use_container_width=True)
                
                innings_count = run_query("SELECT COUNT(*) as count FROM innings WHERE match_id = :match_id", {"match_id": match_id})
                
                if innings_count.iloc[0]['count'] > 0:
                    st.warning(f"⚠️ This match has {innings_count.iloc[0]['count']} innings records. Deleting will remove all associated data.")
                
                if st.button("🚨 Confirm Delete", type="secondary"):
                    try:
                        run_execute("DELETE FROM batting WHERE innings_id IN (SELECT innings_id FROM innings WHERE match_id = :match_id)", {"match_id": match_id})
                        run_execute("DELETE FROM bowling WHERE innings_id IN (SELECT innings_id FROM innings WHERE match_id = :match_id)", {"match_id": match_id})
                        run_execute("DELETE FROM innings WHERE match_id = :match_id", {"match_id": match_id})
                        run_execute("DELETE FROM matches WHERE match_id = :match_id", {"match_id": match_id})
                        st.success("✅ Match and all associated records deleted successfully!")
                        st.rerun()
                    except Exception as e:
                        st.error(f"❌ Error deleting match: {str(e)}")

    # BATTING STATS CRUD
    elif entity_type == "Batting Stats":
        if mode == "Create":
            st.subheader("➕ Add Batting Statistics")
            with st.form("create_batting_form"):
                col1, col2 = st.columns(2)
                
                with col1:
                    innings_df = get_innings()
                    if not innings_df.empty:
                        innings_options = {f"{row['match_info']} - {row['team_name']}": row['innings_id'] for _, row in innings_df.iterrows()}
                        innings_desc = st.selectbox("Innings*", options=[""] + list(innings_options.keys()))
                        innings_id = innings_options.get(innings_desc) if innings_desc else None
                    else:
                        st.warning("No innings available. Please create matches and innings first.")
                        innings_id = st.number_input("Innings ID*", min_value=1, step=1, value=1)
                    
                    players_df = get_players()
                    if not players_df.empty:
                        player_options = {row['full_name']: row['player_id'] for _, row in players_df.iterrows()}
                        player_name = st.selectbox("Player*", options=[""] + list(player_options.keys()))
                        player_id = player_options.get(player_name) if player_name else None
                    else:
                        st.warning("No players available. Please create players first.")
                        player_id = st.number_input("Player ID*", min_value=1, step=1, value=1)
                    
                    runs = st.number_input("Runs", min_value=0, value=0)
                    balls = st.number_input("Balls", min_value=0, value=0)
                    fours = st.number_input("Fours", min_value=0, value=0)
                
                with col2:
                    sixes = st.number_input("Sixes", min_value=0, value=0)
                    dismissal = st.text_input("Dismissal", placeholder="caught Smith b Starc")
                    batting_position = st.number_input("Batting Position", min_value=1, max_value=11, value=1)
                    strike_rate = st.number_input("Strike Rate", min_value=0.0, value=0.0, format="%.2f",
                                               help="Will be auto-calculated if runs and balls are provided")
                
                # Auto-calculate strike rate
                if runs > 0 and balls > 0 and strike_rate == 0:
                    strike_rate = round((runs / balls) * 100, 2)
                    st.info(f"Auto-calculated Strike Rate: {strike_rate}")
                
                submitted = st.form_submit_button("Add Batting Stats")
                if submitted:
                    if not all([innings_id, player_id]):
                        st.error("Please fill all required fields (*)")
                    else:
                        try:
                            # Use calculated strike rate if not provided
                            final_strike_rate = strike_rate
                            if runs > 0 and balls > 0 and strike_rate == 0:
                                final_strike_rate = round((runs / balls) * 100, 2)
                            
                            run_execute("""
                                INSERT INTO batting (innings_id, player_id, runs, balls, fours, sixes, dismissal, batting_position, strike_rate)
                                VALUES (:innings_id, :player_id, :runs, :balls, :fours, :sixes, :dismissal, :batting_position, :strike_rate)
                            """, {
                                "innings_id": innings_id,
                                "player_id": player_id,
                                "runs": runs,
                                "balls": balls,
                                "fours": fours,
                                "sixes": sixes,
                                "dismissal": dismissal.strip() if dismissal else None,
                                "batting_position": batting_position,
                                "strike_rate": final_strike_rate
                            })
                            st.success("✅ Batting statistics added successfully!")
                            st.rerun()
                        except Exception as e:
                            st.error(f"❌ Error adding batting stats: {str(e)}")
        
        elif mode == "Read":
            st.subheader("📊 View Batting Statistics")
            
            col1, col2 = st.columns(2)
            with col1:
                search_term = st.text_input("Search batting records", placeholder="Search by player name")
            with col2:
                min_runs = st.number_input("Minimum Runs", min_value=0, value=0)
            
            df = run_query("""
                SELECT b.*, p.full_name as player_name, i.match_id, t.name as team_name,
                       m.description as match_description
                FROM batting b
                JOIN players p ON b.player_id = p.player_id
                JOIN innings i ON b.innings_id = i.innings_id
                JOIN matches m ON i.match_id = m.match_id
                JOIN teams t ON p.team_id = t.team_id
                ORDER BY b.runs DESC LIMIT 200
            """)
            
            if not df.empty:
                if search_term:
                    df = df[df.apply(lambda row: search_term.lower() in str(row).lower(), axis=1)]
                if min_runs > 0:
                    df = df[df['runs'] >= min_runs]
                
                st.dataframe(df, use_container_width=True)
                
                col1, col2 = st.columns(2)
                with col1:
                    csv = df.to_csv(index=False)
                    st.download_button("📥 Export to CSV", csv, "batting_stats.csv", "text/csv")
                with col2:
                    buffer = io.BytesIO()
                    with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
                        df.to_excel(writer, index=False, sheet_name='Batting Stats')
                        writer.close()
                    st.download_button("📊 Export to Excel", buffer.getvalue(), "batting_stats.xlsx",
                                     "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
            else:
                st.info("No batting statistics found")
        
        elif mode == "Update":
            st.subheader("✏️ Update Batting Statistics")
            
            batting_df = run_query("""
                SELECT b.batting_id, p.full_name, b.runs, b.innings_id, m.description as match_info
                FROM batting b
                JOIN players p ON b.player_id = p.player_id
                JOIN innings i ON b.innings_id = i.innings_id
                JOIN matches m ON i.match_id = m.match_id
                ORDER BY b.batting_id DESC LIMIT 100
            """)
            
            if batting_df.empty:
                st.info("No batting statistics available to update")
                return
                
            batting_options = {f"{row['full_name']} - {row['runs']} runs (Match: {row['match_info']})": row['batting_id'] 
                             for _, row in batting_df.iterrows()}
            selected_batting = st.selectbox("Select Batting Record to Update", options=list(batting_options.keys()))
            batting_id = batting_options[selected_batting]
            
            batting_data = run_query("SELECT * FROM batting WHERE batting_id = :batting_id", {"batting_id": batting_id})
            if batting_data.empty:
                st.error("Batting record not found")
                return
                
            batting_data = batting_data.iloc[0]
            
            with st.form("update_batting_form"):
                col1, col2 = st.columns(2)
                
                with col1:
                    runs = st.number_input("Runs", value=int(batting_data['runs']), min_value=0)
                    balls = st.number_input("Balls", value=int(batting_data['balls']), min_value=0)
                    fours = st.number_input("Fours", value=int(batting_data['fours']), min_value=0)
                
                with col2:
                    sixes = st.number_input("Sixes", value=int(batting_data['sixes']), min_value=0)
                    dismissal = st.text_input("Dismissal", value=batting_data['dismissal'] or "")
                    batting_position = st.number_input("Batting Position", value=int(batting_data['batting_position']), 
                                                     min_value=1, max_value=11)
                    strike_rate = st.number_input("Strike Rate", value=float(batting_data['strike_rate']), 
                                               min_value=0.0, format="%.2f")
                
                # Auto-calculate strike rate
                if runs > 0 and balls > 0:
                    calculated_sr = round((runs / balls) * 100, 2)
                    st.info(f"Auto-calculated Strike Rate: {calculated_sr}")
                
                submitted = st.form_submit_button("Update Batting Stats")
                if submitted:
                    try:
                        # Use calculated strike rate if different
                        final_strike_rate = strike_rate
                        if runs > 0 and balls > 0 and abs(strike_rate - (runs/balls*100)) > 1:
                            final_strike_rate = round((runs / balls) * 100, 2)
                            st.info(f"Using calculated strike rate: {final_strike_rate}")
                        
                        run_execute("""
                            UPDATE batting SET 
                                runs = :runs, balls = :balls, fours = :fours, sixes = :sixes,
                                dismissal = :dismissal, batting_position = :batting_position, strike_rate = :strike_rate
                            WHERE batting_id = :batting_id
                        """, {
                            "runs": runs,
                            "balls": balls,
                            "fours": fours,
                            "sixes": sixes,
                            "dismissal": dismissal.strip() if dismissal else None,
                            "batting_position": batting_position,
                            "strike_rate": final_strike_rate,
                            "batting_id": batting_id
                        })
                        st.success("✅ Batting statistics updated successfully!")
                        st.rerun()
                    except Exception as e:
                        st.error(f"❌ Error updating batting stats: {str(e)}")
        
        elif mode == "Delete":
            st.subheader("🗑️ Delete Batting Statistics")
            st.warning("⚠️ This action cannot be undone. Please be careful!")
            
            batting_df = run_query("""
                SELECT b.batting_id, p.full_name, b.runs, m.description as match_info
                FROM batting b
                JOIN players p ON b.player_id = p.player_id
                JOIN innings i ON b.innings_id = i.innings_id
                JOIN matches m ON i.match_id = m.match_id
                ORDER BY b.batting_id DESC LIMIT 100
            """)
            
            if batting_df.empty:
                st.info("No batting statistics available to delete")
                return
                
            batting_options = {f"{row['full_name']} - {row['runs']} runs (Match: {row['match_info']})": row['batting_id'] 
                             for _, row in batting_df.iterrows()}
            selected_batting = st.selectbox("Select Batting Record to Delete", options=list(batting_options.keys()))
            batting_id = batting_options[selected_batting]
            
            batting_info = run_query("""
                SELECT b.*, p.full_name, m.description as match_info
                FROM batting b
                JOIN players p ON b.player_id = p.player_id
                JOIN innings i ON b.innings_id = i.innings_id
                JOIN matches m ON i.match_id = m.match_id
                WHERE b.batting_id = :batting_id
            """, {"batting_id": batting_id})
            
            if not batting_info.empty:
                st.write("**Batting Record Details:**")
                st.dataframe(batting_info, use_container_width=True)
                
                if st.button("🚨 Confirm Delete", type="secondary"):
                    try:
                        run_execute("DELETE FROM batting WHERE batting_id = :batting_id", {"batting_id": batting_id})
                        st.success("✅ Batting record deleted successfully!")
                        st.rerun()
                    except Exception as e:
                        st.error(f"❌ Error deleting batting record: {str(e)}")

    # BOWLING STATS CRUD
    elif entity_type == "Bowling Stats":
        if mode == "Create":
            st.subheader("➕ Add Bowling Statistics")
            with st.form("create_bowling_form"):
                col1, col2 = st.columns(2)
                
                with col1:
                    innings_df = get_innings()
                    if not innings_df.empty:
                        innings_options = {f"{row['match_info']} - {row['team_name']}": row['innings_id'] for _, row in innings_df.iterrows()}
                        innings_desc = st.selectbox("Innings*", options=[""] + list(innings_options.keys()))
                        innings_id = innings_options.get(innings_desc) if innings_desc else None
                    else:
                        st.warning("No innings available. Please create matches and innings first.")
                        innings_id = st.number_input("Innings ID*", min_value=1, step=1, value=1)
                    
                    players_df = get_players()
                    if not players_df.empty:
                        player_options = {row['full_name']: row['player_id'] for _, row in players_df.iterrows()}
                        player_name = st.selectbox("Player*", options=[""] + list(player_options.keys()))
                        player_id = player_options.get(player_name) if player_name else None
                    else:
                        st.warning("No players available. Please create players first.")
                        player_id = st.number_input("Player ID*", min_value=1, step=1, value=1)
                    
                    overs = st.number_input("Overs", min_value=0.0, value=0.0, step=0.1, format="%.1f")
                    maidens = st.number_input("Maidens", min_value=0, value=0)
                    runs = st.number_input("Runs Conceded", min_value=0, value=0)
                
                with col2:
                    wickets = st.number_input("Wickets", min_value=0, value=0)
                    economy = st.number_input("Economy", min_value=0.0, value=0.0, step=0.1, format="%.2f",
                                           help="Will be auto-calculated if overs and runs are provided")
                    dots = st.number_input("Dot Balls", min_value=0, value=0)
                    wides = st.number_input("Wides", min_value=0, value=0)
                    no_balls = st.number_input("No Balls", min_value=0, value=0)
                
                # Auto-calculate economy
                if overs > 0 and runs > 0 and economy == 0:
                    economy = round(runs / overs, 2)
                    st.info(f"Auto-calculated Economy: {economy}")
                
                submitted = st.form_submit_button("Add Bowling Stats")
                if submitted:
                    if not all([innings_id, player_id]):
                        st.error("Please fill all required fields (*)")
                    else:
                        try:
                            # Use calculated economy if not provided
                            final_economy = economy
                            if overs > 0 and runs > 0 and economy == 0:
                                final_economy = round(runs / overs, 2)
                            
                            run_execute("""
                                INSERT INTO bowling (innings_id, player_id, overs, maidens, runs, wickets, economy, dots, wides, no_balls)
                                VALUES (:innings_id, :player_id, :overs, :maidens, :runs, :wickets, :economy, :dots, :wides, :no_balls)
                            """, {
                                "innings_id": innings_id,
                                "player_id": player_id,
                                "overs": overs,
                                "maidens": maidens,
                                "runs": runs,
                                "wickets": wickets,
                                "economy": final_economy,
                                "dots": dots,
                                "wides": wides,
                                "no_balls": no_balls
                            })
                            st.success("✅ Bowling statistics added successfully!")
                            st.rerun()
                        except Exception as e:
                            st.error(f"❌ Error adding bowling stats: {str(e)}")
        
        elif mode == "Read":
            st.subheader("📊 View Bowling Statistics")
            
            col1, col2, col3 = st.columns(3)
            with col1:
                search_term = st.text_input("Search bowling records", placeholder="Search by player name")
            with col2:
                min_wickets = st.number_input("Minimum Wickets", min_value=0, value=0)
            with col3:
                max_economy = st.number_input("Maximum Economy", min_value=0.0, value=100.0, step=0.1)
            
            df = run_query("""
                SELECT b.*, p.full_name as player_name, i.match_id, t.name as team_name,
                       m.description as match_description, m.date as match_date
                FROM bowling b
                JOIN players p ON b.player_id = p.player_id
                JOIN innings i ON b.innings_id = i.innings_id
                JOIN matches m ON i.match_id = m.match_id
                JOIN teams t ON p.team_id = t.team_id
                ORDER BY b.wickets DESC, b.economy ASC LIMIT 200
            """)
            
            if not df.empty:
                if search_term:
                    df = df[df.apply(lambda row: search_term.lower() in str(row).lower(), axis=1)]
                if min_wickets > 0:
                    df = df[df['wickets'] >= min_wickets]
                if max_economy < 100.0:
                    df = df[df['economy'] <= max_economy]
                
                st.dataframe(df, use_container_width=True)
                
                # Display bowling statistics summary
                if not df.empty:
                    total_wickets = df['wickets'].sum()
                    best_bowling = df.loc[df['wickets'].idxmax()]
                    st.metric("Total Wickets Displayed", total_wickets)
                    st.info(f"Best Bowling: {best_bowling['player_name']} - {best_bowling['wickets']}/{best_bowling['runs']}")
                
                col1, col2 = st.columns(2)
                with col1:
                    csv = df.to_csv(index=False)
                    st.download_button("📥 Export to CSV", csv, "bowling_stats.csv", "text/csv")
                with col2:
                    buffer = io.BytesIO()
                    with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
                        df.to_excel(writer, index=False, sheet_name='Bowling Stats')
                        writer.close()
                    st.download_button("📊 Export to Excel", buffer.getvalue(), "bowling_stats.xlsx",
                                     "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
            else:
                st.info("No bowling statistics found")
        
        elif mode == "Update":
            st.subheader("✏️ Update Bowling Statistics")
            
            bowling_df = run_query("""
                SELECT b.bowling_id, p.full_name, b.wickets, b.runs, b.innings_id, m.description as match_info
                FROM bowling b
                JOIN players p ON b.player_id = p.player_id
                JOIN innings i ON b.innings_id = i.innings_id
                JOIN matches m ON i.match_id = m.match_id
                ORDER BY b.bowling_id DESC LIMIT 100
            """)
            
            if bowling_df.empty:
                st.info("No bowling statistics available to update")
                return
                
            bowling_options = {f"{row['full_name']} - {row['wickets']}/{row['runs']} (Match: {row['match_info']})": row['bowling_id'] 
                             for _, row in bowling_df.iterrows()}
            selected_bowling = st.selectbox("Select Bowling Record to Update", options=list(bowling_options.keys()))
            bowling_id = bowling_options[selected_bowling]
            
            bowling_data = run_query("SELECT * FROM bowling WHERE bowling_id = :bowling_id", {"bowling_id": bowling_id})
            if bowling_data.empty:
                st.error("Bowling record not found")
                return
                
            bowling_data = bowling_data.iloc[0]
            
            with st.form("update_bowling_form"):
                col1, col2 = st.columns(2)
                
                with col1:
                    overs = st.number_input("Overs*", value=float(bowling_data['overs']), step=0.1, format="%.1f", min_value=0.0)
                    maidens = st.number_input("Maidens*", value=int(bowling_data['maidens']), min_value=0)
                    runs = st.number_input("Runs Conceded*", value=int(bowling_data['runs']), min_value=0)
                    wickets = st.number_input("Wickets*", value=int(bowling_data['wickets']), min_value=0)
                
                with col2:
                    economy = st.number_input("Economy", value=float(bowling_data['economy']), step=0.1, format="%.2f", min_value=0.0)
                    # Safely get dots value with default
                    dots_value = bowling_data.get('dots', 0) if 'dots' in bowling_data else 0
                    dots = st.number_input("Dot Balls", value=int(dots_value), min_value=0)
                    
                    # Safely get wides value with default
                    wides_value = bowling_data.get('wides', 0) if 'wides' in bowling_data else 0
                    wides = st.number_input("Wides", value=int(wides_value), min_value=0)
                    
                    # Safely get no_balls value with default
                    no_balls_value = bowling_data.get('no_balls', 0) if 'no_balls' in bowling_data else 0
                    no_balls = st.number_input("No Balls", value=int(no_balls_value), min_value=0)
                
                # Auto-calculate and display economy
                if overs > 0 and runs >= 0:
                    calculated_eco = round(runs / overs, 2) if overs > 0 else 0.0
                    st.info(f"Auto-calculated Economy: {calculated_eco}")
                    
                    # Suggest using calculated economy if significantly different
                    if abs(economy - calculated_eco) > 0.1:
                        st.warning(f"Consider using calculated economy: {calculated_eco}")

                submitted = st.form_submit_button("Update Bowling Stats")
                if submitted:
                    if not all([overs >= 0, runs >= 0, wickets >= 0]):
                        st.error("Please fill all required fields (*) with valid values")
                    else:
                        try:
                            # Use calculated economy if it makes sense
                            final_economy = economy
                            if overs > 0 and abs(economy - (runs/overs)) > 0.5:
                                final_economy = round(runs / overs, 2)
                                st.success(f"Using calculated economy: {final_economy}")
                            
                            run_execute("""
                                UPDATE bowling SET 
                                    overs = :overs, maidens = :maidens, runs = :runs,
                                    wickets = :wickets, economy = :economy, dots = :dots,
                                    wides = :wides, no_balls = :no_balls
                                WHERE bowling_id = :bowling_id
                            """, {
                                "overs": overs,
                                "maidens": maidens,
                                "runs": runs,
                                "wickets": wickets,
                                "economy": final_economy,
                                "dots": dots,
                                "wides": wides,
                                "no_balls": no_balls,
                                "bowling_id": bowling_id
                            })
                            st.success("✅ Bowling statistics updated successfully!")
                            st.rerun()
                        except Exception as e:
                            st.error(f"❌ Error updating bowling stats: {str(e)}")
        
        elif mode == "Delete":
            st.subheader("🗑️ Delete Bowling Statistics")
            st.warning("⚠️ This action cannot be undone. Please be careful!")
            
            bowling_df = run_query("""
                SELECT b.bowling_id, p.full_name, b.wickets, b.runs, m.description as match_info
                FROM bowling b
                JOIN players p ON b.player_id = p.player_id
                JOIN innings i ON b.innings_id = i.innings_id
                JOIN matches m ON i.match_id = m.match_id
                ORDER BY b.bowling_id DESC LIMIT 100
            """)
            
            if bowling_df.empty:
                st.info("No bowling statistics available to delete")
                return
                
            bowling_options = {f"{row['full_name']} - {row['wickets']}/{row['runs']} (Match: {row['match_info']})": row['bowling_id'] 
                             for _, row in bowling_df.iterrows()}
            selected_bowling = st.selectbox("Select Bowling Record to Delete", options=list(bowling_options.keys()))
            bowling_id = bowling_options[selected_bowling]
            
            bowling_info = run_query("""
                SELECT b.*, p.full_name, m.description as match_info, t.name as team_name
                FROM bowling b
                JOIN players p ON b.player_id = p.player_id
                JOIN innings i ON b.innings_id = i.innings_id
                JOIN matches m ON i.match_id = m.match_id
                JOIN teams t ON p.team_id = t.team_id
                WHERE b.bowling_id = :bowling_id
            """, {"bowling_id": bowling_id})
            
            if not bowling_info.empty:
                st.write("**Bowling Record Details:**")
                st.dataframe(bowling_info, use_container_width=True)
                
                confirm_delete = st.checkbox("I understand this action cannot be undone")
                submitted = st.button("🚨 Confirm Delete", type="secondary", disabled=not confirm_delete)
                if submitted:
                    try:
                        run_execute("DELETE FROM bowling WHERE bowling_id = :bowling_id", {"bowling_id": bowling_id})
                        st.success("✅ Bowling record deleted successfully!")
                        st.rerun()
                    except Exception as e:
                        st.error(f"❌ Error deleting bowling record: {str(e)}")
                elif not confirm_delete:
                    st.info("Please check the confirmation box to enable delete button")

    # TEAMS CRUD
    elif entity_type == "Teams":
        if mode == "Create":
            st.subheader("➕ Create New Team")
            with st.form("create_team_form"):
                col1, col2 = st.columns(2)
                
                with col1:
                    name = st.text_input("Team Name*", placeholder="India National Cricket Team")
                    country = st.text_input("Country*", placeholder="India")
                
                with col2:
                    short_name = st.text_input("Short Name", placeholder="IND", max_chars=4)
                    logo_url = st.text_input("Logo URL", placeholder="https://example.com/logo.png")
                
                submitted = st.form_submit_button("Create Team")
                if submitted:
                    if not all([name.strip(), country.strip()]):
                        st.error("Please fill all required fields (*)")
                    else:
                        try:
                            # Check if team already exists
                            existing_team = run_query("SELECT name FROM teams WHERE LOWER(name) = LOWER(:name) OR LOWER(short_name) = LOWER(:short_name)", 
                                                    {"name": name.strip(), "short_name": short_name.strip() if short_name else ""})
                            if not existing_team.empty:
                                st.error("❌ A team with this name or short name already exists!")
                            else:
                                run_execute("""
                                    INSERT INTO teams (name, country, short_name, logo_url)
                                    VALUES (:name, :country, :short_name, :logo_url)
                                """, {
                                    "name": name.strip(),
                                    "country": country.strip(),
                                    "short_name": short_name.strip() if short_name else None,
                                    "logo_url": logo_url.strip() if logo_url else None
                                })
                                st.success("✅ Team created successfully!")
                                st.rerun()
                        except Exception as e:
                            st.error(f"❌ Error creating team: {str(e)}")
        
        elif mode == "Read":
            st.subheader("🏟️ View Teams")
            
            col1, col2 = st.columns(2)
            with col1:
                search_term = st.text_input("Search teams", placeholder="Search by team name or country")
            with col2:
                sort_by = st.selectbox("Sort by", ["Name", "Country", "Most Players", "Recent Matches"])
            
            # Get teams with safe column access
            teams_df = run_query("SELECT team_id, name, country, short_name, logo_url FROM teams")
            
            if not teams_df.empty:
                # Add statistics safely
                for index, team in teams_df.iterrows():
                    player_count = run_query("SELECT COUNT(*) as count FROM players WHERE team_id = :team_id", 
                                           {"team_id": team['team_id']})
                    match_count = run_query("SELECT COUNT(*) as count FROM matches WHERE home_team_id = :team_id OR away_team_id = :team_id", 
                                          {"team_id": team['team_id']})
                    
                    teams_df.at[index, 'player_count'] = player_count.iloc[0]['count'] if not player_count.empty else 0
                    teams_df.at[index, 'match_count'] = match_count.iloc[0]['count'] if not match_count.empty else 0
                
                # Apply search filter
                if search_term:
                    search_lower = search_term.lower()
                    teams_df = teams_df[
                        teams_df.apply(lambda row: 
                                    search_lower in str(row.get('name', '')).lower() or 
                                    search_lower in str(row.get('country', '')).lower(), axis=1)
                    ]
                
                # Apply sorting
                if sort_by == "Name":
                    teams_df = teams_df.sort_values('name')
                elif sort_by == "Country":
                    teams_df = teams_df.sort_values('country')
                elif sort_by == "Most Players":
                    teams_df = teams_df.sort_values('player_count', ascending=False)
                elif sort_by == "Recent Matches":
                    teams_df = teams_df.sort_values('match_count', ascending=False)
                
                # Display team cards
                for _, team in teams_df.iterrows():
                    with st.expander(f"🏏 {team.get('name', 'Unknown')} ({team.get('country', 'Unknown')})"):
                        col1, col2, col3 = st.columns(3)
                        with col1:
                            st.metric("Players", team.get('player_count', 0))
                        with col2:
                            st.metric("Matches", team.get('match_count', 0))
                        with col3:
                            st.write(f"Short: {team.get('short_name', 'N/A')}")
                
                # Display dataframe with safe column access
                display_columns = ['team_id', 'name', 'country', 'short_name']
                if 'player_count' in teams_df.columns:
                    display_columns.append('player_count')
                if 'match_count' in teams_df.columns:
                    display_columns.append('match_count')
                
                st.dataframe(teams_df[display_columns], use_container_width=True)
                
                # Export options
                col1, col2 = st.columns(2)
                with col1:
                    csv = teams_df[display_columns].to_csv(index=False)
                    st.download_button("📥 Export to CSV", csv, "teams.csv", "text/csv")
                with col2:
                    buffer = io.BytesIO()
                    with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
                        teams_df[display_columns].to_excel(writer, index=False, sheet_name='Teams')
                        writer.close()
                    st.download_button("📊 Export to Excel", buffer.getvalue(), "teams.xlsx",
                                     "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
            else:
                st.info("No teams found")
        
        elif mode == "Update":
            st.subheader("✏️ Update Team")
            
            teams_df = run_query("SELECT team_id, name, country FROM teams ORDER BY name")
            if teams_df.empty:
                st.info("No teams available to update")
                return
                
            # Safe team options creation
            team_options = {}
            for _, row in teams_df.iterrows():
                team_name = row.get('name', 'Unknown Team')
                team_country = row.get('country', 'Unknown Country')
                team_id = row.get('team_id')
                if team_id is not None:
                    team_options[f"{team_name} ({team_country})"] = team_id
            
            if not team_options:
                st.error("No valid teams found for selection")
                return
                
            selected_team = st.selectbox("Select Team to Update", options=list(team_options.keys()))
            team_id = team_options[selected_team]
            
            team_data = run_query("SELECT * FROM teams WHERE team_id = :team_id", {"team_id": team_id})
            if team_data.empty:
                st.error("Team not found")
                return
                
            team_data = team_data.iloc[0]
            
            with st.form("update_team_form"):
                col1, col2 = st.columns(2)
                
                with col1:
                    name = st.text_input("Team Name*", value=team_data.get('name', ''))
                    country = st.text_input("Country*", value=team_data.get('country', ''))
                
                with col2:
                    short_name = st.text_input("Short Name", value=team_data.get('short_name', '') or "", max_chars=4)
                    logo_url = st.text_input("Logo URL", value=team_data.get('logo_url', '') or "")
                
                # Display team statistics
                st.subheader("Team Statistics")
                stats_col1, stats_col2 = st.columns(2)
                
                player_count = run_query("SELECT COUNT(*) as count FROM players WHERE team_id = :team_id", {"team_id": team_id})
                match_count = run_query("SELECT COUNT(*) as count FROM matches WHERE home_team_id = :team_id OR away_team_id = :team_id", {"team_id": team_id})
                
                with stats_col1:
                    st.metric("Total Players", player_count.iloc[0]['count'] if not player_count.empty else 0)
                with stats_col2:
                    st.metric("Total Matches", match_count.iloc[0]['count'] if not match_count.empty else 0)
                
                submitted = st.form_submit_button("Update Team")
                if submitted:
                    if not all([name.strip(), country.strip()]):
                        st.error("Please fill all required fields (*)")
                    else:
                        try:
                            run_execute("""
                                UPDATE teams SET 
                                    name = :name, country = :country, short_name = :short_name, logo_url = :logo_url
                                WHERE team_id = :team_id
                            """, {
                                "name": name.strip(),
                                "country": country.strip(),
                                "short_name": short_name.strip() if short_name else None,
                                "logo_url": logo_url.strip() if logo_url else None,
                                "team_id": team_id
                            })
                            st.success("✅ Team updated successfully!")
                            st.rerun()
                        except Exception as e:
                            st.error(f"❌ Error updating team: {str(e)}")
        
        elif mode == "Delete":
            st.subheader("🗑️ Delete Team")
            st.warning("⚠️ This action cannot be undone. Please be careful!")
            
            teams_df = run_query("SELECT team_id, name, country FROM teams ORDER BY name")
            if teams_df.empty:
                st.info("No teams available to delete")
                return
                
            # Safe team options creation
            team_options = {}
            for _, row in teams_df.iterrows():
                team_name = row.get('name', 'Unknown Team')
                team_country = row.get('country', 'Unknown Country')
                team_id = row.get('team_id')
                if team_id is not None:
                    team_options[f"{team_name} ({team_country})"] = team_id
            
            if not team_options:
                st.error("No valid teams found for selection")
                return
                
            selected_team = st.selectbox("Select Team to Delete", options=list(team_options.keys()))
            team_id = team_options[selected_team]
            
            team_info = run_query("SELECT * FROM teams WHERE team_id = :team_id", {"team_id": team_id})
            if not team_info.empty:
                st.write("**Team Details:**")
                st.dataframe(team_info, use_container_width=True)
                
                # Check for dependent records
                players_count = run_query("SELECT COUNT(*) as count FROM players WHERE team_id = :team_id", {"team_id": team_id})
                matches_count = run_query("SELECT COUNT(*) as count FROM matches WHERE home_team_id = :team_id OR away_team_id = :team_id", {"team_id": team_id})
                
                players_count_val = players_count.iloc[0]['count'] if not players_count.empty else 0
                matches_count_val = matches_count.iloc[0]['count'] if not matches_count.empty else 0
                
                if players_count_val > 0 or matches_count_val > 0:
                    st.error(f"❌ Cannot delete team. It has {players_count_val} players and {matches_count_val} matches associated. Please reassign or delete these records first.")
                else:
                    confirm_delete = st.checkbox("I understand this action cannot be undone and all team data will be permanently lost")
                    if st.button("🚨 Confirm Delete", type="secondary", disabled=not confirm_delete):
                        try:
                            run_execute("DELETE FROM teams WHERE team_id = :team_id", {"team_id": team_id})
                            st.success("✅ Team deleted successfully!")
                            st.rerun()
                        except Exception as e:
                            st.error(f"❌ Error deleting team: {str(e)}")
                    elif not confirm_delete:
                        st.info("Please check the confirmation box to enable delete button")

    # VENUES CRUD
    elif entity_type == "Venues":
        if mode == "Create":
            st.subheader("➕ Create New Venue")
            with st.form("create_venue_form"):
                col1, col2 = st.columns(2)
                
                with col1:
                    name = st.text_input("Venue Name*", placeholder="Melbourne Cricket Ground")
                    city = st.text_input("City", placeholder="Melbourne")
                    country = st.text_input("Country", placeholder="Australia")
                
                with col2:
                    capacity = st.number_input("Capacity", min_value=0, step=1000, value=0,
                                            help="Enter 0 if capacity is unknown")
                    # Fix for established year - allow 0 as unknown
                    established = st.number_input("Year Established", 
                                               min_value=0, 
                                               max_value=datetime.now().year, 
                                               step=1, 
                                               value=0,
                                               help="Enter 0 if year is unknown")
                
                submitted = st.form_submit_button("Create Venue")
                if submitted:
                    if not name.strip():
                        st.error("Please fill the required field (*)")
                    else:
                        try:
                            # Check if venue already exists
                            existing_venue = run_query("SELECT name FROM venues WHERE LOWER(name) = LOWER(:name) AND LOWER(city) = LOWER(:city)", 
                                                     {"name": name.strip(), "city": city.strip() if city else ""})
                            if not existing_venue.empty:
                                st.error("❌ A venue with this name already exists in the same city!")
                            else:
                                run_execute("""
                                    INSERT INTO venues (name, city, country, capacity, established)
                                    VALUES (:name, :city, :country, :capacity, :established)
                                """, {
                                    "name": name.strip(),
                                    "city": city.strip() if city else None,
                                    "country": country.strip() if country else None,
                                    "capacity": capacity if capacity > 0 else None,
                                    "established": established if established > 0 else None
                                })
                                st.success("✅ Venue created successfully!")
                                st.rerun()
                        except Exception as e:
                            st.error(f"❌ Error creating venue: {str(e)}")
        
        elif mode == "Read":
            st.subheader("📍 View Venues")
            
            col1, col2, col3 = st.columns(3)
            with col1:
                search_term = st.text_input("Search venues", placeholder="Search by venue name or city")
            with col2:
                min_capacity = st.number_input("Minimum Capacity", min_value=0, value=0)
            with col3:
                country_filter = st.text_input("Filter by Country", placeholder="e.g., Australia")
            
            # Fix SQL syntax - remove NULLS LAST which is not supported in MySQL
            query = """
                SELECT v.*, COUNT(m.match_id) as match_count
                FROM venues v
                LEFT JOIN matches m ON v.venue_id = m.venue_id
                GROUP BY v.venue_id, v.name, v.city, v.country, v.capacity, v.established 
                ORDER BY v.capacity DESC
            """
            
            df = run_query(query)
            
            if not df.empty:
                # Apply filters
                if search_term:
                    search_lower = search_term.lower()
                    df = df[
                        df.apply(lambda row: 
                                search_lower in str(row.get('name', '')).lower() or 
                                search_lower in str(row.get('city', '')).lower(), axis=1)
                    ]
                
                if country_filter:
                    country_lower = country_filter.lower()
                    df = df[df.apply(lambda row: country_lower in str(row.get('country', '')).lower(), axis=1)]
                
                if min_capacity > 0:
                    df = df[(df['capacity'] >= min_capacity) | (df['capacity'].isna())]
                
                # Display venue cards with safe column access
                for _, venue in df.iterrows():
                    venue_name = venue.get('name', 'Unknown Venue')
                    venue_city = venue.get('city', 'Unknown City')
                    venue_country = venue.get('country', 'Unknown Country')
                    
                    with st.expander(f"🏟️ {venue_name} - {venue_city}, {venue_country}"):
                        col1, col2, col3 = st.columns(3)
                        with col1:
                            capacity_val = venue.get('capacity')
                            st.metric("Capacity", f"{capacity_val:,}" if capacity_val else "Unknown")
                        with col2:
                            match_count = venue.get('match_count', 0)
                            st.metric("Matches", match_count)
                        with col3:
                            established = venue.get('established')
                            st.write(f"Est: {established if established else 'Unknown'}")
                
                # Display dataframe with safe column access
                display_columns = ['venue_id', 'name', 'city', 'country', 'capacity', 'established', 'match_count']
                available_columns = [col for col in display_columns if col in df.columns]
                
                st.dataframe(df[available_columns], use_container_width=True)
                
                # Export options
                col1, col2 = st.columns(2)
                with col1:
                    csv = df[available_columns].to_csv(index=False)
                    st.download_button("📥 Export to CSV", csv, "venues.csv", "text/csv")
                with col2:
                    buffer = io.BytesIO()
                    with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
                        df[available_columns].to_excel(writer, index=False, sheet_name='Venues')
                        writer.close()
                    st.download_button("📊 Export to Excel", buffer.getvalue(), "venues.xlsx",
                                     "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
            else:
                st.info("No venues found")
        
        elif mode == "Update":
            st.subheader("✏️ Update Venue")
            
            venues_df = run_query("SELECT venue_id, name, city, country FROM venues ORDER BY name")
            if venues_df.empty:
                st.info("No venues available to update")
                return
                
            # Safe venue options creation
            venue_options = {}
            for _, row in venues_df.iterrows():
                venue_name = row.get('name', 'Unknown Venue')
                venue_city = row.get('city', 'Unknown City')
                venue_country = row.get('country', 'Unknown Country')
                venue_id = row.get('venue_id')
                if venue_id is not None:
                    venue_options[f"{venue_name} - {venue_city}, {venue_country}"] = venue_id
            
            if not venue_options:
                st.error("No valid venues found for selection")
                return
                
            selected_venue = st.selectbox("Select Venue to Update", options=list(venue_options.keys()))
            venue_id = venue_options[selected_venue]
            
            venue_data = run_query("SELECT * FROM venues WHERE venue_id = :venue_id", {"venue_id": venue_id})
            if venue_data.empty:
                st.error("Venue not found")
                return
                
            venue_data = venue_data.iloc[0]
            
            with st.form("update_venue_form"):
                col1, col2 = st.columns(2)
                
                with col1:
                    name = st.text_input("Venue Name*", value=venue_data.get('name', ''))
                    city = st.text_input("City", value=venue_data.get('city', '') or "")
                    country = st.text_input("Country", value=venue_data.get('country', '') or "")
                
                with col2:
                    capacity_val = venue_data.get('capacity', 0)
                    capacity = st.number_input("Capacity", 
                                            value=int(capacity_val) if capacity_val else 0,
                                            min_value=0, step=1000)
                    
                    established_val = venue_data.get('established', 0)
                    established = st.number_input("Year Established", 
                                               value=int(established_val) if established_val else 0,
                                               min_value=0, max_value=datetime.now().year, step=1)
                
                # Display venue statistics
                match_count = run_query("SELECT COUNT(*) as count FROM matches WHERE venue_id = :venue_id", 
                                      {"venue_id": venue_id})
                if not match_count.empty:
                    st.metric("Total Matches at this Venue", match_count.iloc[0]['count'])
                
                submitted = st.form_submit_button("Update Venue")
                if submitted:
                    if not name.strip():
                        st.error("Please fill the required field (*)")
                    else:
                        try:
                            run_execute("""
                                UPDATE venues SET 
                                    name = :name, city = :city, country = :country, 
                                    capacity = :capacity, established = :established
                                WHERE venue_id = :venue_id
                            """, {
                                "name": name.strip(),
                                "city": city.strip() if city else None,
                                "country": country.strip() if country else None,
                                "capacity": capacity if capacity > 0 else None,
                                "established": established if established > 0 else None,
                                "venue_id": venue_id
                            })
                            st.success("✅ Venue updated successfully!")
                            st.rerun()
                        except Exception as e:
                            st.error(f"❌ Error updating venue: {str(e)}")
        
        elif mode == "Delete":
            st.subheader("🗑️ Delete Venue")
            st.warning("⚠️ This action cannot be undone. Please be careful!")
            
            venues_df = run_query("SELECT venue_id, name, city, country FROM venues ORDER BY name")
            if venues_df.empty:
                st.info("No venues available to delete")
                return
                
            # Safe venue options creation
            venue_options = {}
            for _, row in venues_df.iterrows():
                venue_name = row.get('name', 'Unknown Venue')
                venue_city = row.get('city', 'Unknown City')
                venue_country = row.get('country', 'Unknown Country')
                venue_id = row.get('venue_id')
                if venue_id is not None:
                    venue_options[f"{venue_name} - {venue_city}, {venue_country}"] = venue_id
            
            if not venue_options:
                st.error("No valid venues found for selection")
                return
                
            selected_venue = st.selectbox("Select Venue to Delete", options=list(venue_options.keys()))
            venue_id = venue_options[selected_venue]
            
            venue_info = run_query("SELECT * FROM venues WHERE venue_id = :venue_id", {"venue_id": venue_id})
            if not venue_info.empty:
                st.write("**Venue Details:**")
                st.dataframe(venue_info, use_container_width=True)
                
                # Check for dependent records
                matches_count = run_query("SELECT COUNT(*) as count FROM matches WHERE venue_id = :venue_id", {"venue_id": venue_id})
                matches_count_val = matches_count.iloc[0]['count'] if not matches_count.empty else 0
                
                if matches_count_val > 0:
                    st.error(f"❌ Cannot delete venue. It has {matches_count_val} matches associated. Please reassign or delete these matches first.")
                else:
                    confirm_delete = st.checkbox("I understand this action cannot be undone and this venue will be permanently removed")
                    if st.button("🚨 Confirm Delete", type="secondary", disabled=not confirm_delete):
                        try:
                            run_execute("DELETE FROM venues WHERE venue_id = :venue_id", {"venue_id": venue_id})
                            st.success("✅ Venue deleted successfully!")
                            st.rerun()
                        except Exception as e:
                            st.error(f"❌ Error deleting venue: {str(e)}")
                    elif not confirm_delete:
                        st.info("Please check the confirmation box to enable delete button")