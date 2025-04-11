# modules/email_sender.py

import sqlite3
import pandas as pd
import yagmail

def send_emails_to_shortlisted(threshold=0.75):
    # Use app password if 2FA is enabled
    sender_email = "varshithamasaram@gmail.com"
    sender_password = "fliz bvno vajb xehh"

    try:
        yag = yagmail.SMTP(user=sender_email, password=sender_password)
    except Exception as e:
        print("❌ Failed to initialize email sender:", e)
        return {"status": "failed", "error": str(e)}

    # Fetch shortlisted candidates from the DB
    try:
        conn = sqlite3.connect("resumes.db")
        query = f"""
        SELECT name, email, job_role, similarity_score 
        FROM shortlisted_candidates
        WHERE similarity_score >= {threshold}
        ORDER BY similarity_score DESC
        """
        shortlisted = pd.read_sql_query(query, conn)
        conn.close()
    except Exception as e:
        return {"status": "failed", "error": f"DB error: {e}"}

    if shortlisted.empty:
        return {"status": "no_candidates", "message": "No candidates above threshold."}

    print(f"📤 Sending emails to {len(shortlisted)} shortlisted candidates...")

    for _, row in shortlisted.iterrows():
        subject = f"Interview Invitation for {row['job_role']}"
        body = f"""
Hi {row['name']},

Congratulations! 🎉

You have been shortlisted for the role of *{row['job_role']}* based on your resume evaluation.

Your match score: {round(row['similarity_score'], 2)}%

We’d like to invite you to the next round of interviews. Please respond to this email to confirm your availability.

Best Regards,  
Hiring Team
        """

        try:
            yag.send(to=row['email'], subject=subject, contents=body)
            print(f"✅ Email sent to: {row['email']}")
        except Exception as e:
            print(f"❌ Failed to send to {row['email']}: {e}")

    print("📬 All emails sent successfully.")
    return {"status": "success", "count": len(shortlisted)}
