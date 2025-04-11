# modules/matcher.py
import re
from sentence_transformers import SentenceTransformer, util
import sqlite3
import pandas as pd
from datetime import datetime

model = SentenceTransformer('all-MiniLM-L6-v2')

def extract_experience_years(experience_list):
    total_years = 0
    for entry in experience_list:
        matches = re.findall(r'(\d{4})\s*[-–]\s*(Present|\d{4})', entry)
        for start, end in matches:
            start_year = int(start)
            end_year = datetime.now().year if end.lower() == 'present' else int(end)
            if end_year >= start_year:
                total_years += end_year - start_year
    return total_years

def prepare_jd_text(jd_summary_text: str) -> str:
    # Extract skills from predefined keywords
    def extract_skills(text):
        if isinstance(text, list):
            text = ' '.join(text)
        text = str(text).lower()
    
        skill_keywords = ['Python', 'Java', 'C++', 'JavaScript', 'React', 'Angular', 'SQL', 'AWS', 'Django', 'Flask', 'Docker', 'Kubernetes']
        found = [skill for skill in skill_keywords if skill.lower() in text]
        return ', '.join(found) if found else "Not specified"

    # Extract qualifications
    def extract_qualifications(text):
        pattern = r"(Bachelor(?:'s)?|Master(?:'s)?|B\.Tech|M\.Tech|BSc|MSc|PhD)[^.,;\n]*"
        matches = re.findall(pattern, text, re.IGNORECASE)
        return ', '.join(set(matches)) if matches else "Not specified"

    # Extract experience
    def extract_experience_requirements(text):
        match = re.search(r'(\d+)\+?\s*(?:years|yrs)', text)
        return f"{match.group(1)} years" if match else "Not specified"

    # Parse JD summary text
    skills = extract_skills(jd_summary_text)
    qualifications = extract_qualifications(jd_summary_text)
    experience = extract_experience_requirements(jd_summary_text)

    return (
        f"Required Skills: {skills}\n"
        f"Qualifications: {qualifications}\n"
        f"Experience Requirements: {experience}"
    )

def prepare_cv_text(cv: dict) -> str:
    skills = ' '.join(cv.get('Skills', [])) if isinstance(cv.get('Skills'), list) else cv.get('Skills', '')
    education = ' '.join(cv.get('Education', [])) if isinstance(cv.get('Education'), list) else cv.get('Education', '')
    experience = ' '.join(cv.get('Work Experience', [])) if isinstance(cv.get('Work Experience'), list) else cv.get('Work Experience', '')
    tech = ' '.join(cv.get('Tech Stack', [])) if isinstance(cv.get('Tech Stack'), list) else cv.get('Tech Stack', '')
    achievements = ' '.join(cv.get('Achievements', [])) if isinstance(cv.get('Achievements'), list) else cv.get('Achievements', '')
    certifications = ' '.join(cv.get('Certifications', [])) if isinstance(cv.get('Certifications'), list) else cv.get('Certifications', '')

    return f"{skills} {tech} {education} {certifications} {achievements} {experience}"


def match_resumes(parsed_cvs: list, jd_summary_text: str, job_role: str = "N/A", threshold: float = 0.75):
    jd_text = prepare_jd_text(jd_summary_text)
    jd_embedding = model.encode([jd_text], convert_to_tensor=True)

    results = []

    for cv in parsed_cvs:
        cv_text = prepare_cv_text(cv)
        cv_embedding = model.encode([cv_text], convert_to_tensor=True)
        sim_score = float(util.cos_sim(jd_embedding, cv_embedding)[0][0])

        shortlisted = "Yes" if sim_score >= threshold else "No"
        total_exp = extract_experience_years(cv.get('Work Experience', [])) if isinstance(cv.get('Work Experience'), list) else 0

        result = {
            'Name': cv.get('Name', 'N/A'),
            'Contact': cv.get('Phone', 'N/A'),
            'Email': cv.get('Email', 'N/A'),
            'Job Role': job_role,
            'Score': round(sim_score, 3),
            'Shortlisted': shortlisted,
            'Experience': total_exp
        }
        results.append(result)

    df = pd.DataFrame(results)

    # Save to SQLite
    conn = sqlite3.connect("resumes.db")
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS shortlisted_candidates (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            contact TEXT,
            email TEXT,
            job_role TEXT,
            similarity_score REAL,
            shortlisted TEXT,
            UNIQUE(email, job_role)
        )
    ''')
    conn.commit()
    conn.close()

    return df

def store_shortlisted_to_sqlite(matches_df):
    conn = sqlite3.connect("resumes.db")
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS shortlisted_candidates (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            contact TEXT,
            email TEXT,
            job_role TEXT,
            similarity_score REAL,
            shortlisted TEXT,
            UNIQUE(email, job_role)
        )
    ''')

    for _, row in matches_df.iterrows():
        cursor.execute('''
            INSERT OR IGNORE INTO shortlisted_candidates (
                name, contact, email, job_role, similarity_score, shortlisted
            ) VALUES (?, ?, ?, ?, ?, ?)
        ''', (
            row['Name'], row['Contact'], row['Email'], row['Job Role'],
            float(row['Score']), row['Shortlisted']
        ))

    conn.commit()
    conn.close()

def view_top_matches(threshold=0.7):
    conn = sqlite3.connect("resumes.db")
    df = pd.read_sql_query(f'''
        SELECT * FROM shortlisted_candidates WHERE similarity_score >= {threshold}
        ORDER BY similarity_score DESC
    ''', conn)
    conn.close()
    return df