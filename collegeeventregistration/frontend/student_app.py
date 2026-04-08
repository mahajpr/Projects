

import streamlit as st
import requests

st.set_page_config(
    page_title="Inter-College Fest Registration",
    page_icon="🎓",
    layout="wide"
)

st.title("🎓 Inter-College Technical Fest 2026")
st.markdown("### Student Event Registration Form")
st.divider()

event_list = []
event_data = {}

try:
    res = requests.get("http://127.0.0.1:8000/events")
    if res.status_code == 200:
        events = res.json()

        for e in events:
            title = e["title"]
            event_list.append(title)
            event_data[title] = {
                "venue": e["venue"],
                "date": e["date"],
                "time": e["time"]
            }
except:
    st.error("Backend not running")


st.subheader("👤 Personal Details")

col1, col2 = st.columns(2)

with col1:
    name = st.text_input("Full Name *")
    email = st.text_input("Email *")
    phone = st.text_input("Phone *")

with col2:
    gender = st.selectbox("Gender", ["Male", "Female", "Other"])
    year = st.selectbox("Year", ["1st Year", "2nd Year", "3rd Year", "4th Year"])
    department = st.text_input("Department *")

st.divider()


st.subheader("🏫 College Details")
college = st.text_input("College *")
city = st.text_input("City")

st.divider()


st.subheader("🎯 Event Selection")

event = None

if event_list:
    event = st.selectbox("Choose Event", event_list)

    selected = event_data.get(event)

    if selected:
        st.info(f"""
        Venue:{selected['venue']}  
        Date: {selected['date']}  
        Time: {selected['time']}""")
else:
    st.warning("No events available. Contact admin.")

team_event = st.checkbox("Team Event")

team_name = ""
team_size = 1
teammates = ""

if team_event:
    team_name = st.text_input("Team Name")
    team_size = st.number_input("Team Size", 2, 10, 2)
    teammates = st.text_area("Teammates")

st.divider()

consent = st.checkbox("I confirm details are correct")
submit = st.button("🚀 Register")


if submit:

    if not consent:
        st.error("Please confirm consent")
        st.stop()

    payload = {
        "name": name,
        "email": email,
        "phone": phone,
        "gender": gender,
        "year": year,
        "department": department,
        "college": college,
        "city": city,
        "event": event,
        "team_event": "Yes" if team_event else "No",
        "team_name": team_name,
        "team_size": team_size,
        "teammates": teammates
    }

    try:
        res = requests.post("http://127.0.0.1:8000/register", json=payload)

        if res.status_code == 200:
            st.success("🎉 Registered successfully!")
            st.balloons()
        else:
            st.error(res.text)

    except:
        st.error("Backend not running")

API_CHAT = "http://127.0.0.1:8000/chat"
if "chat_open" not in st.session_state:
    st.session_state.chat_open = False

if "messages" not in st.session_state:
    st.session_state.messages = []


if st.button("💬 Chat Assistant", key="chat_btn"):
    st.session_state.chat_open = not st.session_state.chat_open


if st.session_state.chat_open:

    st.markdown('<div class="chat-box">', unsafe_allow_html=True)

    st.markdown("### 🤖 Fest Assistant")

    user_input = st.text_input("Ask about rules...", key="chat_input")

    if st.button("Send") and user_input:
        try:
            res = requests.post(API_CHAT, json={"query": user_input})
            answer = res.json()["answer"]
        except:
            answer = "Server not running"

        st.session_state.messages.append(("You", user_input))
        st.session_state.messages.append(("Bot", answer))

    for sender, msg in st.session_state.messages:
        if sender == "You":
            st.markdown(f"**🧑 {msg}**")
        else:
            st.markdown(f"**🤖 {msg}**")

    st.markdown('</div>', unsafe_allow_html=True)
