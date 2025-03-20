from typing import Any, Dict, Type, Optional
from pydantic import BaseModel, ConfigDict

from ..models.send_reply_request_formatting_options_parse import (
    SendReplyRequestFormattingOptionsParse,
)
from ..models.send_reply_request_blocks_array_item_ref import (
    SendReplyRequestBlocksArrayItemRef,
)
from ..models.send_reply_request_attachments_array_item_ref import (
    SendReplyRequestAttachmentsArrayItemRef,
)
from ..models.send_reply_request_metadata import SendReplyRequestMetadata


class SendReplyRequest(BaseModel):
    """
    Attributes:
        channel (str): Select the public or private channel from the dropdown or pass channel name or channel ID. Ex:
            demo-slack-channel1 Example: C02CAP3LAAG.
        message_to_send (str): The formatted text of the message to be sent. This is also the main 'block' section text
            Example: string.
        thread_ts (str): Message timestamp Example: 1675217357.904929.
        attachments (Optional[list['SendReplyRequestAttachmentsArrayItemRef']]):
        blocks (Optional[list['SendReplyRequestBlocksArrayItemRef']]):
        buttons (Optional[str]): Buttons actions Example: string.
        fields (Optional[str]): Message fields Example: string.
        icon_emoji (Optional[str]): Bot icon
        icon_url (Optional[str]): URL to an image to use as the icon for this message Example: https://a.slack-
            edge.com/production-standard-emoji-assets/14.0/apple-medium/0032-fe0f-20e3@2x.png.
        image (Optional[str]): The URL of the secondary image attachment to be shared as part of the message. The image
            will always be at the bottom of the entire message block Example: string.
        link_names (Optional[bool]): Whether to link and mention all the user groups automatically if the respective
            names are mentioned in the text message? Example: True.
        metadata (Optional[SendReplyRequestMetadata]):
        mrkdwn (Optional[bool]):  Example: True.
        parse (Optional[SendReplyRequestFormattingOptionsParse]): Change how messages are treated. Pass 'none' for
            removing hyperlinks and pass 'full' to ignore slack's default formatting Example: none.
        reply_broadcast (Optional[bool]):  Whether reply should be made visible to everyone in the channel or
            conversation? Defaults to false Example: True.
        unfurl_links (Optional[bool]): Whether to display the preview of the links mentioned in the text message?
            Example: True.
        unfurl_media (Optional[bool]):
        username (Optional[str]): Bot name Example: My Bot lalitha new.
    """

    model_config = ConfigDict(extra="allow")

    channel: str
    message_to_send: str
    thread_ts: str
    attachments: Optional[list["SendReplyRequestAttachmentsArrayItemRef"]] = None
    blocks: Optional[list["SendReplyRequestBlocksArrayItemRef"]] = None
    buttons: Optional[str] = None
    fields: Optional[str] = None
    icon_emoji: Optional[str] = None
    icon_url: Optional[str] = None
    image: Optional[str] = None
    link_names: Optional[bool] = None
    metadata: Optional["SendReplyRequestMetadata"] = None
    mrkdwn: Optional[bool] = None
    parse: Optional[SendReplyRequestFormattingOptionsParse] = None
    reply_broadcast: Optional[bool] = None
    unfurl_links: Optional[bool] = None
    unfurl_media: Optional[bool] = None
    username: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return self.model_dump(exclude_none=True)

    @classmethod
    def from_dict(cls: Type["SendReplyRequest"], src_dict: Dict[str, Any]):
        return cls.model_validate(src_dict)

    @property
    def additional_keys(self) -> list[str]:
        base_fields = self.model_fields.keys()
        return [k for k in self.__dict__ if k not in base_fields]

    def __getitem__(self, key: str) -> Any:
        if key in self.__dict__:
            return self.__dict__[key]
        raise KeyError(key)

    def __setitem__(self, key: str, value: Any) -> None:
        self.__dict__[key] = value

    def __delitem__(self, key: str) -> None:
        if key in self.__dict__:
            del self.__dict__[key]
        else:
            raise KeyError(key)

    def __contains__(self, key: str) -> bool:
        return key in self.__dict__
