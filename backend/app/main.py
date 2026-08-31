import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.db.database import engine, Base
from app.routes import health, materials, matching, reviews, common_materials

# Create DB tables automatically
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="AI-Powered Material Master Harmonization API",
    version="1.0.0",
    description="Backend API for material upload, AI matching, review workflows, and canonical common material catalog."
)

# Enable CORS for React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health.router, prefix="/api")
app.include_router(materials.router, prefix="/api")
app.include_router(matching.router, prefix="/api")
app.include_router(reviews.router, prefix="/api")
app.include_router(common_materials.router, prefix="/api")
