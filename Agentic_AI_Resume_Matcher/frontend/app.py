# import streamlit as st
# import requests

# BACKEND_URL = "http://localhost:8000"

# st.set_page_config(page_title="AI Resume Agent", page_icon="🤖")

# st.title("🤖 Agentic AI Resume Matcher")

# st.write("Upload your resume and let the AI agent analyze how well it matches the job description.")

# uploaded_file = st.file_uploader("Upload Resume (PDF)", type=["pdf"])

# job_desc = st.text_area("Enter Job Description")

# if st.button("Analyze Resume"):

#     if uploaded_file is None:
#         st.warning("Please upload a resume")

#     elif job_desc.strip() == "":
#         st.warning("Please enter a job description")

#     else:
#         files = {
#             "file": (uploaded_file.name, uploaded_file.getvalue(), "application/pdf")
#         }

#         upload_response = requests.post(
#             f"{BACKEND_URL}/upload-resume",
#             files=files
#         )

#         if upload_response.status_code != 200:
#             st.error("Resume upload failed")
#         else:
#             file_name = upload_response.json()["file_name"]

#             st.success("Resume uploaded successfully")

#             with st.spinner("AI Agents analyzing your resume..."):

#                 response = requests.post(
#                     f"{BACKEND_URL}/match-resume-agent",
#                     params={"file_name": file_name},
#                     json={"query": job_desc}
#                 )

#                 if response.status_code == 200:

#                     result = response.json()

#                     st.subheader("📊 AI Analysis")

#                     st.write(result["result"])

#                 else:
#                     st.error("Agent analysis failed")



import streamlit as st
import requests

BACKEND_URL = "http://localhost:8000"

st.set_page_config(page_title="AI Resume Matcher", page_icon="🤖", layout="wide")

# ------------------ HEADER ------------------
st.title("🤖 AI Resume Matcher")
st.markdown("Match your resume with job descriptions using AI agents")

# ------------------ INPUT SECTION ------------------
col1, col2 = st.columns(2)

with col1:
    uploaded_file = st.file_uploader("📄 Upload Resume (PDF)", type=["pdf"])

with col2:
    job_desc = st.text_area("📝 Job Description", height=200)

# ------------------ BUTTON ------------------
if st.button("🚀 Analyze Resume", use_container_width=True):

    if uploaded_file is None:
        st.warning("⚠️ Please upload a resume")

    elif job_desc.strip() == "":
        st.warning("⚠️ Please enter a job description")

    else:
        # Upload file
        files = {
            "file": (uploaded_file.name, uploaded_file.getvalue(), "application/pdf")
        }

        with st.spinner("📤 Uploading resume..."):
            upload_response = requests.post(
                f"{BACKEND_URL}/upload-resume",
                files=files
            )

        if upload_response.status_code != 200:
            st.error("❌ Resume upload failed")
        else:
            file_name = upload_response.json()["file_name"]

            st.success("✅ Resume uploaded successfully")

            # Analyze
            with st.spinner("🤖 AI is analyzing your resume..."):

                response = requests.post(
                    f"{BACKEND_URL}/match-resume-agent",
                    params={"file_name": file_name},
                    json={"query": job_desc}
                )

            if response.status_code == 200:
                result = response.json()

                st.divider()

                st.subheader("📊 Analysis Result")

                # Match Score
                score = int(result["match_score"].replace("%", "").strip())
                st.metric("🎯 Match Score", f"{score}%")
                st.progress(score / 100)

                st.divider()

                            # Columns layout
                col1, col2 = st.columns(2)

                            # Matching Skills
                with col1:
                    st.markdown("### ✅ Matching Skills")
                    skills = result["matching_skills"].split(",")
                    for skill in skills:
                        st.markdown(f"- {skill.strip()}")

                            # Missing Skills
                with col2:
                    st.markdown("### ❌ Missing Skills")
                    skills = result["missing_skills"].split(",")
                    for skill in skills:
                        st.markdown(f"- {skill.strip()}")

                st.divider()

                            # Final Recommendation
                st.markdown("### 🧠 Final Recommendation")
                st.info(result["final_recommendation"])