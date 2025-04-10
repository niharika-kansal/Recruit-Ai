# job_parser.py
import pandas as pd


def parse_jobs(csv_path):
    # Try multiple encodings due to possible Windows CSV artifacts
    for encoding in ['utf-8', 'utf-8-sig', 'latin1']:
        try:
            df = pd.read_csv(csv_path, encoding=encoding)
            break
        except UnicodeDecodeError:
            continue

    jobs = []
    for _, row in df.iterrows():
        jobs.append({
            "title": row.get("Job Title", "Unknown"),
            "description": row.get("Job Description", "")
        })
    return jobs

