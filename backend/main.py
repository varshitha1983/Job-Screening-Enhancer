# main.py
from fastapi import FastAPI
from starlette.middleware.sessions import SessionMiddleware
from fastapi.middleware.cors import CORSMiddleware
from database.db import init_db

# Initialize database
init_db()

# Import routers
from routers.cv_parser_router import router as cv_parser_router
from routers.jd_summarizer_router import router as jd_router
from routers.matcher_router import router as matcher_router
from routers.email_router import router as email_router

app = FastAPI()

# Add SessionMiddleware
app.add_middleware(SessionMiddleware, secret_key="Varshitha*123")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(cv_parser_router)
app.include_router(jd_router)
app.include_router(matcher_router)
app.include_router(email_router)