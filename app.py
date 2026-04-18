import streamlit as st
import os

from resume_parser import extract_text
from analytics import calculate_match_score
from storage import upload_to_blob
from language_ai import extract_key_skills

# --------------------------------------------------
# Streamlit Page Configuration
# --------------------------------------------------
st.set_page_config(
    page_title="AI‑Powered Resume Screening",
    page_icon="🤖",
    layout="centered"
)

# --------------------------------------------------
# UI Header
# --------------------------------------------------
st.title("🤖 AI‑Powered Resume Screening App")
st.write(
    "Upload a resume and paste the Job Description. "
    "The app uses **Azure AI Language** to extract skills "
    "and calculate a matching score."
)

st.divider()

# --------------------------------------------------
# User Inputs
# --------------------------------------------------
job_description = st.text_area(
    "📄 Job Description",
    height=200,
    placeholder="Paste the job description here..."
)

uploaded_file = st.file_uploader(
    "📤 Upload Resume (PDF or DOCX)",
    type=["pdf", "docx"]
)

# --------------------------------------------------
# Analyze Button
# --------------------------------------------------
if st.button("🔍 Analyze Resume"):
    if not uploaded_file or not job_description.strip():
        st.error("❌ Please upload a resume and enter the job description.")
    else:
        with st.spinner("Analyzing resume using Azure AI..."):
            # Save uploaded file locally
            file_path = uploaded_file.name
            with open(file_path, "wb") as f:
                f.write(uploaded_file.getbuffer())

            # Extract resume text
            resume_text = extract_text(file_path)

            # Extract skills using Azure AI Language
            resume_skills = extract_key_skills(resume_text)
            jd_skills = extract_key_skills(job_description)

            # Calculate similarity score
            match_score = calculate_match_score(resume_text, job_description)

            # Upload resume to Azure Blob Storage
            upload_to_blob(file_path)

        # --------------------------------------------------
        # Results Section
        # --------------------------------------------------
        st.success(f"✅ Resume Match Score: **{match_score}%**")

        col1, col2 = st.columns(2)

        with col1:
            st.subheader("🧠 Skills Extracted from Resume")
            if resume_skills:
                st.write(resume_skills)
            else:
                st.info("No significant skills detected.")

        with col2:
            st.subheader("📌 Skills from Job Description")
            if jd_skills:
                st.write(jd_skills)
            else:
                st.info("No significant skills detected.")

        # --------------------------------------------------
        # Matched Skills
        # --------------------------------------------------
        matched_skills = set(resume_skills).intersection(set(jd_skills))

        st.subheader("✅ Matched Skills")
        if matched_skills:
            st.write(list(matched_skills))
        else:
            st.warning("No matching skills found.")

        # Cleanup local file
        os.remove(file_path)