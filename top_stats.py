# pages/player_stats.py
import streamlit as st
import http.client
import json
import requests
import pandas as pd
import os
from dotenv import load_dotenv
from typing import Dict

# ---------------- Load API Key ----------------
load_dotenv()
API_KEY = os.getenv("CRICBUZZ_API_KEY")

if not API_KEY:
    st.error("❌ CRICBUZZ_API_KEY not found in environment variables. Please create a .env file with your API key.")
    st.stop()

# ---------------- API Config ----------------
BASE_URL = "cricbuzz-cricket.p.rapidapi.com"
HEADERS = {
    "x-rapidapi-key": API_KEY,
    "x-rapidapi-host": BASE_URL
}

# ---------------- Helper Functions ----------------
def search_players(query: str) -> Dict:
    """Search players by name"""
    try:
        conn = http.client.HTTPSConnection(BASE_URL)
        conn.request("GET", f"/stats/v1/player/search?plrN={query}", headers=HEADERS)
        res = conn.getresponse()
        data = res.read()
        conn.close()
        return json.loads(data.decode("utf-8"))
    except:
        return {}

def get_player_details(player_id: int) -> Dict:
    """Get full profile of a player"""
    try:
        conn = http.client.HTTPSConnection(BASE_URL)
        conn.request("GET", f"/stats/v1/player/{player_id}", headers=HEADERS)
        res = conn.getresponse()
        data = res.read()
        conn.close()
        return json.loads(data.decode("utf-8"))
    except:
        return {}

def get_player_stats(player_id: int, stat_type="batting") -> Dict:
    """Fetch batting or bowling stats"""
    try:
        url = f"https://{BASE_URL}/stats/v1/player/{player_id}/{stat_type}"
        response = requests.get(url, headers=HEADERS)
        if response.status_code == 200:
            return response.json()
    except:
        return {}
    return {}

def parse_stats_table(stats_json: dict) -> pd.DataFrame:
    """Convert Cricbuzz stats JSON to DataFrame"""
    if not stats_json or "headers" not in stats_json or "values" not in stats_json:
        return pd.DataFrame()
    headers = stats_json["headers"]
    rows = [row.get("values", []) for row in stats_json.get("values", [])]
    return pd.DataFrame(rows, columns=headers)

def get_career_info(player_id: int) -> pd.DataFrame:
    """Fetch player's career debut info"""
    try:
        conn = http.client.HTTPSConnection(BASE_URL)
        conn.request("GET", f"/stats/v1/player/{player_id}/career", headers=HEADERS)
        res = conn.getresponse()
        data = res.read()
        conn.close()
        career_json = json.loads(data.decode("utf-8"))
        if "values" in career_json and career_json["values"]:
            career_df = pd.DataFrame(
                [[f.get("name"), f.get("debut"), f.get("lastPlayed")] for f in career_json["values"]],
                columns=["Format", "Debut", "Last Played"]
            )
            return career_df
    except:
        pass
    return pd.DataFrame()

# ---------------- Streamlit Page ----------------
def show():
    st.title("📊 Player Stats & Profile")

    # Input player name
    player_name = st.text_input("Enter player name (e.g. Kohli, Dhoni, Smith):")
    if not player_name:
        return

    results = search_players(player_name)

    # Raw API response hidden in expander
    with st.expander("🔍 Show Raw API Response (for debugging)"):
        st.json(results)

    # Check if players exist
    if "player" not in results or not results["player"]:
        st.warning("No players found. Try another name.")
        return

    # Player selection
    player_options = {p.get("name","Unknown"): p for p in results["player"]}
    selected_name = st.selectbox("Select a player:", list(player_options.keys()))
    selected_player = player_options[selected_name]
    player_details = get_player_details(selected_player.get("id", 0))

    # Tabs
    tabs = st.tabs(["📌 Profile", "🏏 Batting Stats", "🎯 Bowling Stats"])

    # ---------- PROFILE TAB ----------
    with tabs[0]:
        st.write(f"### {selected_player.get('name','N/A')} ({selected_player.get('teamName','N/A')})")
        st.write(f"📅 DOB: {player_details.get('dob','N/A')}")

        # Image
        if player_details.get("image"):
            st.image(player_details["image"].replace("http://", "https://"), width=150)
        elif selected_player.get("faceImageId"):
            st.image(f"https://www.cricbuzz.com/a/img/v1/152x152/i1/c{selected_player['faceImageId']}.jpg", width=150)
        else:
            st.image("https://placehold.co/150x150/800000/FFFFFF?text=No+Image", width=150)

        # Basic info
        st.subheader("Player Details")
        st.write(f"**Role:** {player_details.get('role','N/A')}")
        st.write(f"**Batting Style:** {player_details.get('bat','N/A')}")
        st.write(f"**Bowling Style:** {player_details.get('bowl','N/A')}")
        st.write(f"**Teams:** {player_details.get('teams','N/A')}")
        st.write(f"**Birth Place:** {player_details.get('birthPlace','N/A')}")

        # ICC Rankings
        if "rankings" in player_details and player_details["rankings"]:
            st.subheader("🏆 ICC Rankings")
            rankings = player_details["rankings"]
            col1, col2, col3 = st.columns(3)
            with col1:
                st.write("### Batting")
                for k, v in rankings.get("bat", {}).items():
                    st.write(f"{k}: {v}")
            with col2:
                st.write("### Bowling")
                for k, v in rankings.get("bowl", {}).items():
                    st.write(f"{k}: {v}")
            with col3:
                st.write("### All-Rounder")
                for k, v in rankings.get("all", {}).items():
                    st.write(f"{k}: {v}")

        # Career info
        st.subheader("Career Debut Info")
        career_df = get_career_info(selected_player.get("id",0))
        if not career_df.empty:
            st.dataframe(career_df, use_container_width=True)
        else:
            st.warning("No career debut information available.")

        # Cricbuzz link
        if player_details.get("webURL"):
            st.markdown(f"[🔗 View on Cricbuzz]({player_details['webURL']})")

    # ---------- BATTING STATS TAB ----------
    with tabs[1]:
        st.subheader("Batting Stats")
        batting_stats = get_player_stats(selected_player.get("id",0), "batting")
        with st.expander("🔍 Show Raw Batting Stats (for debugging)"):
            st.json(batting_stats)
        df_bat = parse_stats_table(batting_stats)
        if not df_bat.empty:
            st.dataframe(df_bat, use_container_width=True)
        else:
            st.warning("No batting stats available.")

    # ---------- BOWLING STATS TAB ----------
    with tabs[2]:
        st.subheader("Bowling Stats")
        bowling_stats = get_player_stats(selected_player.get("id",0), "bowling")
        with st.expander("🔍 Show Raw Bowling Stats (for debugging)"):
            st.json(bowling_stats)
        df_bowl = parse_stats_table(bowling_stats)
        if not df_bowl.empty:
            st.dataframe(df_bowl, use_container_width=True)
        else:
            st.warning("No bowling stats available.")
