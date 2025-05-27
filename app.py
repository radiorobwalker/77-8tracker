import streamlit as st
import feedparser
from datetime import datetime

# RSS feed URL
RSS_URL = "https://www.lcwc911.us/live-incident-list/rss"

# Units to track
TRACKED_UNITS = ["77-8", "77-81"]

def fetch_incidents():
    feed = feedparser.parse(RSS_URL)
    incidents = []
    for entry in feed.entries:
        title = entry.title
        description = entry.description
        pub_date = entry.published
        for unit in TRACKED_UNITS:
            if unit in description:
                incidents.append({
                    "Title": title,
                    "Description": description,
                    "Published": pub_date
                })
                break
    return incidents

st.set_page_config(page_title="77-8 / 77-81 Live Tracker", layout="wide")
st.title("🚑 Live Incident Tracker for Units 77-8 and 77-81")
st.markdown("This dashboard pulls real-time data from LCWC's RSS feed and filters it for units 77-8 and 77-81.")

with st.spinner("Loading incident data..."):
    incidents = fetch_incidents()

if incidents:
    st.success(f"Found {len(incidents)} active incident(s) involving tracked units.")
    for incident in incidents:
        st.subheader(incident["Title"])
        st.write(f"**Published:** {incident['Published']}")
        st.write(f"**Description:** {incident['Description']}")
        st.markdown("---")
else:
    st.info("No active incidents involving 77-8 or 77-81 right now.")

st.caption("Powered by [LCWC RSS Feed](https://www.lcwc911.us/live-incident-list)")
