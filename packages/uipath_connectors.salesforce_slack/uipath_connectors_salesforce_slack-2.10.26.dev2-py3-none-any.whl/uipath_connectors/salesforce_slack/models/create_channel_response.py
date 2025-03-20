from typing import Any, Dict, Type, Optional
from pydantic import BaseModel, ConfigDict

from ..models.create_channel_response_topic import CreateChannelResponseTopic
from ..models.create_channel_response_purpose import CreateChannelResponsePurpose


class CreateChannelResponse(BaseModel):
    """
    Attributes:
        created (Optional[int]):  Example: 1.536962679E9.
        creator (Optional[str]):  Example: UCTGFDTEV.
        id (Optional[str]): The ID of the channel Example: CCU0VUWKD.
        is_archived (Optional[bool]):  Example: True.
        is_channel (Optional[bool]):  Example: True.
        is_ext_shared (Optional[bool]):
        is_general (Optional[bool]):
        is_group (Optional[bool]):
        is_im (Optional[bool]):
        is_member (Optional[bool]):
        is_mpim (Optional[bool]):
        is_open (Optional[bool]):  Example: True.
        is_org_shared (Optional[bool]):
        is_pending_ext_shared (Optional[bool]):
        is_private (Optional[bool]): Whether the channel is private or not? Default is false
        is_shared (Optional[bool]):
        last_read (Optional[str]):  Example: 0000000000.000000.
        name (Optional[str]): The name of the channel to create Example: random.
        name_normalized (Optional[str]):  Example: random.
        priority (Optional[int]):  Example: 0.0.
        purpose (Optional[CreateChannelResponsePurpose]):
        shared_team_ids (Optional[list[str]]):  Example: ['TCU0VUNLT'].
        topic (Optional[CreateChannelResponseTopic]):
        unlinked (Optional[int]):  Example: 0.0.
    """

    model_config = ConfigDict(extra="allow")

    created: Optional[int] = None
    creator: Optional[str] = None
    id: Optional[str] = None
    is_archived: Optional[bool] = None
    is_channel: Optional[bool] = None
    is_ext_shared: Optional[bool] = None
    is_general: Optional[bool] = None
    is_group: Optional[bool] = None
    is_im: Optional[bool] = None
    is_member: Optional[bool] = None
    is_mpim: Optional[bool] = None
    is_open: Optional[bool] = None
    is_org_shared: Optional[bool] = None
    is_pending_ext_shared: Optional[bool] = None
    is_private: Optional[bool] = None
    is_shared: Optional[bool] = None
    last_read: Optional[str] = None
    name: Optional[str] = None
    name_normalized: Optional[str] = None
    priority: Optional[int] = None
    purpose: Optional["CreateChannelResponsePurpose"] = None
    shared_team_ids: Optional[list[str]] = None
    topic: Optional["CreateChannelResponseTopic"] = None
    unlinked: Optional[int] = None

    def to_dict(self) -> Dict[str, Any]:
        return self.model_dump(exclude_none=True)

    @classmethod
    def from_dict(cls: Type["CreateChannelResponse"], src_dict: Dict[str, Any]):
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
