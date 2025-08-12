from fastapi import APIRouter, HTTPException
from app.feature_1.models import FeatureRequest, FeatureResponse
from app.feature_1.feature_logic import do_logic

router = APIRouter()


@router.post("/feature_1", response_model=FeatureResponse, status_code=200)
async def scrape(request: FeatureRequest):
    """
    Feature 1 endpoint.

    Args:
        request (FeatureRequest): The request data containing parameters.

    Returns:
        FeatureResponse: The result including status and data.

    Raises:
        HTTPException: If it fails or invalid parameters are provided.
    """
    try:
        data = await do_logic(request)
        return FeatureResponse(status="success", data=data)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
