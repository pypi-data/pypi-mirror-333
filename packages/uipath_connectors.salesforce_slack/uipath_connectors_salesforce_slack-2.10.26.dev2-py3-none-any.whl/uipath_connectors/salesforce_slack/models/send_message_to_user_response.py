from typing import Any, Dict, Type, Optional
from pydantic import BaseModel, ConfigDict

from ..models.send_message_to_user_response_blocks_array_item_ref import (
    SendMessageToUserResponseBlocksArrayItemRef,
)
from ..models.send_message_to_user_response_response_metadata import (
    SendMessageToUserResponseResponseMetadata,
)
from ..models.send_message_to_user_response_metadata import (
    SendMessageToUserResponseMetadata,
)
from ..models.send_message_to_user_response_message import (
    SendMessageToUserResponseMessage,
)
from ..models.send_message_to_user_response_root import SendMessageToUserResponseRoot
from ..models.send_message_to_user_response_icons import SendMessageToUserResponseIcons


class SendMessageToUserResponse(BaseModel):
    """
    Attributes:
        app_id (Optional[str]):  Example: A02CEJTE85R.
        blocks (Optional[list['SendMessageToUserResponseBlocksArrayItemRef']]):
        channel (Optional[str]): User Example: C02CAP3LAAG.
        icons (Optional[SendMessageToUserResponseIcons]):
        message (Optional[SendMessageToUserResponseMessage]):
        metadata (Optional[SendMessageToUserResponseMetadata]):
        ok (Optional[bool]):  Example: True.
        response_metadata (Optional[SendMessageToUserResponseResponseMetadata]):
        root (Optional[SendMessageToUserResponseRoot]):
        subtype (Optional[str]):  Example: thread_broadcast.
        thread_ts (Optional[str]): The ID (timestamp) of the message sent Example: 1675217357.904929.
        ts (Optional[str]): The ID (timestamp) of the message sent Example: 1631092102.000400.
        username (Optional[str]): Bot name Example: My Bot lalitha new.
    """

    model_config = ConfigDict(extra="allow")

    app_id: Optional[str] = None
    blocks: Optional[list["SendMessageToUserResponseBlocksArrayItemRef"]] = None
    channel: Optional[str] = None
    icons: Optional["SendMessageToUserResponseIcons"] = None
    message: Optional["SendMessageToUserResponseMessage"] = None
    metadata: Optional["SendMessageToUserResponseMetadata"] = None
    ok: Optional[bool] = None
    response_metadata: Optional["SendMessageToUserResponseResponseMetadata"] = None
    root: Optional["SendMessageToUserResponseRoot"] = None
    subtype: Optional[str] = None
    thread_ts: Optional[str] = None
    ts: Optional[str] = None
    username: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return self.model_dump(exclude_none=True)

    @classmethod
    def from_dict(cls: Type["SendMessageToUserResponse"], src_dict: Dict[str, Any]):
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
