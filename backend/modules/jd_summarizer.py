# backend/modules/jd_summarizer.py

from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import torch

# Load the model and tokenizer once
model_name = "google/flan-t5-large"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSeq2SeqLM.from_pretrained(model_name)

def get_answer(jd_text: str, question: str) -> str:
    prompt = f"""Extract the answer from the job description below.

Job Description:
{jd_text}

Question: {question}"""

    inputs = tokenizer(prompt, return_tensors="pt", max_length=512, truncation=True)
    outputs = model.generate(**inputs, max_length=50)
    answer = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return answer.strip()

def get_structured_summary(jd_text: str) -> dict:
    return {
        "Required Skills": get_answer(
            jd_text,
            "Extract a bulleted list of technical and soft skills explicitly required in the job description below. Include only skills directly mentioned like programming languages, tools, frameworks, competencies."
        ),
        "Qualifications": get_answer(
            jd_text,
            "What qualifications are mentioned in this job description?"
        ),
        "Experience": get_answer(
            jd_text,
            "How much experience is required for this job?"
        ),
    }
