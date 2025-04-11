# routers/matcher_router.py
from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from modules.matcher import match_resumes, store_shortlisted_to_sqlite
from pydantic import BaseModel
from typing import List, Dict, Any

router = APIRouter(
    prefix="/match-resumes",
    tags=["Matcher"]
)

class MatchRequest(BaseModel):
    summary_text: str
    parsed_resumes: List[Dict[str, Any]]
    job_role: str
    threshold: float = 0.7

@router.post("/")
async def match_resumes_endpoint(request: MatchRequest):
    try:
        
        matches_df = match_resumes(
            parsed_cvs=request.parsed_resumes,
            jd_summary_text=request.summary_text,
            job_role=request.job_role,
            threshold=request.threshold           
        )

        # store_shortlisted_to_sqlite(matches_df)
        matches_json = matches_df.to_dict(orient="records")
        
        return JSONResponse(
            status_code=200,
            content={
                "status": "success",
                "message": "Matching completed successfully",
                "matches": matches_json
            }
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )