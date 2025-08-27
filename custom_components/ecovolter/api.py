"""Sample API Client."""

from __future__ import annotations

import asyncio
import hashlib
import hmac
import json
import socket
from time import time
from typing import Any

import aiohttp


class EcovolterApiClientError(Exception):
    """Exception to indicate a general API error."""

class EcovolterApiClientCommunicationError(
    EcovolterApiClientError,
):
    """Exception to indicate a communication error."""


class EcovolterApiClientAuthenticationError(
    EcovolterApiClientError,
):
    """Exception to indicate an authentication error."""


def _verify_response_or_raise(response: aiohttp.ClientResponse) -> None:
    """Verify that the response is valid."""
    if response.status in (401, 403):
        msg = "Chyba ověřování, nesprávný tajný klíč."
        raise EcovolterApiClientAuthenticationError(
            msg,
        )
    response.raise_for_status()


class EcovolterApiClient:
    """Sample API Client."""

    def __init__(
        self,
        serial_number: str,
        secret_key: str,
        session: aiohttp.ClientSession,
    ) -> None:
        """Sample API Client."""
        self._serial_number = serial_number
        self._secret_key = secret_key.encode("utf-8")  # bytes type
        self._session = session

    async def async_get_status(self) -> Any:
        """Get settings data from Ecovolter."""
        return await self._api_wrapper(
            method="get",
            path="/status",
        )

    async def async_get_settings(self) -> Any:
        """Get settings data from Ecovolter."""
        return await self._api_wrapper(
            method="get",
            path="/settings",
        )

    async def async_set_settings(self, data: dict) -> Any:
        """Get settings data from Ecovolter."""
        timestamp_miliseconds = int(time() * 1000)
        data["timestamp"] = timestamp_miliseconds
        return await self._api_wrapper(method="patch", path="/settings", data=data)

    async def _api_wrapper(
        self,
        method: str,
        path: str,
        data: dict | None = None,
        headers: dict | None = None,
    ) -> Any:
        """Get information from the API."""
        timestamp_seconds = str(int(time()))
        url = f"http://{self._serial_number}.local/api/v1/charger{path}"
        json_data = json.dumps(data, separators=(",", ":"))
        data_to_sign = (
            f"{url}\n{timestamp_seconds}\n{'' if data is None else json_data}"
        )
        hmac_signature = hmac.new(
            self._secret_key, data_to_sign.encode("utf-8"), hashlib.sha256
        ).hexdigest()
        headers = {
            "X-Timestamp": timestamp_seconds,
            "Authorization": f"HmacSHA256 {hmac_signature}",
        }

        try:
            response = await asyncio.wait_for(
                self._session.request(
                    method=method,
                    url=url,
                    headers=headers,
                    json=data,
                ),
                timeout=10.0
            )
            _verify_response_or_raise(response)
            return await response.json()

        except TimeoutError as exception:
            msg = f"Vypršel čas čekání na odpověď - {exception}"
            raise EcovolterApiClientCommunicationError(
                msg,
            ) from exception
        except (aiohttp.ClientError, socket.gaierror) as exception:
            msg = f"Chyba při stahování informací - {exception}"
            raise EcovolterApiClientCommunicationError(
                msg,
            ) from exception
        except EcovolterApiClientAuthenticationError as exception:
            msg = f"Chyba ověřování, nesprávný tajný klíč. - {exception}"
            raise EcovolterApiClientAuthenticationError(
                msg,
            ) from exception
        except Exception as exception:  # pylint: disable=broad-except
            msg = f"Neznámá chyba! - {exception}"
            raise EcovolterApiClientError(
                msg,
            ) from exception
