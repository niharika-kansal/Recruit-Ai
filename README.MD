# 💼 Recruit AI

> Match the best candidates to your job descriptions using Ollama and Streamlit — powered by LLM magic ✨

![demo](https://media4.giphy.com/media/v1.Y2lkPTc5MGI3NjExZm5tZmRpNmZmZ2hjb2c5cGFxNjUyajBrcGxhODcxeXA1dWE2Z3FnZSZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/emHFjFhg9Ha0wQjihU/giphy.gif)

---

## 🚀 What It Does

This app helps recruiters, HR teams, or anyone hiring to:
- 📥 Upload a CSV of job descriptions
- 📂 Upload multiple PDF resumes
- ✅ Select the jobs you want to match
- 🤖 Use a local Ollama LLM to score each resume per job
- 🏆 See the top candidate per role with reasoning

---

## 🧠 How It Works

```mermaid
sequenceDiagram
    actor User
    participant Streamlit as UI
    participant Parser as Resume/Job Parser
    participant Ollama as Local LLM

    User->>Streamlit: Upload CSV + Resumes
    Streamlit->>Parser: Parse job + resumes
    Streamlit->>User: Select jobs to match
    Streamlit->>Ollama: Send job + resume prompt
    Ollama-->>Streamlit: Return score + reasoning
    Streamlit->>User: Show best candidate per job
