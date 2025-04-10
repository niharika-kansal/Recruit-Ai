# app.py
import streamlit as st
import os
from job_parser import parse_jobs
from resume_parser import parse_resume_folder
from ollama_interface import match_resumes_to_jobs

st.set_page_config(page_title="Resume Matcher Dashboard", layout="wide")
st.title("🔍 Resume Matcher Dashboard")

# File paths
data_folder = "data"
resume_folder = os.path.join(data_folder, "resumes")
job_file = os.path.join(data_folder, "job_description.csv")

# Load jobs and resumes
jobs = parse_jobs(job_file)
resumes = parse_resume_folder(resume_folder)

# Match using Ollama
if st.button("Match Resumes to Jobs"):
    with st.spinner("Running LLM matching using Ollama..."):
        matches = match_resumes_to_jobs(jobs, resumes)

    st.success("Matching complete!")

    for job_title, match_data in matches.items():
        st.subheader(f"Job: {job_title}")
        top_candidate = match_data[0]

        st.markdown(f"**Best Match:** {top_candidate['name']}")
        st.markdown(f"**Score:** {top_candidate['score']} / 100")
        st.markdown(f"**Reasoning:** {top_candidate['reasoning']}")
        st.divider()
else:
    st.info("Click the button above to start matching.")
