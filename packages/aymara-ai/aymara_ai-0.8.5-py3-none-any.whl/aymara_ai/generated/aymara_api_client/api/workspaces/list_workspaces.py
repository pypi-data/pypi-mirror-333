from http import HTTPStatus
from typing import Any, Dict, List, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.workspace_out_schema import WorkspaceOutSchema
from ...types import UNSET, Response


def _get_kwargs(
    *,
    organization_uuid: str,
) -> Dict[str, Any]:
    params: Dict[str, Any] = {}

    params["organization_uuid"] = organization_uuid

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: Dict[str, Any] = {
        "method": "get",
        "url": "/v1/workspaces/",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[List["WorkspaceOutSchema"]]:
    if response.status_code == HTTPStatus.OK:
        response_200 = []
        _response_200 = response.json()
        for response_200_item_data in _response_200:
            response_200_item = WorkspaceOutSchema.from_dict(response_200_item_data)

            response_200.append(response_200_item)

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[List["WorkspaceOutSchema"]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    organization_uuid: str,
) -> Response[List["WorkspaceOutSchema"]]:
    """List Workspaces

    Args:
        organization_uuid (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[List['WorkspaceOutSchema']]
    """

    kwargs = _get_kwargs(
        organization_uuid=organization_uuid,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
    organization_uuid: str,
) -> Optional[List["WorkspaceOutSchema"]]:
    """List Workspaces

    Args:
        organization_uuid (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        List['WorkspaceOutSchema']
    """

    return sync_detailed(
        client=client,
        organization_uuid=organization_uuid,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    organization_uuid: str,
) -> Response[List["WorkspaceOutSchema"]]:
    """List Workspaces

    Args:
        organization_uuid (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[List['WorkspaceOutSchema']]
    """

    kwargs = _get_kwargs(
        organization_uuid=organization_uuid,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    organization_uuid: str,
) -> Optional[List["WorkspaceOutSchema"]]:
    """List Workspaces

    Args:
        organization_uuid (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        List['WorkspaceOutSchema']
    """

    return (
        await asyncio_detailed(
            client=client,
            organization_uuid=organization_uuid,
        )
    ).parsed
