from fastapi import FastAPI
from app.routes import health, materials, matching, reviews, common_materials

app = FastAPI(title="AI-Powered Material Master Harmonization API")

app.include_router(health.router, prefix="/api")
app.include_router(materials.router, prefix="/api")
app.include_router(matching.router, prefix="/api")
app.include_router(reviews.router, prefix="/api")
app.include_router(common_materials.router, prefix="/api")
