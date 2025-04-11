resume-matcher-app/
│
├── app.py                      # 🚀 Main Streamlit dashboard
├── requirements.txt            # 📦 Dependencies for Streamlit Cloud
│
├── job_parser.py               # 🔍 Parses job_description.csv
├── resume_parser.py            # 📄 Extracts text from resume PDFs
├── ollama_interface.py         # 🧠 Sends prompts to Ollama LLM API
│
├── utils/                      # 🔧 (Optional) Extra helpers
│   └── formatting.py           # Custom UI or formatting utils
│
├── assets/                     # 🎨 (Optional) Custom CSS/images/icons
│   └── style.css               # Custom styles (if you split them out)
│
├── data/                       # 📂 Default folder to store job/resume examples (not needed on Streamlit Cloud)
│   ├── job_description.csv
│   └── resumes/
│       ├── resume1.pdf
│       ├── resume2.pdf
│       └── ...
│
└── README.md                   # 📘 Docs for GitHub
