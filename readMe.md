# 🎯 AI-Powered Job Screening System

A comprehensive solution that enhances the recruitment process by intelligently matching resumes to job descriptions using NLP and Machine Learning. It includes two modules:
- **Dataset-Based Screening**: Evaluate and visualize matching for a predefined dataset.
- **Real-Time Screening**: Upload resumes and job descriptions for on-the-fly screening and email automation.

---

## 📌 Problem Statement

Recruiters often face the challenge of sifting through hundreds of resumes manually, leading to inefficiencies, biases, and delays in hiring. Our solution streamlines this process using AI-powered matching and automation, ensuring accurate and fast shortlisting of candidates.

---

## ✅ Key Features

- 🔍 **Resume Parsing** using `PyMuPDF (fitz)` and `spaCy`
- 🧠 **Job Description Summarization** using `google/flan-t5-large`
- 🤝 **Matching** using `SentenceTransformer ('all-MiniLM-L6-v2')` + Cosine Similarity
- 📊 **Dashboard Visualizations** using `Streamlit` and `Plotly`
- 🗃️ **Shortlisted Candidate Storage** using `SQLite3`
- 📧 **Email Automation** using `yagmail`
- 🧾 **Dataset-Based Screening** in `.ipynb` for training and evaluation
- 🌐 **Real-Time Screening** via an interactive Streamlit app


---

## ⚙️ Technologies Used

| Component        | Technology |
|------------------|------------|
| Resume Parsing   | `PyMuPDF`, `spaCy` |
| JD Summarization | `google/flan-t5-large` (HuggingFace Transformers) |
| Matching         | `all-MiniLM-L6-v2` (SentenceTransformers), Cosine Similarity |
| Backend API      | `FastAPI` |
| Frontend         | `Streamlit`, `Plotly` |
| Database         | `SQLite3` |
| Emailing         | `yagmail` |

---

## 🚀 Getting Started

1. **Clone the repository**:
   ```bash
   git clone https://github.com/your-repo/job-screening-ai.git
   cd job-screening-ai

2. **Install dependencies**:

    ```bash
    pip install -r requirements.txt

3. **Run the backend server**:

    ```bash
    cd backend
    uvicorn main:app --reload

4. **Run the Streamlit frontend**:

    ```bash
    cd ../frontend
    streamlit run app.py

---

## 📊 Dataset-Based Matching (Notebook)
Check the notebooks/dataset_screening.ipynb file for training and evaluation results on a given dataset.

The notebook processes candidate-job matching scores, evaluates model performance, and defines a threshold (75%) for shortlisting.

🧪 Real-Time Resume Screening (Streamlit App)
Upload multiple resumes and a job description.

Set a similarity threshold.

View shortlisted candidates.

Send emails directly to top-matched candidates.


## Contributors
Varshitha Masaram – CSE Student at IIITDM Kancheepuram

Dhanush Perikala - CSE Student at IIITDM Kancheepuram

## Acknowledgements
HuggingFace Transformers

SentenceTransformers by UKPLab

Streamlit community

Accenture Hackathon Challenge – Problem Statement 5
