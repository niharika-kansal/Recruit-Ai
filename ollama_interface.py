# ollama_interface.py
import subprocess
import json
import streamlit as st
import re
import requests


OLLAMA_API = "https://6b74-117-203-246-41.ngrok-free.app" 

def query_ollama(prompt, model="phi3"):
    try:
        st.info("Querying remote Ollama...")
        response = requests.post(
            f"{OLLAMA_API}/api/generate",
            headers={ "ngrok-skip-browser-warning": "true" },
            json={
                "model": model,
                "prompt": prompt,
                "stream": False
            },
            timeout=60
        )
        response.raise_for_status()
        raw = response.json().get("response", "")
        match = re.search(r'\{.*?\}', raw, re.DOTALL)
        if not match:
            raise ValueError("No valid JSON found in response.")
        return match.group(0)

    except Exception as e:
        st.error(f"Failed to query remote Ollama: {e}")
        return json.dumps({
            "name": "Unknown",
            "score": 0,
            "reasoning": f"Ollama error: {str(e)}"
        })


    except Exception as e:
        st.error(f"Failed to query remote Ollama: {e}")
        return json.dumps({
            "name": "Unknown",
            "score": 0,
            "reasoning": f"Ollama error: {str(e)}"
        })

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