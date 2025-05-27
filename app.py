import streamlit as st
from streamlit_autorefresh import st_autorefresh
import feedparser
from datetime import datetime

# 🔧 Must be first Streamlit command
st.set_page_config(page_title="77-8 / 77-81 Tracker", layout="wide")

# 🔁 Auto-refresh every 60 seconds
st_autorefresh(interval=60 * 1000, key="refresh")

# 🔹 Page content
st.title("🚑 Live Incident Tracker for Units 77-8 and 77-81")
st.markdown("This dashboard shows the last 5 incidents involving **MEDIC, INT, or AMB 77-8 or 77-81**. It refreshes every minute.")

# 🔍 Tracked unit variants
TRACKED_UNITS = [
    "MEDIC 77-8", "MEDIC 77-81",
    "INT 77-8", "INT 77-81",
    "AMB 77-8", "AMB 77-81"
]

RSS_FEED_URL = "https://www.lcwc911.us/live-incident-list/rss"

# 🔄 Data fetch function
def fetch_tracked_incidents():
    feed = feedparser.parse(RSS_FEED_URL)
    results = []

    for entry in feed.entries:
        description = entry.get("description", "")
        title = entry.get("title", "")
        published = entry.get("published", "")
        municipality = "Unknown"
        matched_unit = None

        if "Municipality:" in description:
            try:
                municipality = description.split("Municipality:")[1].split("<")[0].strip()
            except:
                pass

        for unit in TRACKED_UNITS:
            if unit in description:
                matched_unit = unit
                results.append({
                    "Unit": matched_unit,
                    "Call Type": title,
                    "Municipality": municipality,
                    "Dispatched": published
                })
                break

    return results[:5]

# 🖥️ Display
with st.spinner("Getting incident data..."):
    incidents = fetch_tracked_incidents()

if incidents:
    st.success(f"Showing the last {len(incidents)} calls for tracked units.")
    st.table(incidents)
else:
    st.info("No recent incidents involving 77-8 or 77-81 units found.")

st.caption("Data source: LCWC RSS Feed – does not include cleared times.")
