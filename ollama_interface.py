# ollama_interface.py
import subprocess
import json
import streamlit as st
import re

def query_ollama(prompt, model="llama3"):
    try:
        print("[DEBUG] Sending prompt to Ollama...")
        st.info("Sending prompt to Ollama...")
        result = subprocess.run(
            ["ollama", "run", model],
            input=prompt.encode(),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=60
        )
        output = result.stdout.decode()
        print("[DEBUG] Received response from Ollama.")
        st.success("Received response from Ollama.")
        return output
    except Exception as e:
        error_msg = f"[ERROR] Ollama invocation failed: {e}"
        print(error_msg)
        st.error(error_msg)
        return json.dumps({"name": "Unknown", "score": 0, "reasoning": f"LLM error: {str(e)}"})

def match_resumes_to_jobs(jobs, resumes):
    matches = {}
    for job in jobs:
        job_title = job['title']
        job_desc = job['description']
        job_matches = []

        msg = f"[DEBUG] Matching resumes for job: {job_title}"
        print(msg)
        st.subheader(job_title)
        st.write("Matching resumes...")

        for res in resumes:
            prompt = f"""
You are an expert recruiter.

Given the following job description and resume, rate the candidate's fit from 0 to 100 and explain your reasoning in 2-3 sentences.

Job Description:
{job_desc}

Resume:
{res['content']}

Respond in this format:
{{"name": "{res['name']}", "score": <score>, "reasoning": "<reason>"}}
"""
            try:
                output = query_ollama(prompt)
                json_match = re.search(r'\{.*?\}', output, re.DOTALL)
                if json_match:
                    response = json.loads(json_match.group(0))
                else:
                    raise ValueError("No valid JSON found in LLM response.")
                job_matches.append(response)
                score_msg = f"[DEBUG] Scored {res['name']} for job '{job_title}': {response.get('score', '?')} points"
                print(score_msg)
                st.write(f"{res['name']}: {response.get('score', '?')} - {response.get('reasoning', '')}")
            except Exception as e:
                error_msg = f"[ERROR] Failed to match {res['name']} to job '{job_title}': {e}"
                print(error_msg)
                st.error(error_msg)
                job_matches.append({"name": res['name'], "score": 0, "reasoning": f"Error: {str(e)}"})

        job_matches.sort(key=lambda x: x['score'], reverse=True)
        matches[job_title] = job_matches

    return matches
