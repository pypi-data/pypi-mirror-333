from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.default_error import DefaultError
from ...models.list_email import ListEmail
from ...types import Unset


def _get_kwargs(
    *,
    email_folder: str,
    additional_filters: Union[Unset, str] = UNSET,
    fields: Union[Unset, str] = UNSET,
    important_only: Union[Unset, bool] = UNSET,
    next_page: Union[Unset, str] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    starred_only: Union[Unset, bool] = UNSET,
    unread_only: Union[Unset, bool] = UNSET,
    with_attachments_only: Union[Unset, bool] = UNSET,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    params["emailFolder"] = email_folder

    params["additionalFilters"] = additional_filters

    params["fields"] = fields

    params["importantOnly"] = important_only

    params["nextPage"] = next_page

    params["pageSize"] = page_size

    params["starredOnly"] = starred_only

    params["unreadOnly"] = unread_only

    params["withAttachmentsOnly"] = with_attachments_only

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/ListEmails",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[DefaultError, list["ListEmail"]]]:
    if response.status_code == 200:
        response_200 = []
        _response_200 = response.json()
        for componentsschemas_list_email_list_item_data in _response_200:
            componentsschemas_list_email_list_item = ListEmail.from_dict(
                componentsschemas_list_email_list_item_data
            )

            response_200.append(componentsschemas_list_email_list_item)

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
) -> Response[Union[DefaultError, list["ListEmail"]]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    email_folder: str,
    additional_filters: Union[Unset, str] = UNSET,
    fields: Union[Unset, str] = UNSET,
    important_only: Union[Unset, bool] = UNSET,
    next_page: Union[Unset, str] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    starred_only: Union[Unset, bool] = UNSET,
    unread_only: Union[Unset, bool] = UNSET,
    with_attachments_only: Union[Unset, bool] = UNSET,
) -> Response[Union[DefaultError, list["ListEmail"]]]:
    """List Emails

     Lists emails according to filter criteria

    Args:
        email_folder (str):
        additional_filters (Union[Unset, str]):
        fields (Union[Unset, str]):
        important_only (Union[Unset, bool]):
        next_page (Union[Unset, str]):
        page_size (Union[Unset, int]):
        starred_only (Union[Unset, bool]):
        unread_only (Union[Unset, bool]):
        with_attachments_only (Union[Unset, bool]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[DefaultError, list['ListEmail']]]
    """

    kwargs = _get_kwargs(
        email_folder=email_folder,
        additional_filters=additional_filters,
        fields=fields,
        important_only=important_only,
        next_page=next_page,
        page_size=page_size,
        starred_only=starred_only,
        unread_only=unread_only,
        with_attachments_only=with_attachments_only,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: Union[AuthenticatedClient, Client],
    email_folder: str,
    additional_filters: Union[Unset, str] = UNSET,
    fields: Union[Unset, str] = UNSET,
    important_only: Union[Unset, bool] = UNSET,
    next_page: Union[Unset, str] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    starred_only: Union[Unset, bool] = UNSET,
    unread_only: Union[Unset, bool] = UNSET,
    with_attachments_only: Union[Unset, bool] = UNSET,
) -> Optional[Union[DefaultError, list["ListEmail"]]]:
    """List Emails

     Lists emails according to filter criteria

    Args:
        email_folder (str):
        additional_filters (Union[Unset, str]):
        fields (Union[Unset, str]):
        important_only (Union[Unset, bool]):
        next_page (Union[Unset, str]):
        page_size (Union[Unset, int]):
        starred_only (Union[Unset, bool]):
        unread_only (Union[Unset, bool]):
        with_attachments_only (Union[Unset, bool]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[DefaultError, list['ListEmail']]
    """

    return sync_detailed(
        client=client,
        email_folder=email_folder,
        additional_filters=additional_filters,
        fields=fields,
        important_only=important_only,
        next_page=next_page,
        page_size=page_size,
        starred_only=starred_only,
        unread_only=unread_only,
        with_attachments_only=with_attachments_only,
    ).parsed


async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    email_folder: str,
    additional_filters: Union[Unset, str] = UNSET,
    fields: Union[Unset, str] = UNSET,
    important_only: Union[Unset, bool] = UNSET,
    next_page: Union[Unset, str] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    starred_only: Union[Unset, bool] = UNSET,
    unread_only: Union[Unset, bool] = UNSET,
    with_attachments_only: Union[Unset, bool] = UNSET,
) -> Response[Union[DefaultError, list["ListEmail"]]]:
    """List Emails

     Lists emails according to filter criteria

    Args:
        email_folder (str):
        additional_filters (Union[Unset, str]):
        fields (Union[Unset, str]):
        important_only (Union[Unset, bool]):
        next_page (Union[Unset, str]):
        page_size (Union[Unset, int]):
        starred_only (Union[Unset, bool]):
        unread_only (Union[Unset, bool]):
        with_attachments_only (Union[Unset, bool]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[DefaultError, list['ListEmail']]]
    """

    kwargs = _get_kwargs(
        email_folder=email_folder,
        additional_filters=additional_filters,
        fields=fields,
        important_only=important_only,
        next_page=next_page,
        page_size=page_size,
        starred_only=starred_only,
        unread_only=unread_only,
        with_attachments_only=with_attachments_only,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: Union[AuthenticatedClient, Client],
    email_folder: str,
    additional_filters: Union[Unset, str] = UNSET,
    fields: Union[Unset, str] = UNSET,
    important_only: Union[Unset, bool] = UNSET,
    next_page: Union[Unset, str] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    starred_only: Union[Unset, bool] = UNSET,
    unread_only: Union[Unset, bool] = UNSET,
    with_attachments_only: Union[Unset, bool] = UNSET,
) -> Optional[Union[DefaultError, list["ListEmail"]]]:
    """List Emails

     Lists emails according to filter criteria

    Args:
        email_folder (str):
        additional_filters (Union[Unset, str]):
        fields (Union[Unset, str]):
        important_only (Union[Unset, bool]):
        next_page (Union[Unset, str]):
        page_size (Union[Unset, int]):
        starred_only (Union[Unset, bool]):
        unread_only (Union[Unset, bool]):
        with_attachments_only (Union[Unset, bool]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[DefaultError, list['ListEmail']]
    """

    return (
        await asyncio_detailed(
            client=client,
            email_folder=email_folder,
            additional_filters=additional_filters,
            fields=fields,
            important_only=important_only,
            next_page=next_page,
            page_size=page_size,
            starred_only=starred_only,
            unread_only=unread_only,
            with_attachments_only=with_attachments_only,
        )
    ).parsed
