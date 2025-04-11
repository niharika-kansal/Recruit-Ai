# app.py
import streamlit as st
import os
import tempfile
import shutil
import pandas as pd

from job_parser import parse_jobs
from resume_parser import parse_resume_folder
from ollama_interface import match_resumes_to_jobs

st.set_page_config(page_title="RecruitAI Dashboard", layout="wide")
st.title("RecruitAI Dashboard")
st.caption("Upload job descriptions and resumes to find the best candidates 💡")

# File paths
temp_dir = tempfile.mkdtemp()
resume_folder = os.path.join(temp_dir, "resumes")
os.makedirs(resume_folder, exist_ok=True)

# File upload widgets
uploaded_job_file = st.file_uploader("📄 Upload Job Description CSV", type="csv")
uploaded_resumes = st.file_uploader("📁 Upload Resume PDFs", type="pdf", accept_multiple_files=True)

if uploaded_job_file:
    job_path = os.path.join(temp_dir, "job_description.csv")
    with open(job_path, "wb") as f:
        f.write(uploaded_job_file.read())

    for resume_file in uploaded_resumes or []:
        with open(os.path.join(resume_folder, resume_file.name), "wb") as f:
            f.write(resume_file.read())

    # Load jobs and resumes
    jobs = parse_jobs(job_path)
    job_titles = [job['title'] for job in jobs]

    # Select jobs to match
    selected_job_titles = st.multiselect("✅ Select jobs to match candidates for", job_titles, default=job_titles)
    selected_jobs = [job for job in jobs if job['title'] in selected_job_titles]

    resumes = parse_resume_folder(resume_folder)

    if st.button("🚀 Match Resumes to Selected Jobs", use_container_width=True):
        with st.spinner("Matching in progress using Ollama..."):
            matches = match_resumes_to_jobs(selected_jobs, resumes)

        st.success("✅ Matching complete!")

        best_candidates = {}

        for job_title, match_data in matches.items():
            top_candidate = match_data[0]
            best_candidates[job_title] = top_candidate

            st.markdown("""
                <div style='background-color:#f9f9f9; padding:1.5rem; border-radius:1rem; margin-bottom:1rem; box-shadow: 0 0 5px rgba(0,0,0,0.1);'>
            """, unsafe_allow_html=True)

            st.markdown(f"### 🧑‍💼 Job: `{job_title}`")
            st.markdown(f"**🏅 Best Match:** `{top_candidate['name']}`")
            st.markdown(f"**📊 Score:** `{top_candidate['score']} / 100`")
            st.markdown(f"**📝 Reasoning:** {top_candidate['reasoning']}")

            st.markdown("""</div>""", unsafe_allow_html=True)

            with st.expander("🔍 See all candidates"):
                for match in match_data:
                    st.markdown(f"**{match['name']}** — {match['score']}/100")
                    st.caption(match['reasoning'])
                    st.markdown("---")

        # Summary section
        st.markdown("## 🏆 Best Candidates Across Selected Jobs")
        for job, candidate in best_candidates.items():
            st.markdown(f"- **{job}** → **{candidate['name']}** ({candidate['score']}/100)")
else:
    st.info("⬆️ Upload a job_description.csv file and resumes to begin matching.")
