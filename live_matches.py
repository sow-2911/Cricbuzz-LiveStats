import streamlit as st
import utils.cricbuzz_api as api

def show():
    st.title("🏏 Live Cricket Matches")

    try:
        data = api.get_live_matches()
    except Exception as e:
        st.error(f"Failed to fetch live matches: {e}")
        st.stop()

    matches_found = 0

    for match_type in data.get("typeMatches", []):
        st.header(f"{match_type.get('matchType', 'Unknown')}")
        
        for series in match_type.get("seriesMatches", []):
            # Skip ads
            if "seriesAdWrapper" not in series:
                continue
            series_info = series["seriesAdWrapper"]
            st.subheader(series_info.get("seriesName", "Unknown Series"))
            
            for match in series_info.get("matches", []):
                info = match.get("matchInfo", {})
                score = match.get("matchScore", {})

                # Teams & match description
                st.markdown(f"**{info.get('team1', {}).get('teamName','')} vs {info.get('team2', {}).get('teamName','')}**")
                st.write(f"Match: {info.get('matchDesc','')}")
                st.write(f"Format: {info.get('matchFormat','')}")
                st.write(f"Status: {info.get('status','')}")
                
                # Venue
                venue = info.get("venueInfo", {})
                st.write(f"Venue: {venue.get('ground','')}, {venue.get('city','')}")

                # Scores
                t1 = score.get("team1Score", {}).get("inngs1", {})
                t2 = score.get("team2Score", {}).get("inngs1", {})

                if t1 or t2:
                    st.markdown("**Scores:**")
                    st.write(f"{info.get('team1', {}).get('teamName','')} - {t1.get('runs', 0)}/{t1.get('wickets', 0)} in {t1.get('overs',0)} overs")
                    st.write(f"{info.get('team2', {}).get('teamName','')} - {t2.get('runs', 0)}/{t2.get('wickets', 0)} in {t2.get('overs',0)} overs")

                st.markdown("---")
                matches_found += 1

    if matches_found == 0:
        st.info("No live matches currently.")