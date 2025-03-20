from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response
from ... import errors

from ...models.default_error import DefaultError
from ...models.list_email import ListEmail


def _get_kwargs(
    *,
    email_folder: str,
    additional_filters: Optional[str] = None,
    fields: Optional[str] = None,
    important_only: Optional[bool] = None,
    next_page: Optional[str] = None,
    page_size: Optional[int] = None,
    starred_only: Optional[bool] = None,
    unread_only: Optional[bool] = None,
    with_attachments_only: Optional[bool] = None,
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

    params = {k: v for k, v in params.items() if v is not None}

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
    additional_filters: Optional[str] = None,
    fields: Optional[str] = None,
    important_only: Optional[bool] = None,
    next_page: Optional[str] = None,
    page_size: Optional[int] = None,
    starred_only: Optional[bool] = None,
    unread_only: Optional[bool] = None,
    with_attachments_only: Optional[bool] = None,
) -> Response[Union[DefaultError, list["ListEmail"]]]:
    """List Emails

     Lists emails according to filter criteria

    Args:
        email_folder (str):
        additional_filters (Optional[str]):
        fields (Optional[str]):
        important_only (Optional[bool]):
        next_page (Optional[str]):
        page_size (Optional[int]):
        starred_only (Optional[bool]):
        unread_only (Optional[bool]):
        with_attachments_only (Optional[bool]):

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
    additional_filters: Optional[str] = None,
    fields: Optional[str] = None,
    important_only: Optional[bool] = None,
    next_page: Optional[str] = None,
    page_size: Optional[int] = None,
    starred_only: Optional[bool] = None,
    unread_only: Optional[bool] = None,
    with_attachments_only: Optional[bool] = None,
) -> Optional[Union[DefaultError, list["ListEmail"]]]:
    """List Emails

     Lists emails according to filter criteria

    Args:
        email_folder (str):
        additional_filters (Optional[str]):
        fields (Optional[str]):
        important_only (Optional[bool]):
        next_page (Optional[str]):
        page_size (Optional[int]):
        starred_only (Optional[bool]):
        unread_only (Optional[bool]):
        with_attachments_only (Optional[bool]):

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
    additional_filters: Optional[str] = None,
    fields: Optional[str] = None,
    important_only: Optional[bool] = None,
    next_page: Optional[str] = None,
    page_size: Optional[int] = None,
    starred_only: Optional[bool] = None,
    unread_only: Optional[bool] = None,
    with_attachments_only: Optional[bool] = None,
) -> Response[Union[DefaultError, list["ListEmail"]]]:
    """List Emails

     Lists emails according to filter criteria

    Args:
        email_folder (str):
        additional_filters (Optional[str]):
        fields (Optional[str]):
        important_only (Optional[bool]):
        next_page (Optional[str]):
        page_size (Optional[int]):
        starred_only (Optional[bool]):
        unread_only (Optional[bool]):
        with_attachments_only (Optional[bool]):

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
    additional_filters: Optional[str] = None,
    fields: Optional[str] = None,
    important_only: Optional[bool] = None,
    next_page: Optional[str] = None,
    page_size: Optional[int] = None,
    starred_only: Optional[bool] = None,
    unread_only: Optional[bool] = None,
    with_attachments_only: Optional[bool] = None,
) -> Optional[Union[DefaultError, list["ListEmail"]]]:
    """List Emails

     Lists emails according to filter criteria

    Args:
        email_folder (str):
        additional_filters (Optional[str]):
        fields (Optional[str]):
        important_only (Optional[bool]):
        next_page (Optional[str]):
        page_size (Optional[int]):
        starred_only (Optional[bool]):
        unread_only (Optional[bool]):
        with_attachments_only (Optional[bool]):

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
