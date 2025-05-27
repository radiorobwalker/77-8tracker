import asyncio
import datetime
import streamlit as st
from lcwc.arcgis import ArcGISClient

TRACKED_UNITS = ["77-8", "77-81"]

async def fetch_tracked_incidents():
    client = ArcGISClient()
    incidents = await client.get_incidents()

    filtered = []
    for inc in incidents:
        if any(unit in (inc.units or "") for unit in TRACKED_UNITS):
            filtered.append({
                "Date": inc.date.strftime("%Y-%m-%d %H:%M"),
                "Location": inc.location,
                "Type": inc.description,
                "Units": inc.units
            })
    return filtered

# Streamlit UI
st.set_page_config(page_title="77-8 / 77-81 Live Tracker", layout="wide")
st.title("🚑 Live Incident Tracker for Units 77-8 and 77-81")
st.markdown("This dashboard pulls real-time data from LCWC's ArcGIS system and filters it for units 77-8 and 77-81.")

with st.spinner("Loading incident data..."):
    incidents = asyncio.run(fetch_tracked_incidents())

if incidents:
    st.success(f"Found {len(incidents)} active incident(s) involving tracked units.")
    st.dataframe(incidents, use_container_width=True)
else:
    st.info("No active incidents involving 77-8 or 77-81 right now.")

st.caption("Powered by [LCWC ArcGIS Data](https://www.lcwc911.us)")

