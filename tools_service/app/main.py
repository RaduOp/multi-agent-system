from fastapi import FastAPI
from app.feature_1.endpoints import router as feature_1_router
from app.feature_2.endpoints import router as feature_2_router

# This is how settings are used
from app.core.config import settings

app = FastAPI(title="Tools Service")

app.include_router(feature_1_router, prefix="/feature_1_pref", tags=["random_tag"])
app.include_router(
    feature_2_router, prefix="/feature_2_pref", tags=["even_more_random_tag"]
)
