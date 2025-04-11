# routers/jd_summarizer_router.py

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Dict

from modules.jd_summarizer import get_structured_summary

router = APIRouter(
    prefix="/summarize-jd",
    tags=["JD Summarizer"]
)

session_state = {
    "summarized_jd": None
}

class JDText(BaseModel):
    jd_text: str

@router.post("/")
async def summarize_jd(jd_input: JDText) -> Dict:
    try:
        summary = get_structured_summary(jd_input.jd_text)
        session_state["summarized_jd"] = summary
        return {"summary": summary}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
