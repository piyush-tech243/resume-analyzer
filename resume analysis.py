#load  csv data from pandas
 
import pandas as pd

df = pd.read_csv("Resume.csv")

print(df[:8])

#check how much collumn

 
print(df.columns)

# cleaning data 
         
import re

def clean_text(text):
    text = text.lower()               # lowercase
    text = re.sub(r'\s+', ' ', text)   #remove extra space
    text = re.sub(r'[^a-z+ ]', '', text)   # + allow kiya
    return text

# phela  1 resume ko  uthayaa fir usko clean kiya 

# resume = df["Resume_str"][0]

# clean_resume = clean_text(resume)

# print(clean_resume[:500])   # thoda sa print karo

# sabhi resume ko clean kr rhe h ab 

df["clean_resume"] = df["Resume_str"].apply(clean_text)
print(df["clean_resume"][:8])

# skills ko extract krna resume m se

skills_list = [
    # Programming
    "python", "java",  "c++", "javascript",

    # Data / Analyst
    "sql", "excel", "power bi", "tableau",
    "data analysis", "data visualization",
    "machine learning",

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
    "communication", "teamwork", "leadership",
    "problem solving",

    # Tools
    "ms office", "word", "powerpoint"

]

# skills extractions

def extract_skills(text):
    text = text.lower()
    found_skills = []

    for skill in skills_list:
        if skill in text:
            found_skills.append(skill)

    return found_skills
df["skills"] = df["clean_resume"].apply(extract_skills)
print("Skills:", df["skills"][:8])

# matching resume

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

scores = []

for i in range(len(df)):
    resume_skills = df["skills"][i]
    
    matched = set(resume_skills) & set(job_skills)
    score = len(matched) / len(job_skills) * 100
    
    scores.append(score)

df["score"] = scores
best_roles = []
best_scores = []

for i in range(len(df)):
    resume_skills = df["skills"][i]

    best_role = ""
    best_score = 0

    for role, skills in job_skills.items():
        matched = set(resume_skills) & set(skills)
        score = len(matched) / len(skills) * 100

        if score > best_score:
            best_score = score
            best_role = role

    best_roles.append(best_role)
    best_scores.append(best_score)

df["best_role"] = best_roles
df["best_score"] = best_scores

# score calculate

print(df[["skills", "best_role", "best_score"]].head(8))

# top3 roles

top_roles_list = []

for i in range(len(df)):
    resume_skills = df["skills"][i]

    role_scores = []

    for role, skills in job_skills.items():
        matched = set(resume_skills) & set(skills)
        score = len(matched) / len(skills) * 100

        role_scores.append((role, score))

    # sort by score (high to low)
    role_scores = sorted(role_scores, key=lambda x: x[1], reverse=True)

    # top 3 roles
    top_3 = role_scores[:3]

    top_roles_list.append(top_3)
df["top_3_roles"] = top_roles_list
print(df[["skills", "top_3_roles"]].head(5))

# missing skills

missing_skills_list = []

for i in range(len(df)):
    resume_skills = df["skills"][i]
    role = df["best_role"][i]

    if role in job_skills:   # 🔥 IMPORTANT FIX
        role_skills = job_skills[role]
        missing = list(set(role_skills) - set(resume_skills))
    else:
        missing = []   # agar role empty ya invalid ho

    missing_skills_list.append(missing)

df["missing_skills"] = missing_skills_list
df["best_role"] = df["best_role"].fillna("Unknown")
print(df[["best_role", "missing_skills"]].head(5))

# clean
user_resume = input("Enter your resume text: ")
clean_user_resume = clean_text(user_resume)

# skills extract
user_skills = extract_skills(clean_user_resume)
print("Skills:", user_skills)

# best role find
best_role = ""
best_score = 0

for role, skills in job_skills.items():
    matched = set(user_skills) & set(skills)
    score = len(matched) / len(skills) * 100

    if score > best_score:
        best_score = score
        best_role = role

print("Best Role:", best_role)
print("Score:", best_score)

# missing skills (correct role ke liye)
if best_role in job_skills:
    missing = list(set(job_skills[best_role]) - set(user_skills))
    print("Missing Skills:", missing)
    print("Recommendation: You should learn", missing)
        # smart message
    if best_score >= 80:
        print("✔ You are a strong candidate for", best_role, "role")
    elif best_score >= 50:
        print("✔ You are a good candidate for", best_role, "role")
    else:
        print("✔ You need improvement for", best_role, "role")

    if len(missing) > 0:
        print("✔ Improve these skills to increase your chances:", missing)
    else:
        print("✔ You have all required skills 🎉")

else:
    print("No role matched")
