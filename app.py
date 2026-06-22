import pandas as pd
import streamlit as st
from resume_parser import extract_text

# Skills List
skills_list = [
    "python",
    "sql",
    "machine learning",
    "deep learning",
    "tensorflow",
    "pytorch",
    "nlp",
    "fastapi",
    "flask",
    "django",
    "react",
    "javascript",
    "html",
    "css",
    "git",
    "github",
    "mongodb",
    "mysql"
]

# Load Jobs Dataset
jobs = pd.read_csv("data/jobs.csv")


# Skill Detection Function
def extract_skills(text):

    found_skills = []

    text = text.lower()

    for skill in skills_list:
        if skill in text:
            found_skills.append(skill)

    return found_skills


# Job Recommendation Function
def recommend_job(user_skills):

    best_job = None
    best_score = 0
    missing_skills = []

    for _, row in jobs.iterrows():

        job_skills = row["Skills"].split()

        matched = 0

        for skill in job_skills:
            if skill in user_skills:
                matched += 1

        score = (matched / len(job_skills)) * 100

        if score > best_score:

            best_score = score
            best_job = row["Job Title"]

            missing_skills = [
                skill
                for skill in job_skills
                if skill not in user_skills
            ]

    return best_job, best_score, missing_skills


# Streamlit UI
st.title("🤖 AI Resume Analyzer")

uploaded_file = st.file_uploader(
    "Upload Resume",
    type=["pdf"]
)

if uploaded_file:

    st.success("Resume Uploaded Successfully!")

    # Extract Resume Text
    resume_text = extract_text(uploaded_file)

    # Detect Skills
    skills = extract_skills(resume_text)

    st.subheader("🛠 Detected Skills")

    if skills:
        for skill in skills:
            st.success(skill)
    else:
        st.warning("No skills detected.")

    # Recommend Job
    job, score, missing = recommend_job(skills)

    st.subheader("🎯 Recommended Role")
    st.success(job)

    st.subheader("📊 Match Score")
    st.info(f"{score:.2f}%")

    # Resume Score
    resume_score = min(100, len(skills) * 10)

    st.subheader("⭐ Resume Score")
    st.progress(resume_score)

    st.write(f"Resume Score: {resume_score}/100")

    # Missing Skills
    st.subheader("⚠️ Missing Skills")

    if missing:
        for skill in missing:
            st.warning(skill)
    else:
        st.success("No missing skills found!")

    # AI/ML Suggestions
    st.subheader("🚀 AI/ML Career Suggestions")

    ai_skills = [
        "python",
        "machine learning",
        "tensorflow",
        "pytorch",
        "sql"
    ]

    for skill in ai_skills:
        if skill not in skills:
            st.warning(f"Learn: {skill}")

    # Resume Content
    st.subheader("📄 Resume Content")

    st.text_area(
        "Extracted Text",
        resume_text,
        height=300
    )