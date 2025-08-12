from fastapi import APIRouter, HTTPException
from app.feature_2.models import FeatureRequest, FeatureResponse
from app.feature_2.feature_logic import do_logic

router = APIRouter()


@router.post("/feature_2", response_model=FeatureResponse, status_code=200)
async def feature_2_endpoint(request: FeatureRequest):
    """
    Feature 2 endpoint.

    Args:
        request (ScrapeRequest): The request data containing parameters.

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
