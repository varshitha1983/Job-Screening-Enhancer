# cv_parser_router.py
from fastapi import APIRouter, UploadFile, File
from typing import List  # ✅ Fix: use from typing
from modules.cv_parser import parse_cv

router = APIRouter(
    prefix="/parse-resumes",  # ✅ This is correct
    tags=["CV Parser"]
)

@router.post("/")
async def parse_resumes(files: List[UploadFile] = File(...)):  # ✅ Use List from typing
    results = []
    for file in files:
        if file.filename.endswith(".pdf"):
            parsed = await parse_cv(file)
            parsed["Filename"] = file.filename
            results.append(parsed)
        else:
            results.append({"Filename": file.filename, "error": "Only PDF supported."})
    return {"parsed_resumes": results}
