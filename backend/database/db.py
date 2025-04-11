# backend/db.py
import sqlite3
import os
import pandas as pd
DB_NAME = "resumes.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    # Table for storing parsed resumes
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS parsed_resumes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            email TEXT,
            phone TEXT,
            education TEXT,
            experience TEXT,
            skills TEXT,
            certifications TEXT,
            achievements TEXT,
            tech_stack TEXT,
            filename TEXT
        )
    ''')

    # Create a new table for match scores
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

def insert_parsed_resume(data):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute('''
        INSERT INTO parsed_resumes (name, email, phone, education, experience, skills, certifications, achievements, tech_stack, filename)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        data.get('name'), data.get('email'), data.get('phone'), data.get('education'),
        data.get('experience'), data.get('skills'), data.get('certifications'),
        data.get('achievements'), data.get('tech_stack'), data.get('filename')
    ))

    conn.commit()
    conn.close()

def store_shortlisted_to_sqlite(matches_df):
    conn = sqlite3.connect("resumes.db")
    cursor = conn.cursor()

    for _, row in matches_df.iterrows():
        cursor.execute('''
            INSERT OR IGNORE INTO shortlisted_candidates (
            name, contact, email, job_role, similarity_score, shortlisted
            ) VALUES (?, ?, ?, ?, ?, ?)
        ''', (
            row['Name'],
            row['Contact'],
            row['Email'],
            row['Job Role'],
            float(row['Score']),
            row['Shortlisted']
        ))

    conn.commit()
    conn.close()
    # print("✅ All shortlisted candiadtes stored in 'resume_jd_matches' table.")



def get_shortlisted_candidates(job_role=None):
    conn = sqlite3.connect("resumes.db")
    query = "SELECT * FROM shortlisted_candidates"
    if job_role:
        query += " WHERE job_role = ?"
        df = pd.read_sql_query(query, conn, params=(job_role,))
    else:
        df = pd.read_sql_query(query, conn)
    conn.close()
    return df
