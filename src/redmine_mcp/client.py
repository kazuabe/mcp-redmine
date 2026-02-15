import os
from typing import Any

import httpx


class RedmineClient:
    """Async HTTP client for Redmine REST API."""

    def __init__(
        self,
        url: str | None = None,
        api_key: str | None = None,
    ):
        self.base_url = (url or os.environ["REDMINE_URL"]).rstrip("/")
        self.api_key = api_key or os.environ["REDMINE_API_KEY"]
        self._headers = {
            "X-Redmine-API-Key": self.api_key,
            "Content-Type": "application/json",
        }

    async def get(self, path: str, params: dict[str, Any] | None = None) -> dict[str, Any]:
        async with httpx.AsyncClient() as client:
            resp = await client.get(
                f"{self.base_url}{path}",
                headers=self._headers,
                params=params,
            )
            resp.raise_for_status()
            return resp.json()

    async def post(self, path: str, json: dict[str, Any] | None = None) -> dict[str, Any]:
        async with httpx.AsyncClient() as client:
            resp = await client.post(
                f"{self.base_url}{path}",
                headers=self._headers,
                json=json,
            )
            resp.raise_for_status()
            if resp.status_code == 204:
                return {}
            return resp.json()

    async def put(self, path: str, json: dict[str, Any] | None = None) -> dict[str, Any]:
        async with httpx.AsyncClient() as client:
            resp = await client.put(
                f"{self.base_url}{path}",
                headers=self._headers,
                json=json,
            )
            resp.raise_for_status()
            return {}

    async def delete(self, path: str) -> dict[str, Any]:
        async with httpx.AsyncClient() as client:
            resp = await client.delete(
                f"{self.base_url}{path}",
                headers=self._headers,
            )
            resp.raise_for_status()
            return {}
