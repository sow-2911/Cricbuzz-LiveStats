# utils/cricbuzz_api.py
import requests
import time
from functools import lru_cache
import streamlit as st  # for Streamlit caching

CRICBUZZ_BASE = "https://cricbuzz-cricket.p.rapidapi.com"  # RapidAPI endpoint
RAPIDAPI_KEY = "83742a41d0mshb65558ccbf010fap14fa4ejsn7ea02362f1b7"

# Use the variable for headers
HEADERS = {
    "x-rapidapi-key": RAPIDAPI_KEY,
    "x-rapidapi-host": "cricbuzz-cricket.p.rapidapi.com"
}

def fetch_json(path, params=None, timeout=10, max_retries=2):
    url = f"{CRICBUZZ_BASE}/{path}"
    retries = 0
    while retries <= max_retries:
        try:
            r = requests.get(url, headers=HEADERS, params=params, timeout=timeout)
            r.raise_for_status()
            return r.json()
        except requests.RequestException as e:
            retries += 1
            if retries > max_retries:
                raise
            time.sleep(1 * retries)

# Streamlit cache to avoid hitting API repeatedly
@st.cache_data(ttl=10)  # cache lasts 10 seconds
def get_live_matches():
    """
    Returns live matches from Cricbuzz via RapidAPI.
    """
    return fetch_json("/matches/v1/live")  # adjust path if needed
