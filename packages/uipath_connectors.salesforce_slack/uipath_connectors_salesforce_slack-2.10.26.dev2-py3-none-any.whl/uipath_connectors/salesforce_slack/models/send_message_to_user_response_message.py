from typing import Any, Dict, Type, Optional
from pydantic import BaseModel, ConfigDict

from ..models.send_message_to_user_response_message_attachments_array_item_ref import (
    SendMessageToUserResponseMessageAttachmentsArrayItemRef,
)
from ..models.send_message_to_user_response_message_bot_profile import (
    SendMessageToUserResponseMessageBotProfile,
)
from ..models.send_message_to_user_response_message_icons import (
    SendMessageToUserResponseMessageIcons,
)
from ..models.send_message_to_user_response_message_root import (
    SendMessageToUserResponseMessageRoot,
)
from ..models.send_message_to_user_response_message_blocks_array_item_ref import (
    SendMessageToUserResponseMessageBlocksArrayItemRef,
)
from ..models.send_message_to_user_response_message_metadata import (
    SendMessageToUserResponseMessageMetadata,
)


class SendMessageToUserResponseMessage(BaseModel):
    """
    Attributes:
        app_id (Optional[str]):  Example: A02CEJTE85R.
        attachments (Optional[list['SendMessageToUserResponseMessageAttachmentsArrayItemRef']]):
        blocks (Optional[list['SendMessageToUserResponseMessageBlocksArrayItemRef']]):
        bot_id (Optional[str]):  Example: B02CRAP7A23.
        bot_profile (Optional[SendMessageToUserResponseMessageBotProfile]):
        icons (Optional[SendMessageToUserResponseMessageIcons]):
        metadata (Optional[SendMessageToUserResponseMessageMetadata]):
        root (Optional[SendMessageToUserResponseMessageRoot]):
        subtype (Optional[str]):  Example: thread_broadcast.
        team (Optional[str]):  Example: TCU0VUNLT.
        text (Optional[str]):  Example: Would you like to play a game?.
        thread_ts (Optional[str]):  Example: 1675217357.904929.
        ts (Optional[str]):  Example: 1631092102.000400.
        type_ (Optional[str]):  Example: message.
        user (Optional[str]):  Example: UCUFVVCKS.
        username (Optional[str]):  Example: My Bot lalitha new.
    """

    model_config = ConfigDict(extra="allow")

    app_id: Optional[str] = None
    attachments: Optional[
        list["SendMessageToUserResponseMessageAttachmentsArrayItemRef"]
    ] = None
    blocks: Optional[list["SendMessageToUserResponseMessageBlocksArrayItemRef"]] = None
    bot_id: Optional[str] = None
    bot_profile: Optional["SendMessageToUserResponseMessageBotProfile"] = None
    icons: Optional["SendMessageToUserResponseMessageIcons"] = None
    metadata: Optional["SendMessageToUserResponseMessageMetadata"] = None
    root: Optional["SendMessageToUserResponseMessageRoot"] = None
    subtype: Optional[str] = None
    team: Optional[str] = None
    text: Optional[str] = None
    thread_ts: Optional[str] = None
    ts: Optional[str] = None
    type_: Optional[str] = None
    user: Optional[str] = None
    username: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return self.model_dump(exclude_none=True)

    @classmethod
    def from_dict(
        cls: Type["SendMessageToUserResponseMessage"], src_dict: Dict[str, Any]
    ):
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
