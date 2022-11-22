from http import HTTPStatus
from typing import Any, Dict, Optional, Union, cast

import httpx

from ...client import Client
from ...models.user import User
from ...types import Response


def _get_kwargs(
    username: str,
    *,
    client: Client,
) -> Dict[str, Any]:
    url = "{}/rest_api/user/{username}/".format(client.base_url, username=username)

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    return {
        "method": "get",
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
    }


def _parse_response(*, response: httpx.Response) -> Optional[Union[Any, User]]:
    if response.status_code == HTTPStatus.OK:
        response_200 = User.from_dict(response.json())

        return response_200
    if response.status_code == HTTPStatus.UNAUTHORIZED:
        response_401 = cast(Any, None)
        return response_401
    if response.status_code == HTTPStatus.NOT_FOUND:
        response_404 = cast(Any, None)
        return response_404
    return None


def _build_response(*, response: httpx.Response) -> Response[Union[Any, User]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    username: str,
    *,
    client: Client,
) -> Response[Union[Any, User]]:
    """Retrieve the user details by username

     API endpoint that allows users to be viewed or edited.

    Args:
        username (str):

    Returns:
        Response[Union[Any, User]]
    """

    kwargs = _get_kwargs(
        username=username,
        client=client,
    )

    response = httpx.request(
        verify=client.verify_ssl,
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    username: str,
    *,
    client: Client,
) -> Optional[Union[Any, User]]:
    """Retrieve the user details by username

     API endpoint that allows users to be viewed or edited.

    Args:
        username (str):

    Returns:
        Response[Union[Any, User]]
    """

    return sync_detailed(
        username=username,
        client=client,
    ).parsed


async def asyncio_detailed(
    username: str,
    *,
    client: Client,
) -> Response[Union[Any, User]]:
    """Retrieve the user details by username

     API endpoint that allows users to be viewed or edited.

    Args:
        username (str):

    Returns:
        Response[Union[Any, User]]
    """

    kwargs = _get_kwargs(
        username=username,
        client=client,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(response=response)


async def asyncio(
    username: str,
    *,
    client: Client,
) -> Optional[Union[Any, User]]:
    """Retrieve the user details by username

     API endpoint that allows users to be viewed or edited.

    Args:
        username (str):

    Returns:
        Response[Union[Any, User]]
    """

    return (
        await asyncio_detailed(
            username=username,
            client=client,
        )
    ).parsed
