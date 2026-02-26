"""
<<<<<<< HEAD
AI Hiring Intelligence Platform
Production-Ready ATS + JD-Based Resume Analyzer
Single Page Application
=======
AI Resume Screener - Production Ready
Intelligent resume screening powered by LangChain & Groq
>>>>>>> cb1078669a78c034caae61b925307ef40c626ce0
"""

import streamlit as st
import os
import json
<<<<<<< HEAD
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_community.document_loaders import PyPDFLoader

load_dotenv()

# ----------------------------
# PAGE CONFIG
# ----------------------------
st.set_page_config(
    page_title="AI Hiring Intelligence Platform",
    page_icon="🤖",
    layout="wide"
)

st.markdown("<h1 style='text-align:center;'>🤖 AI Hiring Intelligence Platform</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center;color:gray;'>ATS Score • JD Matching • Resume Optimization</p>", unsafe_allow_html=True)

# ----------------------------
# LOAD API
# ----------------------------
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    st.error("Please add OPENAI_API_KEY in .env file")
    st.stop()

llm = ChatOpenAI(
    api_key=api_key,
    model_name="gpt-4-turbo",
    temperature=0.2
)

# ----------------------------
# JD GENERATOR FUNCTION
# ----------------------------
def generate_job_description(role: str):
    jd_prompt = PromptTemplate(
        input_variables=["role"],
        template="""
Create a professional job description for:

Role: {role}

Include:
- Role Summary
- Key Responsibilities
- Required Technical Skills
- Experience Requirements
"""
    )
    chain = jd_prompt | llm
    result = chain.invoke({"role": role})
    return result.content.strip()

# ----------------------------
# INPUT SECTION
# ----------------------------
uploaded_file = st.file_uploader("📄 Upload Resume (PDF)", type=["pdf"])

st.markdown("### 💼 Optional: Job Description")

jd_option = st.radio(
    "Select Mode:",
    ["Resume Only (General ATS Score)", "Generate from Job Role", "Paste Custom Job Description"],
    horizontal=True
)

job_role = ""
job_description = ""

if jd_option == "Generate from Job Role":
    job_role = st.text_input("Enter Job Role")
elif jd_option == "Paste Custom Job Description":
    job_description = st.text_area("Paste Full Job Description", height=200)

analyze = st.button("🔍 Analyze Resume", use_container_width=True)

# =====================================================
# MAIN EXECUTION
# =====================================================
if analyze:

    if not uploaded_file:
        st.error("Please upload resume.")
        st.stop()

    # Extract Resume
    os.makedirs("temp", exist_ok=True)
    temp_path = f"temp/{uploaded_file.name}"

    with open(temp_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    loader = PyPDFLoader(temp_path)
    pages = loader.load()
    resume_text = "\n".join([p.page_content for p in pages])

    if len(resume_text.strip()) < 100:
        st.error("Unable to extract meaningful resume content.")
        st.stop()

    # -------------------------------------------------
    # MODE SELECTION
    # -------------------------------------------------
    if jd_option == "Paste Custom Job Description" and job_description:
        final_jd = job_description
        mode = "jd_match"

    elif jd_option == "Generate from Job Role" and job_role:
        with st.spinner("Generating Job Description..."):
            final_jd = generate_job_description(job_role)
        mode = "jd_match"

    else:
        mode = "resume_only"

    # -------------------------------------------------
    # PROMPT BASED ON MODE
    # -------------------------------------------------
    if mode == "jd_match":

        prompt = PromptTemplate(
            input_variables=["resume", "jd"],
            template="""
Analyze resume against job description.

Return JSON:

{{
 "ats_breakdown": {{
    "overall_score": 0
 }},
 "matching_skills": [],
 "missing_keywords": [],
 "weak_areas": [],
 "resume_rewrite_examples": [
    {{"original": "", "improved": ""}}
 ],
 "section_improvements": [],
 "interview_readiness": "",
 "final_verdict": ""
}}

Resume:
{resume}

Job Description:
{jd}
"""
        )

        chain = prompt | llm
        result = chain.invoke({
            "resume": resume_text[:6000],
            "jd": final_jd
        })

    else:
        # Resume-only ATS mode
        prompt = PromptTemplate(
            input_variables=["resume"],
            template="""
Evaluate this resume for overall ATS quality without job description.

Consider:
- Structure
- Keyword density
- Impact metrics
- Technical clarity
- Formatting

Return JSON:

{{
 "ats_breakdown": {{
    "overall_score": 0
 }},
 "matching_skills": [],
 "missing_keywords": [],
 "weak_areas": [],
 "resume_rewrite_examples": [
    {{"original": "", "improved": ""}}
 ],
 "section_improvements": [],
 "interview_readiness": "",
 "final_verdict": ""
}}

Resume:
{resume}
"""
        )

        chain = prompt | llm
        result = chain.invoke({
            "resume": resume_text[:6000]
        })

    # -------------------------------------------------
    # Parse JSON
    # -------------------------------------------------
    response_text = result.content.strip()

    if response_text.startswith("```"):
        response_text = response_text.split("```")[1]
        if response_text.startswith("json"):
            response_text = response_text[4:]
        response_text = response_text.strip()

    try:
        analysis = json.loads(response_text)
    except:
        st.error("Error parsing LLM response.")
        st.stop()

    # -------------------------------------------------
    # RESULTS DISPLAY
    # -------------------------------------------------
    tab1, tab2, tab3 = st.tabs([
        "📊 ATS Score",
        "🧠 Insights",
        "🚀 Resume Optimization"
    ])

    with tab1:
        st.metric("Overall ATS Score", f"{analysis['ats_breakdown']['overall_score']}%")

    with tab2:
        for s in analysis["weak_areas"]:
            st.write(f"- {s}")

    with tab3:
        for r in analysis["resume_rewrite_examples"]:
            st.write(f"Original: {r['original']}")
            st.write(f"Improved: {r['improved']}")
            st.markdown("---")

    os.remove(temp_path)
=======
from typing import Dict
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

load_dotenv()

st.set_page_config(
    page_title="AI Resume Screener",
    page_icon="📄",
    layout="wide"
)

# Custom CSS for clean, professional white theme
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    
    /* Global Styles */
    * {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
    }
    
    /* Main App Background - Pure White */
    .stApp {
        background-color: #FFFFFF;
        color: #000000;
    }
    
    /* Main Container */
    .main .block-container {
        max-width: 1200px;
        padding: 2rem 1rem;
    }
    
    /* Header Styles */
    .main-header {
        font-size: 2.5rem;
        font-weight: 700;
        color: #000000;
        text-align: center;
        margin-bottom: 0.5rem;
        letter-spacing: -0.5px;
    }
    
    .sub-header {
        font-size: 1.1rem;
        text-align: center;
        color: #6B7280;
        margin-bottom: 2.5rem;
        font-weight: 400;
    }
    
    /* Section Headers */
    .section-header {
        font-size: 1.25rem;
        font-weight: 600;
        color: #111827;
        margin-bottom: 1rem;
        padding-bottom: 0.5rem;
        border-bottom: 2px solid #E5E7EB;
    }
    
    /* Card Containers */
    .card {
        background: #FFFFFF;
        border: 1px solid #E5E7EB;
        border-radius: 8px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.1);
    }
    
    .card:hover {
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        transition: box-shadow 0.2s ease;
    }
    
    /* Result Sections */
    .result-section {
        background: #F9FAFB;
        border: 1px solid #E5E7EB;
        border-radius: 8px;
        padding: 1.5rem;
        margin: 1rem 0;
    }
    
    .result-section h3 {
        color: #111827;
        font-weight: 600;
        font-size: 1.1rem;
        margin-bottom: 1rem;
        margin-top: 0;
    }
    
    .result-section p, .result-section li {
        color: #374151;
        font-size: 0.95rem;
        line-height: 1.6;
    }
    
    .result-section ul {
        margin: 0.5rem 0;
        padding-left: 1.5rem;
    }
    
    .result-section li {
        margin: 0.5rem 0;
    }
    
    /* Metric Cards */
    .metric-card {
        background: #FFFFFF;
        border: 2px solid #E5E7EB;
        border-radius: 8px;
        padding: 1.5rem;
        margin: 1rem 0;
        text-align: center;
    }
    
    /* Recommendation Styles */
    .strong-fit {
        color: #059669;
        font-weight: 700;
        font-size: 1.5rem;
    }
    
    .moderate-fit {
        color: #D97706;
        font-weight: 700;
        font-size: 1.5rem;
    }
    
    .not-fit, .weak-fit {
        color: #DC2626;
        font-weight: 700;
        font-size: 1.5rem;
    }
    
    /* Sidebar Styling */
    [data-testid="stSidebar"] {
        background-color: #F9FAFB;
        border-right: 1px solid #E5E7EB;
    }
    
    [data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3 {
        color: #111827;
        font-weight: 600;
    }
    
    [data-testid="stSidebar"] p {
        color: #4B5563;
        font-size: 0.9rem;
    }
    
    /* Input Fields */
    .stTextInput input, .stTextArea textarea {
        background: #FFFFFF !important;
        border: 1px solid #D1D5DB !important;
        border-radius: 6px !important;
        color: #000000 !important;
        padding: 0.75rem !important;
        font-size: 0.95rem !important;
    }
    
    .stTextInput input::placeholder, .stTextArea textarea::placeholder {
        color: #9CA3AF !important;
    }
    
    .stTextInput input:focus, .stTextArea textarea:focus {
        border-color: #2563EB !important;
        box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.1) !important;
        outline: none !important;
    }
    
    /* Input Labels */
    .stTextInput label, .stTextArea label, .stFileUploader label {
        color: #111827 !important;
        font-weight: 500 !important;
        font-size: 0.95rem !important;
        margin-bottom: 0.5rem !important;
    }
    
    /* File Uploader */
    [data-testid="stFileUploader"] {
        background: #F9FAFB;
        border: 2px dashed #D1D5DB;
        border-radius: 8px;
        padding: 2rem;
    }
    
    [data-testid="stFileUploader"]:hover {
        border-color: #2563EB;
        background: #EFF6FF;
    }
    
    /* File uploader button */
    [data-testid="stFileUploader"] button {
        background: #2563EB !important;
        color: white !important;
        border: none !important;
        border-radius: 6px !important;
        padding: 0.625rem 1.25rem !important;
        font-weight: 500 !important;
        font-size: 0.95rem !important;
    }
    
    [data-testid="stFileUploader"] button:hover {
        background: #1D4ED8 !important;
    }
    
    /* Uploaded file display */
    [data-testid="stFileUploader"] section {
        color: #111827 !important;
    }
    
    [data-testid="stFileUploader"] section > div {
        background: #FFFFFF !important;
        border: 1px solid #E5E7EB !important;
        border-radius: 6px !important;
        padding: 0.75rem !important;
        margin-top: 0.75rem !important;
    }
    
    [data-testid="stFileUploader"] section > div > div {
        color: #111827 !important;
        font-size: 0.95rem !important;
        font-weight: 500 !important;
    }
    
    [data-testid="stFileUploader"] small {
        color: #6B7280 !important;
        font-size: 0.875rem !important;
    }
    
    /* Buttons */
    .stButton button {
        background: #2563EB !important;
        color: white !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 0.75rem 2rem !important;
        font-weight: 600 !important;
        font-size: 1rem !important;
        transition: background 0.2s ease !important;
    }
    
    .stButton button:hover {
        background: #1D4ED8 !important;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1) !important;
    }
    
    /* Metrics */
    [data-testid="stMetricValue"] {
        font-size: 2.5rem !important;
        font-weight: 700 !important;
        color: #111827 !important;
    }
    
    [data-testid="stMetricLabel"] {
        color: #6B7280 !important;
        font-size: 0.95rem !important;
        font-weight: 500 !important;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    /* Expander */
    .streamlit-expanderHeader {
        background: #F9FAFB !important;
        border: 1px solid #E5E7EB !important;
        border-radius: 6px !important;
        color: #111827 !important;
        font-weight: 500 !important;
    }
    
    .streamlit-expanderHeader:hover {
        background: #F3F4F6 !important;
    }
    
    .streamlit-expanderContent {
        border: 1px solid #E5E7EB !important;
        border-top: none !important;
        background: #FFFFFF !important;
    }
    
    /* Success/Error/Warning/Info Messages */
    .stSuccess {
        background: #ECFDF5 !important;
        border: 1px solid #10B981 !important;
        border-radius: 6px !important;
        color: #065F46 !important;
    }
    
    .stError {
        background: #FEF2F2 !important;
        border: 1px solid #EF4444 !important;
        border-radius: 6px !important;
        color: #991B1B !important;
    }
    
    .stWarning {
        background: #FFFBEB !important;
        border: 1px solid #F59E0B !important;
        border-radius: 6px !important;
        color: #92400E !important;
    }
    
    .stInfo {
        background: #EFF6FF !important;
        border: 1px solid #3B82F6 !important;
        border-radius: 6px !important;
        color: #1E40AF !important;
    }
    
    /* Checkbox */
    .stCheckbox {
        color: #111827 !important;
    }
    
    .stCheckbox label {
        color: #111827 !important;
        font-size: 0.95rem !important;
        font-weight: 400 !important;
    }
    
    /* Headers and Headings */
    h1, h2, h3, h4, h5, h6 {
        color: #111827 !important;
        font-weight: 600 !important;
    }
    
    /* Markdown text */
    .stMarkdown {
        color: #111827 !important;
    }
    
    .stMarkdown p {
        color: #374151 !important;
        line-height: 1.6;
    }
    
    .stMarkdown strong, .stMarkdown b {
        color: #111827 !important;
        font-weight: 600 !important;
    }
    
    /* List items */
    ul li, ol li {
        color: #374151 !important;
        margin: 0.25rem 0;
    }
    
    /* Divider */
    hr {
        border: none;
        height: 1px;
        background: #E5E7EB;
        margin: 2rem 0;
    }
    
    /* Scrollbar */
    ::-webkit-scrollbar {
        width: 8px;
        height: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: #F3F4F6;
    }
    
    ::-webkit-scrollbar-thumb {
        background: #D1D5DB;
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: #9CA3AF;
    }
    
    /* Code blocks */
    code {
        font-family: 'Monaco', 'Menlo', monospace !important;
        background: #F3F4F6 !important;
        padding: 0.2rem 0.4rem !important;
        border-radius: 3px !important;
        color: #111827 !important;
        font-size: 0.875rem !important;
    }
    
    /* Spinner */
    .stSpinner > div {
        border-top-color: #2563EB !important;
    }
    
    /* Remove default Streamlit branding colors */
    .stApp header {
        background: transparent !important;
    }
    
    /* Ensure all text is readable */
    p, span, div, label {
        color: #111827;
    }
    
    /* Section spacing */
    .element-container {
        margin-bottom: 0.5rem;
    }
    </style>
""", unsafe_allow_html=True)


class ResumeScreener:
    """Main class for resume screening functionality"""
    
    def __init__(self, groq_api_key: str):
        """Initialize the screener with Groq API"""
        self.llm = ChatGroq(
            groq_api_key=groq_api_key,
            model_name="llama-3.3-70b-versatile",  # Updated to current supported model
            temperature=0.2,  # Lower temperature for consistent, factual outputs
            max_tokens=2048
        )
    
    def extract_text_from_pdf(self, pdf_path: str) -> str:
        """
        Extract text from PDF using LangChain's PyPDFLoader
        
        Args:
            pdf_path: Path to the PDF file
            
        Returns:
            Extracted text content
        """
        try:
            loader = PyPDFLoader(pdf_path)
            pages = loader.load()
            
            if not pages:
                return ""
            
            # Combine all pages
            full_text = "\n\n".join([page.page_content for page in pages])
            return full_text.strip()
        
        except Exception as e:
            st.error(f"Error extracting PDF text: {str(e)}")
            return ""
    
    def split_text(self, text: str, chunk_size: int = 4000, chunk_overlap: int = 200) -> list:
        """
        Split text into chunks to avoid token overflow
        
        Args:
            text: Input text to split
            chunk_size: Maximum size of each chunk
            chunk_overlap: Overlap between chunks
            
        Returns:
            List of text chunks
        """
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            length_function=len,
            separators=["\n\n", "\n", " ", ""]
        )
        chunks = text_splitter.split_text(text)
        return chunks
    
    def generate_job_description(self, job_role: str) -> str:
        """
        Generate a realistic job description based on the job role
        
        Args:
            job_role: Job title/role
            
        Returns:
            Generated job description
        """
        jd_prompt = PromptTemplate(
            input_variables=["job_role"],
            template="""You are an HR professional creating a realistic job description.

Job Role: {job_role}

Create a professional job description that includes:
1. Brief role overview (2-3 sentences)
2. Key Responsibilities (4-6 bullet points)
3. Required Technical Skills (5-8 specific skills)
4. Required Experience (years and type)
5. Educational Requirements
6. Preferred Qualifications (2-3 items)

Make it realistic and aligned with industry standards for this role as seen on LinkedIn, Naukri, or Indeed.
Do not be overly generic. Include specific technologies and tools relevant to this role.

Job Description:"""
        )
        
        # Use LCEL (LangChain Expression Language) instead of deprecated LLMChain
        chain = jd_prompt | self.llm
        
        try:
            result = chain.invoke({"job_role": job_role})
            return result.content.strip()
        except Exception as e:
            st.error(f"Error generating job description: {str(e)}")
            return f"Error generating job description for {job_role}"
    
    def analyze_resume(self, resume_text: str, job_description: str) -> Dict:
        """
        Analyze resume against job description using LangChain
        
        Args:
            resume_text: Extracted resume text
            job_description: Job description to match against
            
        Returns:
            Dictionary containing analysis results
        """
        # If resume is too long, use first chunk
        chunks = self.split_text(resume_text)
        resume_content = chunks[0] if chunks else resume_text
        
        analysis_prompt = PromptTemplate(
            input_variables=["resume", "job_description"],
            template="""You are an expert AI Resume Screener, ATS System, and Technical Recruiter.

Your goal is to analyze a candidate's resume against a given job role or full job description
and provide accurate, practical, and industry-relevant feedback.

TASKS:
1. Extract core skills, tools, technologies, experience, and projects from the resume.
2. Compare them strictly with the job requirements.
3. Calculate a realistic ATS-style match score (0–100%).
4. Identify strengths that directly match the role.
5. Identify missing or weak skills.
6. Provide clear, actionable resume improvement suggestions.
7. Give a final hiring verdict.

RULES:
- Be concise and professional.
- Avoid generic advice.
- Focus on ATS keywords and real recruiter expectations.
- No hallucination; use only resume content.
- Use bullet points for clarity.
- Be specific with examples from the resume.
- Consider years of experience, project complexity, and skill depth.

JOB DESCRIPTION:
{job_description}

CANDIDATE RESUME:
{resume}

Provide a structured analysis in the following JSON format:

{{
    "match_percentage": <number between 0-100, realistic ATS score>,
    "matching_skills": ["skill1 with context", "skill2 with context", ...],
    "missing_skills": ["critical skill 1", "important skill 2", ...],
    "weak_skills": ["skill that needs improvement", ...],
    "experience_relevance": "<detailed assessment of years and type of experience>",
    "education_relevance": "<assessment of educational background>",
    "strengths": [
        "Specific strength with evidence from resume",
        "Another strength with quantifiable achievement",
        ...
    ],
    "weaknesses": [
        "Specific gap or weakness",
        "Area needing improvement",
        ...
    ],
    "improvement_suggestions": [
        "Actionable suggestion 1",
        "Actionable suggestion 2",
        ...
    ],
    "ats_keywords": [
        "Missing ATS keyword 1",
        "Missing ATS keyword 2",
        ...
    ],
    "recommended_projects": [
        "Specific project type to build",
        "Another relevant project suggestion",
        ...
    ],
    "recommended_certifications": [
        "Relevant certification 1",
        "Relevant certification 2",
        ...
    ],
    "recommendation": "<Strong Fit | Moderate Fit | Weak Fit>",
    "reasoning": "<detailed explanation for the verdict with specific examples>",
    "interview_readiness": "<assessment of candidate's readiness for technical interviews>",
    "salary_expectation_alignment": "<whether experience level matches typical role expectations>"
}}

IMPORTANT: 
- Be honest and realistic with the match percentage
- Provide specific, actionable feedback
- Reference actual content from the resume
- Consider both technical skills and soft skills
- Evaluate project complexity and impact

Return ONLY valid JSON, no additional text."""
        )
        
        # Use LCEL (LangChain Expression Language) instead of deprecated LLMChain
        chain = analysis_prompt | self.llm
        
        try:
            result = chain.invoke({
                "resume": resume_content,
                "job_description": job_description
            })
            
            # Parse JSON response
            response_text = result.content.strip()
            
            # Clean up response if it has markdown code blocks
            if response_text.startswith("```"):
                response_text = response_text.split("```")[1]
                if response_text.startswith("json"):
                    response_text = response_text[4:]
                response_text = response_text.strip()
            
            analysis = json.loads(response_text)
            return analysis
            
        except json.JSONDecodeError as e:
            st.error(f"Error parsing analysis results: {str(e)}")
            return self._get_fallback_analysis()
        except Exception as e:
            st.error(f"Error analyzing resume: {str(e)}")
            return self._get_fallback_analysis()
    
    def _get_fallback_analysis(self) -> Dict:
        """Return a fallback analysis structure if parsing fails"""
        return {
            "match_percentage": 0,
            "matching_skills": [],
            "missing_skills": ["Analysis failed - please try again"],
            "weak_skills": [],
            "experience_relevance": "Not mentioned",
            "education_relevance": "Not mentioned",
            "strengths": [],
            "weaknesses": ["Unable to complete analysis"],
            "improvement_suggestions": ["Please try analyzing again"],
            "ats_keywords": [],
            "recommended_projects": [],
            "recommended_certifications": [],
            "recommendation": "Weak Fit",
            "reasoning": "Technical error occurred during analysis",
            "interview_readiness": "Unable to assess",
            "salary_expectation_alignment": "Unable to assess"
        }


def display_results(analysis: Dict, job_description: str):
    """
    Display analysis results in a structured format
    
    Args:
        analysis: Analysis results dictionary
        job_description: The job description used
    """
    st.markdown("---")
    st.markdown("## 📊 Screening Results")
    
    # Match percentage and recommendation
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric(
            label="Match Percentage",
            value=f"{analysis['match_percentage']}%"
        )
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        recommendation = analysis['recommendation']
        
        # Style recommendation based on fit
        if "Strong" in recommendation:
            rec_class = "strong-fit"
        elif "Moderate" in recommendation:
            rec_class = "moderate-fit"
        else:
            rec_class = "not-fit"
        
        st.markdown('<p style="color: #ffffff; font-weight: 700; font-size: 1.1rem; margin-bottom: 0.5rem;">Final Recommendation:</p>', unsafe_allow_html=True)
        st.markdown(f'<p class="{rec_class}">{recommendation}</p>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Reasoning
    st.markdown('<div class="result-section">', unsafe_allow_html=True)
    st.markdown("### 💡 Reasoning")
    st.write(analysis['reasoning'])
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Skills analysis
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="result-section">', unsafe_allow_html=True)
        st.markdown("### ✅ Matching Skills")
        if analysis['matching_skills']:
            for skill in analysis['matching_skills']:
                st.markdown(f"- {skill}")
        else:
            st.write("No matching skills identified")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="result-section">', unsafe_allow_html=True)
        st.markdown("### ❌ Missing Skills")
        if analysis['missing_skills']:
            for skill in analysis['missing_skills']:
                st.markdown(f"- {skill}")
        else:
            st.write("No critical missing skills")
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Experience and Education
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="result-section">', unsafe_allow_html=True)
        st.markdown("### 💼 Experience Relevance")
        st.write(analysis['experience_relevance'])
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="result-section">', unsafe_allow_html=True)
        st.markdown("### 🎓 Education Relevance")
        st.write(analysis['education_relevance'])
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Strengths and Weaknesses
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="result-section">', unsafe_allow_html=True)
        st.markdown("### 💪 Strengths")
        if analysis['strengths']:
            for strength in analysis['strengths']:
                st.markdown(f"- {strength}")
        else:
            st.write("No significant strengths identified")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="result-section">', unsafe_allow_html=True)
        st.markdown("### ⚠️ Areas for Improvement")
        if analysis['weaknesses']:
            for weakness in analysis['weaknesses']:
                st.markdown(f"- {weakness}")
        else:
            st.write("No significant weaknesses identified")
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Weak Skills (if present)
    if analysis.get('weak_skills'):
        st.markdown('<div class="result-section">', unsafe_allow_html=True)
        st.markdown("### ⚡ Skills Needing Improvement")
        for skill in analysis['weak_skills']:
            st.markdown(f"- {skill}")
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Improvement Suggestions
    if analysis.get('improvement_suggestions'):
        st.markdown('<div class="result-section">', unsafe_allow_html=True)
        st.markdown("### 📈 Resume Improvement Suggestions")
        for suggestion in analysis['improvement_suggestions']:
            st.markdown(f"- {suggestion}")
        st.markdown('</div>', unsafe_allow_html=True)
    
    # ATS Keywords and Recommendations
    col1, col2 = st.columns(2)
    
    with col1:
        if analysis.get('ats_keywords'):
            st.markdown('<div class="result-section">', unsafe_allow_html=True)
            st.markdown("### 🔑 Missing ATS Keywords")
            for keyword in analysis['ats_keywords']:
                st.markdown(f"- {keyword}")
            st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        if analysis.get('recommended_certifications'):
            st.markdown('<div class="result-section">', unsafe_allow_html=True)
            st.markdown("### 🎖️ Recommended Certifications")
            for cert in analysis['recommended_certifications']:
                st.markdown(f"- {cert}")
            st.markdown('</div>', unsafe_allow_html=True)
    
    # Recommended Projects
    if analysis.get('recommended_projects'):
        st.markdown('<div class="result-section">', unsafe_allow_html=True)
        st.markdown("### 🚀 Recommended Projects to Build")
        for project in analysis['recommended_projects']:
            st.markdown(f"- {project}")
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Interview Readiness and Salary Alignment
    col1, col2 = st.columns(2)
    
    with col1:
        if analysis.get('interview_readiness'):
            st.markdown('<div class="result-section">', unsafe_allow_html=True)
            st.markdown("### 🎯 Interview Readiness")
            st.write(analysis['interview_readiness'])
            st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        if analysis.get('salary_expectation_alignment'):
            st.markdown('<div class="result-section">', unsafe_allow_html=True)
            st.markdown("### 💰 Salary Expectation Alignment")
            st.write(analysis['salary_expectation_alignment'])
            st.markdown('</div>', unsafe_allow_html=True)
    
    # Job Description used
    with st.expander("📋 View Job Description Used"):
        st.text(job_description)


def main():
    """Main application function"""
    
    # Load API key from environment
    groq_api_key = os.getenv("GROQ_API_KEY")
    
    # Header
    st.markdown("""
        <div style="text-align: center; margin-bottom: 3rem; padding: 2rem 0; border-bottom: 2px solid #E5E7EB;">
            <h1 class="main-header">🤖 AI Resume Screener</h1>
            <p class="sub-header">Intelligent resume screening powered by LangChain & Groq</p>
        </div>
    """, unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        
        st.markdown("""
            <div style="padding-bottom: 0.75rem; margin-bottom: 1rem;">
                <h3 style="color: #111827; margin: 0; font-size: 1.1rem; font-weight: 600;">📖 How to Use</h3>
            </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div style="background: #F9FAFB; padding: 1rem; border-radius: 6px; border: 1px solid #E5E7EB;">
            <p style="margin: 0.5rem 0; color: #374151;"><strong>1.</strong> 📄 Upload candidate's resume (PDF)</p>
            <p style="margin: 0.5rem 0; color: #374151;"><strong>2.</strong> 💼 Enter the job role or paste job description</p>
            <p style="margin: 0.5rem 0; color: #374151;"><strong>3.</strong> 🔍 Click 'Analyze Resume'</p>
            <p style="margin: 0.5rem 0; color: #374151;"><strong>4.</strong> 📊 Review the detailed screening results</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        st.markdown("""
            <div style="padding-bottom: 0.75rem; margin-bottom: 1rem;">
                <h3 style="color: #111827; margin: 0; font-size: 1.1rem; font-weight: 600;">ℹ️ About</h3>
            </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div style="background: #F9FAFB; padding: 1rem; border-radius: 6px; border: 1px solid #E5E7EB;">
            <p style="margin: 0.5rem 0; color: #374151;"><strong>🔗 LangChain</strong> - AI orchestration</p>
            <p style="margin: 0.5rem 0; color: #374151;"><strong>⚡ Groq LLM</strong> - Fast AI analysis</p>
            <p style="margin: 0.5rem 0; color: #374151;"><strong>🎨 Streamlit</strong> - Modern UI</p>
            <p style="margin: 0.5rem 0; margin-top: 1rem; padding-top: 1rem; border-top: 1px solid #E5E7EB; color: #6B7280; font-size: 0.875rem;">
                Built for production-ready resume screening with state-of-the-art AI.
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    # Main content area
    if not groq_api_key:
        st.warning("⚠️ Please configure your Groq API key in the .env file to get started.")
        st.info("Add GROQ_API_KEY='your-api-key-here' to the .env file")
        return
    
    # Initialize screener
    try:
        screener = ResumeScreener(groq_api_key)
    except Exception as e:
        st.error(f"Error initializing screener: {str(e)}")
        return
    
    # Input section
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("""
            <div style="margin-bottom: 1rem;">
                <h3 style="color: #111827; font-weight: 600; font-size: 1.1rem; margin: 0;">
                    📄 Upload Resume
                </h3>
            </div>
        """, unsafe_allow_html=True)
        uploaded_file = st.file_uploader(
            "Upload candidate's resume (PDF)",
            type=['pdf'],
            help="Upload a PDF resume file",
            label_visibility="collapsed"
        )
    
    with col2:
        st.markdown("""
            <div style="margin-bottom: 1rem;">
                <h3 style="color: #111827; font-weight: 600; font-size: 1.1rem; margin: 0;">
                    💼 Job Details
                </h3>
            </div>
        """, unsafe_allow_html=True)
        job_role = st.text_input(
            "Job Role",
            placeholder="e.g., Data Scientist, GenAI Developer, ML Engineer",
            help="Enter the job title/role",
            label_visibility="collapsed"
        )
        
        use_custom_jd = st.checkbox("Use custom job description instead")
    
    # Optional custom job description
    job_description = ""
    if use_custom_jd:
        job_description = st.text_area(
            "Paste Job Description",
            height=200,
            placeholder="Paste the complete job description here...",
            help="Paste a custom job description instead of auto-generating one"
        )
    
    # Analyze button
    st.markdown("---")
    analyze_button = st.button("🔍 Analyze Resume", type="primary", use_container_width=True)
    
    # Analysis logic
    if analyze_button:
        # Validation
        if not uploaded_file:
            st.error("❌ Please upload a resume PDF file.")
            return
        
        if not use_custom_jd and not job_role:
            st.error("❌ Please enter a job role.")
            return
        
        if use_custom_jd and not job_description:
            st.error("❌ Please paste a job description.")
            return
        
        
        # Save uploaded file temporarily
        os.makedirs("temp", exist_ok=True)
        temp_file_path = os.path.join("temp", uploaded_file.name)
        with open(temp_file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        
        # Process resume
        with st.spinner("📖 Extracting resume content..."):
            resume_text = screener.extract_text_from_pdf(temp_file_path)
        
        # Validate resume text
        if not resume_text or len(resume_text.strip()) < 50:
            st.error("❌ Unable to extract meaningful content from the resume. Please check the PDF file.")
            return
        
        st.success(f"✅ Resume extracted successfully ({len(resume_text)} characters)")
        
        # Generate or use job description
        if not use_custom_jd:
            with st.spinner(f"📝 Generating job description for '{job_role}'..."):
                job_description = screener.generate_job_description(job_role)
            st.success("✅ Job description generated")
        
        # Analyze resume
        with st.spinner("🤖 Analyzing resume against job requirements..."):
            analysis = screener.analyze_resume(resume_text, job_description)
        
        # Display results
        display_results(analysis, job_description)
        
        # Clean up temp file
        try:
            os.remove(temp_file_path)
        except:
            pass
    
    # Footer
    st.markdown("---")
    st.markdown("""
        <div style="text-align: center; padding: 2rem 0;">
            <p style="color: #6B7280; font-size: 0.95rem; margin: 0;">
                Built with ❤️ using LangChain, Groq & Streamlit
            </p>
            <p style="color: #9CA3AF; font-size: 0.875rem; margin-top: 0.5rem;">
                Powered by AI • Production Ready • State-of-the-Art
            </p>
        </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
>>>>>>> cb1078669a78c034caae61b925307ef40c626ce0
