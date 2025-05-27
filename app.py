import streamlit as st
import feedparser
from datetime import datetime
import time

# Constants
TRACKED_UNITS = ["77-8", "77-81"]
RSS_FEED_URL = "https://www.lcwc911.us/live-incident-list/rss"

# Set auto-refresh
st.set_page_config(page_title="77-8 / 77-81 Tracker", layout="wide)
countdown = 60
st_autorefresh = st.experimental_rerun if countdown == 0 else time.sleep(1)

# Page title
st.title("🚑 Live Incident Tracker for Units 77-8 and 77-81")
st.markdown("This dashboard shows the last 5 incidents involving 77-8 or 77-81. It refreshes every minute.")

# Fetch and filter incidents
def fetch_tracked_incidents():
    feed = feedparser.parse(RSS_FEED_URL)
    results = []

    for entry in feed.entries:
        description = entry.get("description", "")
        title = entry.get("title", "")
        published = entry.get("published", "")
        municipality = "Unknown"

        if "Municipality:" in description:
            try:
                municipality = description.split("Municipality:")[1].split("<")[0].strip()
            except:
                pass

        for unit in TRACKED_UNITS:
            if unit in description:
                results.append({
                    "Unit(s)": unit,
                    "Call Type": title,
                    "Municipality": municipality,
                    "Dispatched": published
                })
                break

    return results[:5]

# Load data
with st.spinner("Getting incident data..."):
    incidents = fetch_tracked_incidents()

# Display
if incidents:
    st.success(f"Displaying the last {len(incidents)} incidents involving tracked units.")
    st.table(incidents)
else:
    st.info("No recent incidents involving 77-8 or 77-81 found.")

st.caption("Data provided by LCWC via RSS. Clear times are not included in the RSS feed.")
