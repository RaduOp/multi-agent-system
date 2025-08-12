from app.feature_1.models import FeatureRequest, DataPayload, ResultItem
import datetime


async def do_logic(request: FeatureRequest) -> DataPayload:
    """
    Here goes the logic for the feature.

    Args:
        request (FeatureRequest): The request parameters.

    Returns:
        dict: Output data, mocked for now
    """
    # Mock some result list with generic items
    results = [
        ResultItem(id=i, name=f"Item {i}", value=i * 10) for i in range(request.limit)
    ]

    # Build the mocked response dict
    data_payload = DataPayload(
        timestamp=datetime.datetime.now(datetime.UTC), results=results
    )
    return data_payload
