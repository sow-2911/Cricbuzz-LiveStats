import streamlit as st
from _pages import home, live_matches, top_stats, sql_queries, crud_operations

st.set_page_config(page_title="Cricbuzz LiveStats", layout="wide")

PAGES = {
    "Home": home,
    "Live Match": live_matches,
    "Top Player Stats": top_stats,
    "SQL Analytics": sql_queries,
    "CRUD Admin": crud_operations
}

page = st.sidebar.selectbox("Go to", list(PAGES.keys()))

# Show the selected page
PAGES[page].show()