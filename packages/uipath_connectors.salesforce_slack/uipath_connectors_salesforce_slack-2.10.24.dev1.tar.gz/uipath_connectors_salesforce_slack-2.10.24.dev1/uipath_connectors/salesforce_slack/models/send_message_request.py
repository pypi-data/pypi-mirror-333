from typing import Any, TypeVar, TYPE_CHECKING

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.send_message_request_formatting_options_parse import (
    SendMessageRequestFormattingOptionsParse,
)
from typing import Union

if TYPE_CHECKING:
    from ..models.send_message_request_metadata import SendMessageRequestMetadata
    from ..models.send_message_request_attachments_array_item_ref import (
        SendMessageRequestAttachmentsArrayItemRef,
    )


T = TypeVar("T", bound="SendMessageRequest")


@_attrs_define
class SendMessageRequest:
    """
    Attributes:
        channel (str): Channel name/ID Example: C02CAP3LAAG.
        message_to_send (str): The formatted text of the message to be sent. This is also the main 'block' section text
            Example: string.
        attachments (Union[Unset, list['SendMessageRequestAttachmentsArrayItemRef']]):
        buttons (Union[Unset, str]): Buttons actions Example: string.
        fields (Union[Unset, str]): Message fields Example: string.
        icon_emoji (Union[Unset, str]): Bot icon
        icon_url (Union[Unset, str]): URL to an image to use as the icon for this message Example: https://a.slack-
            edge.com/production-standard-emoji-assets/14.0/apple-medium/0032-fe0f-20e3@2x.png.
        image (Union[Unset, str]): The URL of the secondary image attachment to be shared as part of the message. The
            image will always be at the bottom of the entire message block Example: string.
        link_names (Union[Unset, bool]): Whether to link and mention all the user groups automatically if the respective
            names are mentioned in the text message? Example: True.
        metadata (Union[Unset, SendMessageRequestMetadata]):
        mrkdwn (Union[Unset, bool]):  Example: True.
        parse (Union[Unset, SendMessageRequestFormattingOptionsParse]): Change how messages are treated. Pass 'none' for
            removing hyperlinks and pass 'full' to ignore slack's default formatting Example: none.
        reply_broadcast (Union[Unset, bool]):  Example: True.
        thread_ts (Union[Unset, str]): The ID (timestamp) of the message sent Example: 1675217357.904929.
        unfurl_links (Union[Unset, bool]): Whether to display the preview of the links mentioned in the text message?
            Example: True.
        unfurl_media (Union[Unset, bool]):
        username (Union[Unset, str]): Bot name Example: My Bot lalitha new.
    """

    channel: str
    message_to_send: str
    attachments: Union[Unset, list["SendMessageRequestAttachmentsArrayItemRef"]] = UNSET
    buttons: Union[Unset, str] = UNSET
    fields: Union[Unset, str] = UNSET
    icon_emoji: Union[Unset, str] = UNSET
    icon_url: Union[Unset, str] = UNSET
    image: Union[Unset, str] = UNSET
    link_names: Union[Unset, bool] = UNSET
    metadata: Union[Unset, "SendMessageRequestMetadata"] = UNSET
    mrkdwn: Union[Unset, bool] = UNSET
    parse: Union[Unset, SendMessageRequestFormattingOptionsParse] = UNSET
    reply_broadcast: Union[Unset, bool] = UNSET
    thread_ts: Union[Unset, str] = UNSET
    unfurl_links: Union[Unset, bool] = UNSET
    unfurl_media: Union[Unset, bool] = UNSET
    username: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:

        channel = self.channel

        message_to_send = self.message_to_send

        attachments: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.attachments, Unset):
            attachments = []
            for (
                componentsschemas_send_message_request_attachments_item_data
            ) in self.attachments:
                componentsschemas_send_message_request_attachments_item = componentsschemas_send_message_request_attachments_item_data.to_dict()
                attachments.append(
                    componentsschemas_send_message_request_attachments_item
                )

        buttons = self.buttons

        fields = self.fields

        icon_emoji = self.icon_emoji

        icon_url = self.icon_url

        image = self.image

        link_names = self.link_names

        metadata: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.metadata, Unset):
            metadata = self.metadata.to_dict()

        mrkdwn = self.mrkdwn

        parse: Union[Unset, str] = UNSET
        if not isinstance(self.parse, Unset):
            parse = self.parse.value

        reply_broadcast = self.reply_broadcast

        thread_ts = self.thread_ts

        unfurl_links = self.unfurl_links

        unfurl_media = self.unfurl_media

        username = self.username

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "channel": channel,
                "messageToSend": message_to_send,
            }
        )
        if attachments is not UNSET:
            field_dict["attachments"] = attachments
        if buttons is not UNSET:
            field_dict["buttons"] = buttons
        if fields is not UNSET:
            field_dict["fields"] = fields
        if icon_emoji is not UNSET:
            field_dict["icon_emoji"] = icon_emoji
        if icon_url is not UNSET:
            field_dict["icon_url"] = icon_url
        if image is not UNSET:
            field_dict["image"] = image
        if link_names is not UNSET:
            field_dict["link_names"] = link_names
        if metadata is not UNSET:
            field_dict["metadata"] = metadata
        if mrkdwn is not UNSET:
            field_dict["mrkdwn"] = mrkdwn
        if parse is not UNSET:
            field_dict["parse"] = parse
        if reply_broadcast is not UNSET:
            field_dict["reply_broadcast"] = reply_broadcast
        if thread_ts is not UNSET:
            field_dict["thread_ts"] = thread_ts
        if unfurl_links is not UNSET:
            field_dict["unfurl_links"] = unfurl_links
        if unfurl_media is not UNSET:
            field_dict["unfurl_media"] = unfurl_media
        if username is not UNSET:
            field_dict["username"] = username

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.send_message_request_metadata import SendMessageRequestMetadata
        from ..models.send_message_request_attachments_array_item_ref import (
            SendMessageRequestAttachmentsArrayItemRef,
        )

        d = src_dict.copy()
        channel = d.pop("channel")

        message_to_send = d.pop("messageToSend")

        attachments = []
        _attachments = d.pop("attachments", UNSET)
        for componentsschemas_send_message_request_attachments_item_data in (
            _attachments or []
        ):
            componentsschemas_send_message_request_attachments_item = (
                SendMessageRequestAttachmentsArrayItemRef.from_dict(
                    componentsschemas_send_message_request_attachments_item_data
                )
            )

            attachments.append(componentsschemas_send_message_request_attachments_item)

        buttons = d.pop("buttons", UNSET)

        fields = d.pop("fields", UNSET)

        icon_emoji = d.pop("icon_emoji", UNSET)

        icon_url = d.pop("icon_url", UNSET)

        image = d.pop("image", UNSET)

        link_names = d.pop("link_names", UNSET)

        _metadata = d.pop("metadata", UNSET)
        metadata: Union[Unset, SendMessageRequestMetadata]
        if isinstance(_metadata, Unset):
            metadata = UNSET
        else:
            metadata = SendMessageRequestMetadata.from_dict(_metadata)

        mrkdwn = d.pop("mrkdwn", UNSET)

        _parse = d.pop("parse", UNSET)
        parse: Union[Unset, SendMessageRequestFormattingOptionsParse]
        if isinstance(_parse, Unset):
            parse = UNSET
        else:
            parse = SendMessageRequestFormattingOptionsParse(_parse)

        reply_broadcast = d.pop("reply_broadcast", UNSET)

        thread_ts = d.pop("thread_ts", UNSET)

        unfurl_links = d.pop("unfurl_links", UNSET)

        unfurl_media = d.pop("unfurl_media", UNSET)

        username = d.pop("username", UNSET)

        send_message_request = cls(
            channel=channel,
            message_to_send=message_to_send,
            attachments=attachments,
            buttons=buttons,
            fields=fields,
            icon_emoji=icon_emoji,
            icon_url=icon_url,
            image=image,
            link_names=link_names,
            metadata=metadata,
            mrkdwn=mrkdwn,
            parse=parse,
            reply_broadcast=reply_broadcast,
            thread_ts=thread_ts,
            unfurl_links=unfurl_links,
            unfurl_media=unfurl_media,
            username=username,
        )

        send_message_request.additional_properties = d
        return send_message_request

    @property
    def additional_keys(self) -> list[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
