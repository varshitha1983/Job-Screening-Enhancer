# app.py (Real-Time Job Screening Frontend)
import streamlit as st
import requests
import pandas as pd
import sys
import os

# Add the parent directory (project root) to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from backend.database.db import get_shortlisted_candidates
from backend.modules.matcher import store_shortlisted_to_sqlite

BACKEND_URL = "http://localhost:8000"

st.set_page_config(page_title="Real-Time Job Screening", layout="wide")
st.title("🧪 Real-Time Job Screening Dashboard")

# Layout
st.markdown("### 📄 Job Role/Position")
job_role = st.text_input("Enter Job Role", placeholder="e.g., Backend Developer")

st.markdown("### 📄 Job Description")
jd_text = st.text_area("Paste job description text here", height=200)

st.markdown("### 📤 Upload Resumes")
resume_files = st.file_uploader("Upload one or more resumes (PDF format)", type=["pdf"], accept_multiple_files=True)

threshold = st.slider("🎯 Match Score Threshold (%)", min_value=0, max_value=100, value=75)

if jd_text and resume_files:
    with st.spinner("⏳ Processing resumes..."):
        try:
            # 1. Summarize JD
            jd_response = requests.post(
                f"{BACKEND_URL}/summarize-jd/",
                json={"jd_text": jd_text}
            )
            jd_response.raise_for_status()
            jd_summary = jd_response.json().get("summary")
            st.success("✅ Job description summarized!")
            st.markdown(f"**Summarized JD:** _{jd_summary}_")

            # 2. Parse resumes
            files = [("files", (file.name, file.read(), "application/pdf")) for file in resume_files]
            upload_response = requests.post(
                f"{BACKEND_URL}/parse-resumes/",
                files=files
            )
            upload_response.raise_for_status()
            parsed_resumes = upload_response.json().get("parsed_resumes", [])
            st.success(f"✅ {len(parsed_resumes)} resumes uploaded and parsed.")
            st.markdown(f"**Parsed CV:** _{parsed_resumes}_")
            # 3. Match resumes
            # Your current summarized JD is in a dict
            # Turn it into a single string
            def flatten_summary_dict(summary_dict):
                return " ".join([f"{k}: {v}" for k, v in summary_dict.items()])
            
            summary_text = flatten_summary_dict(jd_summary)  # Convert dict to string


            
            match_payload = {
                "summary_text": summary_text,
                "parsed_resumes": parsed_resumes,
                "job_role": job_role,
                "threshold": threshold / 100
            }
            match_response = requests.post(
                f"{BACKEND_URL}/match-resumes/",
                json=match_payload
            )
            match_response.raise_for_status()
            
            result_data = match_response.json()
            matched_df = pd.DataFrame(result_data.get("matches", []))
            matched_df = matched_df[matched_df["Score"] > 0.75]
            store_shortlisted_to_sqlite(matched_df)

            # Read from DB
            shortlisted_df = get_shortlisted_candidates(job_role)

            if shortlisted_df.empty:
                st.warning("⚠️ No candidates have been shortlisted yet.")
            else:
                st.success(f"🎯 Below are the results with match scores and shortlist status for each candidate!")
                st.dataframe(shortlisted_df)


                # 4. Email shortlisted candidates
                right_col = st.columns([6, 1])  # Adjust the ratio to shift button further right

                with right_col[1]:
                    st.markdown(
                        """
                        <style>
                        div.stButton > button:first-child {
                            background-color: #28a745;
                            color: white;
                            float: right;
                        }
                        </style>
                        """,
                        unsafe_allow_html=True,
                    )
                    if st.button("📨 Send Emails to Shortlisted Candidates"):
                        email_response = requests.post(f"{BACKEND_URL}/send-emails/")
                        if email_response.status_code == 200:
                            st.success(email_response.json().get("message"))
                            st.balloons()
                        else:
                            st.error(email_response.json().get("error", "Email sending failed."))

        except requests.exceptions.RequestException as e:
            st.error(f"❌ Error: {str(e)}")
            if hasattr(e, 'response') and e.response is not None:
                st.error(f"Server response: {e.response.text}")