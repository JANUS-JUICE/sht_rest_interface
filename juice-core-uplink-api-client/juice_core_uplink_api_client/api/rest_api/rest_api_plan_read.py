from http import HTTPStatus
from typing import Any, Dict, Optional, Union, cast

import httpx

from ...client import Client
from ...models.read_only_plan import ReadOnlyPlan
from ...types import Response


def _get_kwargs(
    id: str,
    *,
    client: Client,
) -> Dict[str, Any]:
    url = "{}/rest_api/plan/{id}/".format(client.base_url, id=id)

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    return {
        "method": "get",
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
    }


def _parse_response(*, response: httpx.Response) -> Optional[Union[Any, ReadOnlyPlan]]:
    if response.status_code == HTTPStatus.OK:
        response_200 = ReadOnlyPlan.from_dict(response.json())

        return response_200
    if response.status_code == HTTPStatus.UNAUTHORIZED:
        response_401 = cast(Any, None)
        return response_401
    if response.status_code == HTTPStatus.NOT_FOUND:
        response_404 = cast(Any, None)
        return response_404
    return None


def _build_response(*, response: httpx.Response) -> Response[Union[Any, ReadOnlyPlan]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    id: str,
    *,
    client: Client,
) -> Response[Union[Any, ReadOnlyPlan]]:
    """Retrieve a plan

     Retrieve, update or delete a segmentation instance.

    Args:
        id (str):

    Returns:
        Response[Union[Any, ReadOnlyPlan]]
    """

    kwargs = _get_kwargs(
        id=id,
        client=client,
    )

    response = httpx.request(
        verify=client.verify_ssl,
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    id: str,
    *,
    client: Client,
) -> Optional[Union[Any, ReadOnlyPlan]]:
    """Retrieve a plan

     Retrieve, update or delete a segmentation instance.

    Args:
        id (str):

    Returns:
        Response[Union[Any, ReadOnlyPlan]]
    """

    return sync_detailed(
        id=id,
        client=client,
    ).parsed


async def asyncio_detailed(
    id: str,
    *,
    client: Client,
) -> Response[Union[Any, ReadOnlyPlan]]:
    """Retrieve a plan

     Retrieve, update or delete a segmentation instance.

    Args:
        id (str):

    Returns:
        Response[Union[Any, ReadOnlyPlan]]
    """

    kwargs = _get_kwargs(
        id=id,
        client=client,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(response=response)


async def asyncio(
    id: str,
    *,
    client: Client,
) -> Optional[Union[Any, ReadOnlyPlan]]:
    """Retrieve a plan

     Retrieve, update or delete a segmentation instance.

    Args:
        id (str):

    Returns:
        Response[Union[Any, ReadOnlyPlan]]
    """

    return (
        await asyncio_detailed(
            id=id,
            client=client,
        )
    ).parsed
