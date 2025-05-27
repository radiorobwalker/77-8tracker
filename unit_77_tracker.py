"""
unit_77_tracker.py
------------------
Monitors the LCWC Live Incident List for activity involving EMS units 77-8 and 77-81.
Scrapes the live feed, logs when those units are assigned, and tracks their incident details.

Dependencies:
- requests
- beautifulsoup4
- pandas

To install dependencies:
pip install requests beautifulsoup4 pandas

To schedule this script to run every minute (Linux/Mac):
* * * * * /usr/bin/python3 /path/to/unit_77_tracker.py

Created for cloud-based tracking and GitHub deployment.
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd
import datetime
import os

# --- Configuration ---
TARGET_UNITS = ["77-8", "77-81"]
OUTPUT_FILE = "unit_77_incidents.csv"
LCWC_URL = "https://www.lcwc911.us/live-incident-list"

# --- Function: Fetch Incident Data ---
def fetch_incident_data():
    try:
        response = requests.get(LCWC_URL)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"[ERROR] Unable to fetch data: {e}")
        return []

    soup = BeautifulSoup(response.text, 'html.parser')
    table = soup.find('table', class_='views-table')
    if not table:
        print("[WARNING] Incident table not found.")
        return []

    incidents = []
    rows = table.find_all('tr')[1:]  # Skip header row

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
                    "Timestamp Checked": datetime.datetime.now().isoformat(),
                    "Date/Time": date_time,
                    "Type": nature,
                    "Location": location,
                    "Municipality": municipality,
                    "Units": units
                })
                break

    return incidents

# --- Function: Update CSV File ---
def update_csv(incidents):
    new_df = pd.DataFrame(incidents)

    if os.path.exists(OUTPUT_FILE):
        existing_df = pd.read_csv(OUTPUT_FILE)
        combined_df = pd.concat([existing_df, new_df], ignore_index=True)
        combined_df.drop_duplicates(subset=["Date/Time", "Units"], inplace=True)
    else:
        combined_df = new_df

    combined_df.to_csv(OUTPUT_FILE, index=False)

# --- Main Execution ---
def main():
    incidents = fetch_incident_data()
    if incidents:
        update_csv(incidents)
        print(f"[INFO] Logged {len(incidents)} tracked incident(s) at {datetime.datetime.now().isoformat()}")
    else:
        print(f"[INFO] No tracked units active at {datetime.datetime.now().isoformat()}")

if __name__ == "__main__":
    main()
