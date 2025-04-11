# backend/modules/cv_parser.py

import fitz
import spacy
import re
from fastapi import UploadFile
nlp = spacy.load("en_core_web_trf")

async def extract_text_from_pdf(file: UploadFile):
    doc = fitz.open(stream=await file.read(), filetype="pdf")
    text = ""
    for page in doc:
        text += page.get_text()
    return text


def extract_email(text):
    match = re.findall(r'\b[\w.-]+?@\w+?\.\w+?\b', text)
    return match[0] if match else None

def extract_phone(text):
    match = re.findall(r'\+?\d[\d\s-]{8,}\d', text)
    return match[0] if match else None

def extract_education(text):
    keywords = ['Bachelor', 'Master', 'B.Tech', 'M.Tech', 'B.E', 'M.E', 'PhD', 'MBA']
    return [line.strip() for line in text.split('\n') if any(k in line for k in keywords)]

def extract_work_experience_section(text):
    match = re.search(r'Work Experience(.*?)(Education|Skills|Certifications|Achievements|Projects|$)', 
                      text, re.IGNORECASE | re.DOTALL)
    return match.group(1).strip() if match else ""

def extract_experience_years(text):
    section = extract_work_experience_section(text)
    year_ranges = re.findall(r'\(?(\d{4})\)?\s*[-–]\s*\(?(\d{4})\)?', section)
    return sum(max(0, int(end) - int(start)) for start, end in year_ranges)

def extract_certifications(text):
    return [line.strip() for line in text.split('\n') if "certificat" in line.lower()]

def extract_achievements(text):
    return [line.strip() for line in text.split('\n') 
            if re.search(r'(award|achievement|honor|rank|topper|winner)', line, re.IGNORECASE)]

def extract_entities(text):
    doc = nlp(text)
    entities = {"PERSON": [], "ORG": [], "SKILLS": []}
    for ent in doc.ents:
        if ent.label_ == "PERSON":
            entities["PERSON"].append(ent.text)
        elif ent.label_ == "ORG":
            entities["ORG"].append(ent.text)
    skills_list = ["Java", "SQL", "Python", "Spring Boot", "MySQL", "Kafka", "AWS", "Azure", "Docker"]
    entities["SKILLS"] = [s for s in skills_list if s.lower() in text.lower()]
    return entities

async def parse_cv(file):
    text = await extract_text_from_pdf(file)
    email = extract_email(text)
    phone = extract_phone(text)
    entities = extract_entities(text)
    education = extract_education(text)
    work_ex = extract_experience_years(text)
    certifications = extract_certifications(text)
    achievements = extract_achievements(text)

    parsed = {
        "Name": entities["PERSON"][0] if entities["PERSON"] else None,
        "Email": email,
        "Phone": phone,
        "Education": education,
        "Work Experience": work_ex,
        "Skills": entities["SKILLS"],
        "Certifications": certifications,
        "Achievements": achievements,
        "Tech Stack": entities["SKILLS"]
    }
    return parsed
