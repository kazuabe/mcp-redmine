from unittest.mock import AsyncMock, MagicMock, patch

import httpx
import pytest

from redmine_mcp.client import RedmineClient


@pytest.fixture
def client():
    return RedmineClient(url="https://redmine.example.com", api_key="test-key")


def _mock_response(status_code=200, json_data=None):
    resp = AsyncMock(spec=httpx.Response)
    resp.status_code = status_code
    resp.json.return_value = json_data or {}
    resp.raise_for_status = MagicMock()
    return resp


@pytest.mark.asyncio
async def test_get(client):
    mock_resp = _mock_response(json_data={"issues": []})
    with patch("httpx.AsyncClient") as MockClient:
        instance = AsyncMock()
        instance.get.return_value = mock_resp
        MockClient.return_value.__aenter__ = AsyncMock(return_value=instance)
        MockClient.return_value.__aexit__ = AsyncMock(return_value=False)

        result = await client.get("/issues.json", params={"limit": 10})

        instance.get.assert_called_once_with(
            "https://redmine.example.com/issues.json",
            headers=client._headers,
            params={"limit": 10},
        )
        assert result == {"issues": []}


@pytest.mark.asyncio
async def test_post(client):
    mock_resp = _mock_response(status_code=201, json_data={"issue": {"id": 1}})
    with patch("httpx.AsyncClient") as MockClient:
        instance = AsyncMock()
        instance.post.return_value = mock_resp
        MockClient.return_value.__aenter__ = AsyncMock(return_value=instance)
        MockClient.return_value.__aexit__ = AsyncMock(return_value=False)

        result = await client.post("/issues.json", json={"issue": {"subject": "Test"}})

        instance.post.assert_called_once()
        assert result == {"issue": {"id": 1}}


@pytest.mark.asyncio
async def test_put(client):
    mock_resp = _mock_response(status_code=204)
    with patch("httpx.AsyncClient") as MockClient:
        instance = AsyncMock()
        instance.put.return_value = mock_resp
        MockClient.return_value.__aenter__ = AsyncMock(return_value=instance)
        MockClient.return_value.__aexit__ = AsyncMock(return_value=False)

        result = await client.put("/issues/1.json", json={"issue": {"status_id": 2}})

        instance.put.assert_called_once()
        assert result == {}


@pytest.mark.asyncio
async def test_delete(client):
    mock_resp = _mock_response(status_code=200)
    with patch("httpx.AsyncClient") as MockClient:
        instance = AsyncMock()
        instance.delete.return_value = mock_resp
        MockClient.return_value.__aenter__ = AsyncMock(return_value=instance)
        MockClient.return_value.__aexit__ = AsyncMock(return_value=False)

        result = await client.delete("/issues/1.json")

        instance.delete.assert_called_once()
        assert result == {}


def test_headers(client):
    assert client._headers["X-Redmine-API-Key"] == "test-key"
    assert client._headers["Content-Type"] == "application/json"


def test_base_url_trailing_slash():
    c = RedmineClient(url="https://redmine.example.com/", api_key="key")
    assert c.base_url == "https://redmine.example.com"
