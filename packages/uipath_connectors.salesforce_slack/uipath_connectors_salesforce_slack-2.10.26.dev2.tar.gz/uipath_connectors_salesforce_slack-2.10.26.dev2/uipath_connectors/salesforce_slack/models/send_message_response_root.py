from typing import Any, Dict, Type, Optional
from pydantic import BaseModel, ConfigDict

from ..models.send_message_response_root_metadata import SendMessageResponseRootMetadata
from ..models.send_message_response_root_icons import SendMessageResponseRootIcons
from ..models.send_message_response_root_blocks_array_item_ref import (
    SendMessageResponseRootBlocksArrayItemRef,
)


class SendMessageResponseRoot(BaseModel):
    """
    Attributes:
        app_id (Optional[str]):  Example: A02CEJTE85R.
        blocks (Optional[list['SendMessageResponseRootBlocksArrayItemRef']]):
        bot_id (Optional[str]):  Example: B02DYM5F1ST.
        icons (Optional[SendMessageResponseRootIcons]):
        is_locked (Optional[bool]):
        latest_reply (Optional[str]):  Example: 1675233584.607969.
        metadata (Optional[SendMessageResponseRootMetadata]):
        reply_count (Optional[int]):  Example: 4.0.
        reply_users (Optional[list[str]]):  Example: ['B02DYM5F1ST'].
        reply_users_count (Optional[int]):  Example: 1.0.
        subscribed (Optional[bool]):
        subtype (Optional[str]):  Example: bot_message.
        text (Optional[str]):  Example: failtest.
        thread_ts (Optional[str]):  Example: 1675217357.904929.
        ts (Optional[str]):  Example: 1675217357.904929.
        type_ (Optional[str]):  Example: message.
        username (Optional[str]):  Example: UiPath for Slack Staging.
    """

    model_config = ConfigDict(extra="allow")

    app_id: Optional[str] = None
    blocks: Optional[list["SendMessageResponseRootBlocksArrayItemRef"]] = None
    bot_id: Optional[str] = None
    icons: Optional["SendMessageResponseRootIcons"] = None
    is_locked: Optional[bool] = None
    latest_reply: Optional[str] = None
    metadata: Optional["SendMessageResponseRootMetadata"] = None
    reply_count: Optional[int] = None
    reply_users: Optional[list[str]] = None
    reply_users_count: Optional[int] = None
    subscribed: Optional[bool] = None
    subtype: Optional[str] = None
    text: Optional[str] = None
    thread_ts: Optional[str] = None
    ts: Optional[str] = None
    type_: Optional[str] = None
    username: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return self.model_dump(exclude_none=True)

    @classmethod
    def from_dict(cls: Type["SendMessageResponseRoot"], src_dict: Dict[str, Any]):
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
