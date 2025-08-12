import pytest
import datetime
from app.feature_1.models import FeatureRequest, DataPayload, ResultItem, NestedOptions
from app.feature_1.feature_logic import do_logic


@pytest.mark.asyncio
async def test_do_logic_returns_correct_type():
    """Ensure do_logic returns a DataPayload instance."""
    request = FeatureRequest(
        resource_id="abc123",
        limit=3,
        offset=0,
        include_metadata=True,
        timeout_seconds=5,
        user_token="fake_token_12345",
        nested_options=NestedOptions(options={"foo": "bar"}),
    )

    result = await do_logic(request)

    assert isinstance(result, DataPayload)
    assert isinstance(result.timestamp, datetime.datetime)
    assert isinstance(result.results, list)
    assert all(isinstance(item, ResultItem) for item in result.results)


@pytest.mark.asyncio
async def test_do_logic_respects_limit():
    """Ensure the number of results matches the request limit."""
    request = FeatureRequest(
        resource_id="xyz789",
        limit=5,
        offset=0,
        include_metadata=False,
        timeout_seconds=10,
        user_token="token_67890",
        nested_options=NestedOptions(),
    )

    result = await do_logic(request)
    assert len(result.results) == 5


@pytest.mark.asyncio
async def test_do_logic_result_item_content():
    """Ensure each ResultItem has correct mocked values."""
    limit = 2
    request = FeatureRequest(
        resource_id="test123",
        limit=limit,
        offset=0,
        include_metadata=False,
        timeout_seconds=3,
        user_token="token_test",
        nested_options=NestedOptions(),
    )

    result = await do_logic(request)

    for i, item in enumerate(result.results):
        assert item.id == i
        assert item.name == f"Item {i}"
        assert item.value == i * 10
