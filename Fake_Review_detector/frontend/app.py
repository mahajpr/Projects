import streamlit as st
import pandas as pd
import requests

st.set_page_config(
    page_title="Fake Review Detection Dashboard",
    layout="wide"
)

BASE_URL = "http://127.0.0.1:8000"

API_ANALYZE = f"{BASE_URL}/analyze"
API_STATS = f"{BASE_URL}/stats"
API_REVIEWS = f"{BASE_URL}/reviews"
API_FLAGGED = f"{BASE_URL}/flagged"


if "page" not in st.session_state:
    st.session_state.page = "Dashboard"

st.sidebar.title("🔍 Fake Review Detection")

if st.sidebar.button("Dashboard"):
    st.session_state.page = "Dashboard"

if st.sidebar.button("All Reviews"):
    st.session_state.page = "All Reviews"

if st.sidebar.button("Flagged Reviews"):
    st.session_state.page = "Flagged Reviews"

if st.sidebar.button("Reports"):
    st.session_state.page = "Reports"

if st.session_state.page == "Dashboard":

    st.markdown("## Fake Review Detection Dashboard")

    try:
        stats_response = requests.get(API_STATS, timeout=30)
        stats = stats_response.json() if stats_response.status_code == 200 else {}
    except:
        stats = {}

    stats_defaults = {
        "total_reviews": 0,
        "detected_fake": 0,
        "flagged_reviews": 0,
        "monthly_reviews": 0
    }

    stats = {**stats_defaults, **stats}

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Reviews", stats["total_reviews"])
    col2.metric("Detected as Fake", stats["detected_fake"])
    col3.metric("Flagged for Review", stats["flagged_reviews"])
    col4.metric("Monthly Stats", stats["monthly_reviews"])

    st.markdown("---")

    left, right = st.columns([2, 1])

    with left:
        st.subheader("Review Analysis")

        review_text = st.text_area("Customer Review", height=120)

        if st.button("Analyze Review") and review_text.strip():
            try:
                response = requests.post(
                    API_ANALYZE,
                    json={"review": review_text},
                    timeout=60
                )

                if response.status_code == 200:
                    st.session_state.result = response.json()
                else:
                    st.error("Backend error")

            except:
                st.error("Could not connect to backend")

        if "result" in st.session_state:
            r = st.session_state.result

            st.markdown("### Explanation & Similar Reviews")
            st.success(r.get("explanation", "No explanation"))

            st.markdown("#### 📚 Similar Historical Reviews")
            for sim in r.get("similar_reviews", []):
                st.warning(sim)

    with right:
        if "result" in st.session_state:
            r = st.session_state.result

            st.subheader("Detection Result")

            if r.get("prediction") == "Fake":
                st.error(
                    f"🚨 Fake Review — {int(r.get('confidence', 0)*100)}% Confidence"
                )
            else:
                st.success(
                    f"✅ Genuine Review — {int(r.get('confidence', 0)*100)}% Confidence"
                )

            if r.get("suspicious_phrases"):
                st.markdown("**⚠️ Suspicious Phrases Detected**")
                st.write(", ".join(r["suspicious_phrases"]))

        st.markdown("### Recent Review Trends")

        try:
            response = requests.get(API_REVIEWS, timeout=30)
            data = response.json() if response.status_code == 200 else []

            if data:
                df = pd.DataFrame(data)
                df["created_at"] = pd.to_datetime(df["created_at"])
                df["date"] = df["created_at"].dt.date

                grouped = df.groupby(["date", "prediction"]).size().unstack(fill_value=0)
                st.line_chart(grouped)
            else:
                st.info("No review data yet")

        except:
            st.error("Failed to load trends")

elif st.session_state.page == "All Reviews":

    st.markdown("## 📝 All Reviews")

    try:
        response = requests.get(API_REVIEWS, timeout=30)
        data = response.json() if response.status_code == 200 else []

        if not data:
            st.info("No reviews yet")
        else:
            df = pd.DataFrame(data)
            df = df[["review_text", "prediction", "confidence"]]
            df.columns = ["Review", "Prediction", "Confidence"]
            st.dataframe(df, use_container_width=True)

    except:
        st.error("Failed to fetch reviews")

elif st.session_state.page == "Flagged Reviews":

    st.markdown("## 🚩 Flagged Reviews")

    try:
        response = requests.get(API_FLAGGED, timeout=30)
        data = response.json() if response.status_code == 200 else []

        if not data:
            st.info("No flagged reviews yet")
        else:
            df = pd.DataFrame(data)
            df = df[["review_text", "reason", "confidence"]]
            df.columns = ["Review", "Reason", "Confidence"]
            st.dataframe(df, use_container_width=True)

    except:
        st.error("Failed to fetch flagged reviews")

elif st.session_state.page == "Reports":

    st.markdown("## 📊 Reports")

    report_data = pd.DataFrame({
        "Month": ["Jan", "Feb", "Mar", "Apr"],
        "Fake Reviews": [210, 320, 410, 530],
        "Genuine Reviews": [480, 450, 430, 390]
    }).set_index("Month")

    st.bar_chart(report_data)

    st.download_button(
        label="Download Report (CSV)",
        data=report_data.to_csv(),
        file_name="fake_review_report.csv",
        mime="text/csv"
    )