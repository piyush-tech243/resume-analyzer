import streamlit as st
import re
import PyPDF2
from docx import Document
from rapidfuzz import fuzz
st.title("📄 Resume analyzer.py")
st.markdown("### 👨‍💻 Built by: Piyush Solanki")
st.markdown("GitHub: https://github.com/piyush-tech243")
st.markdown("🔗 LinkedIn: https://www.linkedin.com/in/piyush-solanki-9a5bb2317")
st.markdown("Made with ❤️ using Python, Streamlit, RapidFuzz, PyPDF2 & NLP")

# resume pdf

uploaded_file = st.file_uploader("📤 Upload Resume", type=["pdf", "docx", "txt"])
user_resume = st.text_area("Or paste your Text  here")


# cleaning data

def clean_text(text):
    text = text.lower()               # lowercase
    text = re.sub(r'\s+', ' ', text)   #remove extra space
    text = re.sub(r'[^a-z+ ]', '', text)   # + allow kiya
    return text

# ---------------- EXACT WORD CHECK ----------------
def is_exact_word(skill, text):
    return re.search(rf"\b{re.escape(skill)}\b", text) is not None

# ---------------- PDF ----------------
def extract_text_from_pdf(file):
    reader = PyPDF2.PdfReader(file)
    text = ""
    for page in reader.pages:
        if page.extract_text():
            text += page.extract_text()
    return text

# ---------------- DOCX ----------------
def extract_text_from_docx(file):
    doc = Document(file)
    text = ""
    for para in doc.paragraphs:
        text += para.text + " "
    return text


skills_list = [
    # Programming
    "python", "java",  "c++", "javascript",
    # AI ENGINEERING
    
    "deep learning","generative Ai","pytorch","tensorflow","keras","statistics","deep learning framework","CNN", "scikit-learn","Anaconda","Agentic AI"
    "pandas","numpy","Ai prompting","neural network","Agentic AI"

    # Data / Analyst
    "sql", "excel", "power bi", "tableau",
    "data analysis", "data visualization",
    "machine learning","matplotlib","basic statistics knowledge"

    # Web
    "html", "css", "react", "node js",

    # HR
    "hr", "recruitment", "payroll",
    "employee relations", "talent acquisition",

    # Marketing
    "marketing", "seo", "digital marketing",
    "social media", "content creation", "sales",

    # Finance
    "accounting", "financial analysis", "budgeting",

    # Soft skills
    "communication", "teamwork", "leadership","digital communication skills"
    "problem solving","Clear speaking","Problem-solving communication","Verbal Communication","Written Communication"
    "Listening Skills","Interpersonal Communication","Professional Communication","public speaking skills","persuasion" , "influence skills"
    
    # Tools
    "ms office", "word", "powerpoint"
]

def extract_skills(text):
    text = text.lower()
    words = text.split()
    found_skills = []

    for skill in skills_list:
        skill_words = skill.split()

        # ✅ 1. Exact match (best)
        if f" {skill} " in f" {text} ":
            found_skills.append(skill)
            continue

        # 🔒 2. Short skills → only exact
        if len(skill) <= 4:
            continue

        # ✅ 3. Multi-word skills
        if len(skill_words) > 1:
            for i in range(len(words) - len(skill_words) + 1):
                phrase = " ".join(words[i:i+len(skill_words)])

                if fuzz.ratio(skill, phrase) > 90:
                    found_skills.append(skill)

        # ✅ 4. Single-word fuzzy (STRICT + SAFE)
        else:
            for word in words:

                # 🔥 filters
                if len(word) < 4:
                    continue

                if abs(len(word) - len(skill)) > 1:
                    continue

                if fuzz.ratio(skill, word) > 92:
                    
                    # 🔥 EXTRA CHECK (most important)
                    if word.startswith(skill[:3]):  
                        found_skills.append(skill)

    return list(set(found_skills))
job_skills = {

    # 💻 Data / IT
    "Data Analyst": ["python", "sql", "excel", "power bi", "tableau", "data analysis"],
    "Data Scientist": ["python", "machine learning", "deep learning", "nlp", "statistics"],
    "Software Developer": ["python", "java", "c++", "javascript", "algorithms"],
    "Web Developer": ["html", "css", "javascript", "react", "node js"],
    "AI Engineer": ["machine learning", "deep learning", "tensorflow", "pytorch"],
    "Cyber Security": ["network security", "penetration testing", "ethical hacking"],
    "Cloud Engineer": ["aws", "azure", "cloud", "devops"],

    # 🏢 Business / Management
    "HR": ["hr", "recruitment", "payroll", "employee relations", "talent acquisition"],
    "Marketing": ["marketing", "seo", "digital marketing", "sales", "social media"],
    "Sales": ["sales", "negotiation", "lead generation", "client handling"],
    "Business Analyst": ["excel", "sql", "business analysis", "requirements gathering"],
    "Project Manager": ["management", "planning", "leadership", "agile"],

    # 💰 Finance / Banking
    "Banking": ["banking", "finance", "loan", "credit", "risk management"],
    "Accountant": ["accounting", "tally", "gst", "taxation", "financial analysis"],
    "Financial Analyst": ["finance", "financial modeling", "excel", "budgeting"],

    # 📞 Support / Operations
    "Customer Support": ["customer service", "communication", "problem solving"],
    "Operations": ["operations", "process management", "logistics"],

    # 🎨 Creative
    "Graphic Designer": ["photoshop", "illustrator", "design", "creativity"],
    "Content Writer": ["writing", "content creation", "seo", "blogging"],

    # 🏥 Others
    "Teacher": ["teaching", "communication", "subject knowledge"],
    "Healthcare": ["nursing", "patient care", "medical"],
}
if st.button("Analyze Resume"):

    # 📌 Get text
    if uploaded_file:
        if uploaded_file.type == "application/pdf":
            user_resume = extract_text_from_pdf(uploaded_file)
        elif uploaded_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
            user_resume = extract_text_from_docx(uploaded_file)
        else:
            user_resume = str(uploaded_file.read(), "utf-8")

    # 🧠 Clean + Extract
    clean_resume = clean_text(user_resume)
    user_skills = extract_skills(clean_resume)

    st.subheader("🧠 Skills")
    for skill in user_skills:
        st.write("✔", skill)

    # 🎯 Best Role
    best_role = ""
    best_score = 0
    role_scores = []

    for role, skills in job_skills.items():
        matched = set(user_skills) & set(skills)
        score = len(matched) / len(skills) * 100

        role_scores.append((role, score))

        if score > best_score:
            best_score = score
            best_role = role

    st.subheader("🎯 Best Role")
    st.write(best_role)

    # 🏆 Top 3
    role_scores.sort(key=lambda x: x[1], reverse=True)

    st.subheader("🏆 Top 3 Role Suggestions")
    for role, score in role_scores[:3]:
        st.write(f"✔ {role} - {round(score, 2)}%")

    # 📊 Score
    st.subheader("📊 Match Score")
    st.write(str(round(best_score, 2)) + "%")

    # ❗ Missing Skills
    if best_role in job_skills:

        missing = list(set(job_skills[best_role]) - set(user_skills))

        st.subheader("📌 Missing Skills")

        if len(missing) == 0:
            st.success("🎉 No missing skills!")
        else:
            for skill in missing:
                st.write("•", skill)

        # 📌 Recommendation
        st.subheader("📌 Recommendation")

        if len(missing) == 0:
            st.success("🎉 Perfect match! You are fully qualified.")
        elif best_score >= 80:
            st.info("✔ Good candidate but improvement needed")
        else:
            st.warning("⚠ You need improvement")
