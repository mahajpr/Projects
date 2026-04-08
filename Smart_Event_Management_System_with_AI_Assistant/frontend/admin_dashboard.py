
import streamlit as st
import os
import json
import requests
import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials


st.set_page_config(page_title="Admin Dashboard", layout="wide")

st.title("Admin Dashboard")

if "token" not in st.session_state:
    st.subheader("Admin Login")

    email = st.text_input("Email")
    pwd = st.text_input("Password", type="password")

    if st.button("Login"):
        res = requests.post("http://127.0.0.1:8000/login",
            json={"email": email, "password": pwd}
        )

        if res.status_code == 200 and "access_token" in res.json():
            st.session_state.token = res.json()["access_token"]
            st.success("Login success")
            st.rerun()
        else:
            st.error("Invalid credentials")

    st.stop()

headers = {"Authorization": f"Bearer {st.session_state.token}"}

st.header("📅 Create Event")

with st.form("event_form"):
    title = st.text_input("Title")
    venue = st.text_input("Venue")
    date = st.text_input("Date")
    time = st.text_input("Time")

    if st.form_submit_button("Create Event"):
        res = requests.post("http://127.0.0.1:8000/events",
            json={
                "title": title,
                "venue": venue,
                "date": date,
                "time": time
            },
            headers=headers
        )

        if res.status_code == 200:
            st.success("Event created")
        else:
            st.error(res.text)

st.divider()

st.header("📊 Registrations (Google Sheet)")

try:
    scope = [
        "https://spreadsheets.google.com/feeds",
        "https://www.googleapis.com/auth/drive"
    ]
    
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

    creds_path = os.path.join(BASE_DIR, "..", "backend", "credentials.json")
    creds_path = os.path.abspath(creds_path)

    if not os.path.exists(creds_path):
        st.error("credentials.json not found")
        st.stop()

    creds = ServiceAccountCredentials.from_json_keyfile_name(creds_path, scope)

    client = gspread.authorize(creds)

    sheet = client.open("College Event Registrations").sheet1
    data = sheet.get_all_records()

    df = pd.DataFrame(data)

    st.metric("Total Registrations", len(df))

    st.dataframe(df, use_container_width=True)

    csv = df.to_csv(index=False).encode()
    st.download_button(
        "Download CSV",
        csv,
        "registrations.csv",
        "text/csv"
    )

except Exception as e:
    st.error("Google Sheet not connected")
    st.code(str(e))


