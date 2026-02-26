🤖 AI Hiring Intelligence Platform

A Production-Ready ATS + Job Description-Based Resume Analyzer built using Streamlit + OpenAI + LangChain.

This intelligent system evaluates resumes, calculates ATS scores, performs JD matching, and provides AI-powered resume improvement suggestions.

🚀 Features
📊 ATS Resume Scoring

Calculates overall ATS score

Evaluates structure, keyword density, formatting, and impact metrics

Provides improvement recommendations

💼 JD-Based Matching

Generate Job Description from a job role

Paste custom Job Description

Compare resume against JD

Identify:

Matching skills

Missing keywords

Weak areas

🧠 AI-Powered Resume Optimization

Resume rewrite suggestions

Section improvement recommendations

Interview readiness evaluation

Final hiring verdict

🛠 Tech Stack

Frontend: Streamlit

LLM Integration: OpenAI GPT-4 Turbo

Framework: LangChain

PDF Parsing: PyPDFLoader

Environment Management: python-dotenv

📂 Project Structure
AI-Hiring-Intelligence/
│
├── app.py
├── .env
├── requirements.txt
└── README.md
⚙️ Installation & Setup
1️⃣ Clone Repository
git clone https://github.com/your-username/AI-Hiring-Intelligence.git
cd AI-Hiring-Intelligence
2️⃣ Create Virtual Environment
python -m venv venv
source venv/bin/activate  # Mac/Linux
venv\Scripts\activate     # Windows
3️⃣ Install Dependencies
pip install -r requirements.txt
4️⃣ Add OpenAI API Key

Create a .env file:

OPENAI_API_KEY=your_api_key_here
5️⃣ Run Application
streamlit run app.py
🖥 Application Modes
1️⃣ Resume Only Mode

Evaluates resume quality

Returns ATS score

Suggests improvements

2️⃣ Generate JD Mode

Enter job role

AI generates professional job description

Resume compared against generated JD

3️⃣ Custom JD Mode

Paste real job description

Get JD-specific ATS score

📊 Output Example (JSON Structure)
{
  "ats_breakdown": {
    "overall_score": 82
  },
  "matching_skills": [],
  "missing_keywords": [],
  "weak_areas": [],
  "resume_rewrite_examples": [],
  "section_improvements": [],
  "interview_readiness": "",
  "final_verdict": ""
}
🧠 How It Works

Resume uploaded as PDF

Text extracted using PyPDFLoader

LLM prompt constructed dynamically

GPT-4 Turbo analyzes resume

Structured JSON response returned

Streamlit displays score and insights

🎯 Use Cases

Students preparing for placements

AI/ML Engineers optimizing resumes

Career coaches

HR teams for quick screening

Freelance resume optimization services

🔐 Environment Variables
Variable	Description
OPENAI_API_KEY	Required for LLM access
📌 Future Improvements (Planned)

Embedding-based semantic similarity scoring

Keyword density visualization chart

Section-wise ATS scoring

Resume version comparison

Downloadable PDF report

Multi-agent evaluation system

RAG-based skill benchmarking