import requests
from bs4 import BeautifulSoup
import pandas as pd
import datetime
import streamlit as st

# Configuration
TARGET_UNITS = ["77-8", "77-81"]
LCWC_URL = "https://www.lcwc911.us/live-incident-list"

# Function: Fetch Incident Data
def fetch_incident_data():
    try:
        response = requests.get(LCWC_URL)
        response.raise_for_status()
    except requests.RequestException as e:
        st.error(f"Failed to fetch data: {e}")
        return pd.DataFrame()

    soup = BeautifulSoup(response.text, 'html.parser')
    table = soup.find('table', class_='views-table')
    if not table:
        st.warning("Incident table not found.")
        return pd.DataFrame()

    incidents = []
    rows = table.find_all('tr')[1:]  # Skip header

    for row in rows:
        cells = row.find_all('td')
        if len(cells) < 5:
            continue

        date_time = cells[0].get_text(strip=True)
        nature = cells[1].get_text(strip=True)
        location = cells[2].get_text(strip=True)
        municipality = cells[3].get_text(strip=True)
        units = cells[4].get_text(strip=True)

        for unit in TARGET_UNITS:
            if unit in units:
                incidents.append({
                    "Checked At": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "Date/Time": date_time,
                    "Type": nature,
                    "Location": location,
                    "Municipality": municipality,
                    "Units": units
                })
                break

    return pd.DataFrame(incidents)

# Streamlit App
st.set_page_config(page_title="77-8 and 77-81 Tracker", layout="wide")
st.title("🚑 Unit 77-8 and 77-81 Activity Tracker")

st.markdown("This dashboard checks the LCWC live feed for incidents involving units 77-8 and 77-81. Refresh the page to update.")

df = fetch_incident_data()

if not df.empty:
    st.success(f"Found {len(df)} active incident(s) involving tracked units.")
    st.dataframe(df, use_container_width=True)
else:
    st.info("No active incidents involving 77-8 or 77-81 right now.")

st.caption("Live source: [lcwc911.us](https://www.lcwc911.us/live-incident-list)")
