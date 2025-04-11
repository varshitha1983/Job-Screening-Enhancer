# routers/email_router.py

from fastapi import APIRouter
from fastapi.responses import JSONResponse
from modules.email_sender import send_emails_to_shortlisted

router = APIRouter(
    prefix="/send-emails",
    tags=["Email Sender"]
)

@router.post("/")
async def send_emails():
    try:
        result = send_emails_to_shortlisted(threshold=0.75)

        if result["status"] == "success":
            return {"message": f"Emails sent to the candidates."}
        elif result["status"] == "no_candidates":
            return {"message": "No candidates found above threshold."}
        else:
            return JSONResponse(status_code=500, content={"error": result.get("error", "Unknown error.")})

    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})
