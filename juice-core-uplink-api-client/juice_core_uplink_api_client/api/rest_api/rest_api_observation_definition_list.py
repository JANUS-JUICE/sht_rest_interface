from http import HTTPStatus
from typing import Any, Dict, Optional

import httpx

from ...client import Client
from ...models.observation_definition import ObservationDefinition
from ...types import Response


def _get_kwargs(
    *,
    client: Client,
) -> Dict[str, Any]:
    url = "{}/rest_api/observation_definition/".format(client.base_url)

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    return {
        "method": "get",
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
    }


def _parse_response(*, response: httpx.Response) -> Optional[ObservationDefinition]:
    if response.status_code == HTTPStatus.OK:
        response_200 = ObservationDefinition.from_dict(response.json())

        return response_200
    return None


def _build_response(*, response: httpx.Response) -> Response[ObservationDefinition]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    *,
    client: Client,
) -> Response[ObservationDefinition]:
    """Retrieve the observation definition identified by the mnemonic

     Get the list of observation definitions available in the system

    Returns:
        Response[ObservationDefinition]
    """

    kwargs = _get_kwargs(
        client=client,
    )

    response = httpx.request(
        verify=client.verify_ssl,
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    *,
    client: Client,
) -> Optional[ObservationDefinition]:
    """Retrieve the observation definition identified by the mnemonic

     Get the list of observation definitions available in the system

    Returns:
        Response[ObservationDefinition]
    """

    return sync_detailed(
        client=client,
    ).parsed


async def asyncio_detailed(
    *,
    client: Client,
) -> Response[ObservationDefinition]:
    """Retrieve the observation definition identified by the mnemonic

     Get the list of observation definitions available in the system

    Returns:
        Response[ObservationDefinition]
    """

    kwargs = _get_kwargs(
        client=client,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(response=response)


async def asyncio(
    *,
    client: Client,
) -> Optional[ObservationDefinition]:
    """Retrieve the observation definition identified by the mnemonic

     Get the list of observation definitions available in the system

    Returns:
        Response[ObservationDefinition]
    """

    return (
        await asyncio_detailed(
            client=client,
        )
    ).parsed