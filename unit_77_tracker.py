# unit_77_dashboard.py
# Streamlit dashboard to view incidents involving 77-8 and 77-81

import streamlit as st
import pandas as pd
import os

DATA_FILE = "unit_77_incidents.csv"

st.set_page_config(page_title="Unit 77 Tracker", layout="wide")
st.title("🚑 Unit 77-8 and 77-81 Activity Tracker")

# Load data
if os.path.exists(DATA_FILE):
    df = pd.read_csv(DATA_FILE)
    df["Date/Time"] = pd.to_datetime(df["Date/Time"], errors='coerce')
    df["Timestamp Checked"] = pd.to_datetime(df["Timestamp Checked"], errors='coerce')

    # Sort by latest incident first
    df.sort_values(by=["Date/Time"], ascending=False, inplace=True)

    # Display metrics
    st.markdown(f"### Total Incidents Logged: {len(df)}")
    st.dataframe(df, use_container_width=True)

    # Filter by unit if needed
    unit_filter = st.selectbox("Filter by Unit", options=["All"] + list(set(
        u for units in df["Units"] for u in units.split(','))))

    if unit_filter != "All":
        df_filtered = df[df["Units"].str.contains(unit_filter)]
        st.dataframe(df_filtered, use_container_width=True)

else:
    st.warning("No data file found. Run the tracking script first to collect data.")

