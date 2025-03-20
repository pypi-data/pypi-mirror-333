from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response
from ... import errors

from ...models.default_error import DefaultError
from ...models.upload_file_body import UploadFileBody
from ...models.upload_file_response import UploadFileResponse


def _get_kwargs(
    *,
    body: UploadFileBody,
    send_as: str,
    channels: Optional[str] = None,
    filename: Optional[str] = None,
    filetype: Optional[str] = None,
    initial_comment: Optional[str] = None,
    thread_ts: Optional[str] = None,
    title: Optional[str] = None,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    params: dict[str, Any] = {}

    params["send_as"] = send_as

    params["channels"] = channels

    params["filename"] = filename

    params["filetype"] = filetype

    params["initial_comment"] = initial_comment

    params["thread_ts"] = thread_ts

    params["title"] = title

    params = {k: v for k, v in params.items() if v is not None}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/send_files_to_channel",
        "params": params,
    }

    _body = body.to_multipart()

    _kwargs["files"] = _body

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[DefaultError, UploadFileResponse]]:
    if response.status_code == 200:
        response_200 = UploadFileResponse.from_dict(response.json())

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
) -> Response[Union[DefaultError, UploadFileResponse]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    body: UploadFileBody,
    send_as: str,
    channels: Optional[str] = None,
    filename: Optional[str] = None,
    filetype: Optional[str] = None,
    initial_comment: Optional[str] = None,
    thread_ts: Optional[str] = None,
    title: Optional[str] = None,
) -> Response[Union[DefaultError, UploadFileResponse]]:
    """Send File to Channel

     Upload and send a file to one or more channels in Slack

    Args:
        send_as (str):
        channels (Optional[str]):
        filename (Optional[str]):
        filetype (Optional[str]):
        initial_comment (Optional[str]):
        thread_ts (Optional[str]):
        title (Optional[str]):
        body (UploadFileBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[DefaultError, UploadFileResponse]]
    """

    kwargs = _get_kwargs(
        body=body,
        send_as=send_as,
        channels=channels,
        filename=filename,
        filetype=filetype,
        initial_comment=initial_comment,
        thread_ts=thread_ts,
        title=title,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: Union[AuthenticatedClient, Client],
    body: UploadFileBody,
    send_as: str,
    channels: Optional[str] = None,
    filename: Optional[str] = None,
    filetype: Optional[str] = None,
    initial_comment: Optional[str] = None,
    thread_ts: Optional[str] = None,
    title: Optional[str] = None,
) -> Optional[Union[DefaultError, UploadFileResponse]]:
    """Send File to Channel

     Upload and send a file to one or more channels in Slack

    Args:
        send_as (str):
        channels (Optional[str]):
        filename (Optional[str]):
        filetype (Optional[str]):
        initial_comment (Optional[str]):
        thread_ts (Optional[str]):
        title (Optional[str]):
        body (UploadFileBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[DefaultError, UploadFileResponse]
    """

    return sync_detailed(
        client=client,
        body=body,
        send_as=send_as,
        channels=channels,
        filename=filename,
        filetype=filetype,
        initial_comment=initial_comment,
        thread_ts=thread_ts,
        title=title,
    ).parsed


async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    body: UploadFileBody,
    send_as: str,
    channels: Optional[str] = None,
    filename: Optional[str] = None,
    filetype: Optional[str] = None,
    initial_comment: Optional[str] = None,
    thread_ts: Optional[str] = None,
    title: Optional[str] = None,
) -> Response[Union[DefaultError, UploadFileResponse]]:
    """Send File to Channel

     Upload and send a file to one or more channels in Slack

    Args:
        send_as (str):
        channels (Optional[str]):
        filename (Optional[str]):
        filetype (Optional[str]):
        initial_comment (Optional[str]):
        thread_ts (Optional[str]):
        title (Optional[str]):
        body (UploadFileBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[DefaultError, UploadFileResponse]]
    """

    kwargs = _get_kwargs(
        body=body,
        send_as=send_as,
        channels=channels,
        filename=filename,
        filetype=filetype,
        initial_comment=initial_comment,
        thread_ts=thread_ts,
        title=title,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: Union[AuthenticatedClient, Client],
    body: UploadFileBody,
    send_as: str,
    channels: Optional[str] = None,
    filename: Optional[str] = None,
    filetype: Optional[str] = None,
    initial_comment: Optional[str] = None,
    thread_ts: Optional[str] = None,
    title: Optional[str] = None,
) -> Optional[Union[DefaultError, UploadFileResponse]]:
    """Send File to Channel

     Upload and send a file to one or more channels in Slack

    Args:
        send_as (str):
        channels (Optional[str]):
        filename (Optional[str]):
        filetype (Optional[str]):
        initial_comment (Optional[str]):
        thread_ts (Optional[str]):
        title (Optional[str]):
        body (UploadFileBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[DefaultError, UploadFileResponse]
    """

    return (
        await asyncio_detailed(
            client=client,
            body=body,
            send_as=send_as,
            channels=channels,
            filename=filename,
            filetype=filetype,
            initial_comment=initial_comment,
            thread_ts=thread_ts,
            title=title,
        )
    ).parsed
