from typing import Any, Dict, Type, Optional
from pydantic import BaseModel, ConfigDict

from ..models.send_reply_response_message_attachments_actions_array_item_ref import (
    SendReplyResponseMessageAttachmentsActionsArrayItemRef,
)


class SendReplyResponseMessageAttachmentsArrayItemRef(BaseModel):
    """
    Attributes:
        actions (Optional[list['SendReplyResponseMessageAttachmentsActionsArrayItemRef']]):
        callback_id (Optional[str]):  Example: wopr_game.
        color (Optional[str]):  Example: 3AA3E3.
        fallback (Optional[str]):  Example: You are unable to choose a game.
        id (Optional[int]):  Example: 1.0.
        text (Optional[str]):  Example: Choose a game to play.
    """

    model_config = ConfigDict(extra="allow")

    actions: Optional[
        list["SendReplyResponseMessageAttachmentsActionsArrayItemRef"]
    ] = None
    callback_id: Optional[str] = None
    color: Optional[str] = None
    fallback: Optional[str] = None
    id: Optional[int] = None
    text: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return self.model_dump(exclude_none=True)

    @classmethod
    def from_dict(
        cls: Type["SendReplyResponseMessageAttachmentsArrayItemRef"],
        src_dict: Dict[str, Any],
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
