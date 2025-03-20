from typing import Any, Dict, Type, Optional
from pydantic import BaseModel, ConfigDict

from ..models.send_message_to_user_response_message_bot_profile_icons import (
    SendMessageToUserResponseMessageBotProfileIcons,
)


class SendMessageToUserResponseMessageBotProfile(BaseModel):
    """
    Attributes:
        app_id (Optional[str]):  Example: A44S6RJ2V.
        deleted (Optional[bool]):
        icons (Optional[SendMessageToUserResponseMessageBotProfileIcons]):
        id (Optional[str]):  Example: B02CRAP7A23.
        name (Optional[str]):  Example: CE DEV App.
        team_id (Optional[str]):  Example: TCU0VUNLT.
        updated (Optional[int]):  Example: 1.63056859E9.
    """

    model_config = ConfigDict(extra="allow")

    app_id: Optional[str] = None
    deleted: Optional[bool] = None
    icons: Optional["SendMessageToUserResponseMessageBotProfileIcons"] = None
    id: Optional[str] = None
    name: Optional[str] = None
    team_id: Optional[str] = None
    updated: Optional[int] = None

    def to_dict(self) -> Dict[str, Any]:
        return self.model_dump(exclude_none=True)

    @classmethod
    def from_dict(
        cls: Type["SendMessageToUserResponseMessageBotProfile"],
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
