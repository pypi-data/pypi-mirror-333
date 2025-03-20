from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.default_error import DefaultError
from ...models.get_comments import GetComments
from ...types import Unset


def _get_kwargs(
    issue_id_or_key: str,
    *,
    expand: Union[Unset, str] = UNSET,
    fields: Union[Unset, str] = UNSET,
    next_page: Union[Unset, str] = UNSET,
    order_by: Union[Unset, str] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    where: Union[Unset, str] = UNSET,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    params["expand"] = expand

    params["fields"] = fields

    params["nextPage"] = next_page

    params["orderBy"] = order_by

    params["pageSize"] = page_size

    params["where"] = where

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/issue/{issue_id_or_key}/comment".format(
            issue_id_or_key=issue_id_or_key,
        ),
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[DefaultError, list["GetComments"]]]:
    if response.status_code == 200:
        response_200 = []
        _response_200 = response.json()
        for componentsschemas_get_comments_list_item_data in _response_200:
            componentsschemas_get_comments_list_item = GetComments.from_dict(
                componentsschemas_get_comments_list_item_data
            )

            response_200.append(componentsschemas_get_comments_list_item)

        return response_200
    if response.status_code == 400:
        response_400 = DefaultError.from_dict(response.json())

        return response_400
    if response.status_code == 401:
        response_401 = DefaultError.from_dict(response.json())

        return response_401
    if response.status_code == 403:
        response_403 = DefaultError.from_dict(response.json())

        return response_403
    if response.status_code == 404:
        response_404 = DefaultError.from_dict(response.json())

        return response_404
    if response.status_code == 405:
        response_405 = DefaultError.from_dict(response.json())

        return response_405
    if response.status_code == 406:
        response_406 = DefaultError.from_dict(response.json())

        return response_406
    if response.status_code == 409:
        response_409 = DefaultError.from_dict(response.json())

        return response_409
    if response.status_code == 415:
        response_415 = DefaultError.from_dict(response.json())

        return response_415
    if response.status_code == 500:
        response_500 = DefaultError.from_dict(response.json())

        return response_500
    if response.status_code == 402:
        response_402 = DefaultError.from_dict(response.json())

        return response_402
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[Union[DefaultError, list["GetComments"]]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    issue_id_or_key: str,
    *,
    client: Union[AuthenticatedClient, Client],
    expand: Union[Unset, str] = UNSET,
    fields: Union[Unset, str] = UNSET,
    next_page: Union[Unset, str] = UNSET,
    order_by: Union[Unset, str] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    where: Union[Unset, str] = UNSET,
) -> Response[Union[DefaultError, list["GetComments"]]]:
    """Get Comments

     Gets all comments for an issue

    Args:
        issue_id_or_key (str):
        expand (Union[Unset, str]):
        fields (Union[Unset, str]):
        next_page (Union[Unset, str]):
        order_by (Union[Unset, str]):
        page_size (Union[Unset, int]):
        where (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[DefaultError, list['GetComments']]]
    """

    kwargs = _get_kwargs(
        issue_id_or_key=issue_id_or_key,
        expand=expand,
        fields=fields,
        next_page=next_page,
        order_by=order_by,
        page_size=page_size,
        where=where,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    issue_id_or_key: str,
    *,
    client: Union[AuthenticatedClient, Client],
    expand: Union[Unset, str] = UNSET,
    fields: Union[Unset, str] = UNSET,
    next_page: Union[Unset, str] = UNSET,
    order_by: Union[Unset, str] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    where: Union[Unset, str] = UNSET,
) -> Optional[Union[DefaultError, list["GetComments"]]]:
    """Get Comments

     Gets all comments for an issue

    Args:
        issue_id_or_key (str):
        expand (Union[Unset, str]):
        fields (Union[Unset, str]):
        next_page (Union[Unset, str]):
        order_by (Union[Unset, str]):
        page_size (Union[Unset, int]):
        where (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[DefaultError, list['GetComments']]
    """

    return sync_detailed(
        issue_id_or_key=issue_id_or_key,
        client=client,
        expand=expand,
        fields=fields,
        next_page=next_page,
        order_by=order_by,
        page_size=page_size,
        where=where,
    ).parsed


async def asyncio_detailed(
    issue_id_or_key: str,
    *,
    client: Union[AuthenticatedClient, Client],
    expand: Union[Unset, str] = UNSET,
    fields: Union[Unset, str] = UNSET,
    next_page: Union[Unset, str] = UNSET,
    order_by: Union[Unset, str] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    where: Union[Unset, str] = UNSET,
) -> Response[Union[DefaultError, list["GetComments"]]]:
    """Get Comments

     Gets all comments for an issue

    Args:
        issue_id_or_key (str):
        expand (Union[Unset, str]):
        fields (Union[Unset, str]):
        next_page (Union[Unset, str]):
        order_by (Union[Unset, str]):
        page_size (Union[Unset, int]):
        where (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[DefaultError, list['GetComments']]]
    """

    kwargs = _get_kwargs(
        issue_id_or_key=issue_id_or_key,
        expand=expand,
        fields=fields,
        next_page=next_page,
        order_by=order_by,
        page_size=page_size,
        where=where,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    issue_id_or_key: str,
    *,
    client: Union[AuthenticatedClient, Client],
    expand: Union[Unset, str] = UNSET,
    fields: Union[Unset, str] = UNSET,
    next_page: Union[Unset, str] = UNSET,
    order_by: Union[Unset, str] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    where: Union[Unset, str] = UNSET,
) -> Optional[Union[DefaultError, list["GetComments"]]]:
    """Get Comments

     Gets all comments for an issue

    Args:
        issue_id_or_key (str):
        expand (Union[Unset, str]):
        fields (Union[Unset, str]):
        next_page (Union[Unset, str]):
        order_by (Union[Unset, str]):
        page_size (Union[Unset, int]):
        where (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[DefaultError, list['GetComments']]
    """

    return (
        await asyncio_detailed(
            issue_id_or_key=issue_id_or_key,
            client=client,
            expand=expand,
            fields=fields,
            next_page=next_page,
            order_by=order_by,
            page_size=page_size,
            where=where,
        )
    ).parsed
