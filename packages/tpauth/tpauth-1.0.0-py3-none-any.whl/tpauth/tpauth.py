from datetime import timedelta
from urllib.parse import urljoin
import httpx

from tpauth.endpoint import Endpoint
from tpauth.response.success import FromTokenUnauthoried, Success
from tpauth.response.unauthorised import Unauthorised
from tpauth.response.unknown import Unknown


class TPAuth:
    HEADERS = {
        "accept": "*/*",
    }

    def __init__(self, host: str):
        self._host = host

    async def login(
        self, username: str, password: str, timeout: timedelta = timedelta(seconds=10)
    ):
        headers = {
            **self.HEADERS,
            "authorization": "Bearer nothing here",
            "content-type": "application/json",
        }
        endpoint = urljoin(self._host, Endpoint.LOGIN)
        payload = {"name": username, "password": password}

        try:
            async with httpx.AsyncClient(
                headers=headers, timeout=timeout.total_seconds()
            ) as client:
                response = await client.post(endpoint, json=payload)
        except httpx.RequestError as exc:
            return Unknown(cause=f"Request error: {exc}")

        if response.status_code == 200:
            try:
                data = response.json()
                return Success(**data)
            except Exception as e:
                return Unknown(cause=f"JSON parsing error from response: {e}")
        elif response.status_code == 400:
            try:
                data = response.json()
                return Unauthorised(**data)
            except Exception as e:
                return Unauthorised(error="Unauthorized access")
        else:
            try:
                data = response.json()
                error_detail = data.get("detail", "Unknown error")
            except Exception:
                error_detail = response.text or "Unknown error"
            return Unknown(
                cause=f"Status code: {response.status_code} - {error_detail}"
            )

    async def from_token(self, token: str, timeout: timedelta = timedelta(seconds=10)):
        headers = {"accept": "*/*", "authorization": f"Bearer {token}"}
        endpoint = urljoin(self._host, Endpoint.FROM_TOKEN)
        try:
            async with httpx.AsyncClient(timeout=timeout.total_seconds()) as client:
                response = await client.get(endpoint, headers=headers)
        except httpx.RequestError as exc:
            return Unknown(cause=f"Request error: {exc}")
        try:
            data = response.json()
            if response.status_code == 200:
                return Success(**data)
            return FromTokenUnauthoried(**data)
        except Exception as e:
            return Unknown(cause=f"JSON parsing error from response: {e}")
