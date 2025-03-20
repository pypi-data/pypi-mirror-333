from typing import Any, Dict, Type, Optional
from pydantic import BaseModel, ConfigDict

from ..models.set_channel_topic_response_purpose import SetChannelTopicResponsePurpose
from ..models.set_channel_topic_response_latest import SetChannelTopicResponseLatest


class SetChannelTopicResponse(BaseModel):
    """
    Attributes:
        created (Optional[int]):  Example: 1.649195947E9.
        creator (Optional[str]):  Example: U12345678.
        id (Optional[str]):  Example: C12345678.
        is_archived (Optional[bool]):
        is_channel (Optional[bool]):  Example: True.
        is_ext_shared (Optional[bool]):
        is_frozen (Optional[bool]):
        is_general (Optional[bool]):
        is_group (Optional[bool]):
        is_im (Optional[bool]):
        is_member (Optional[bool]):  Example: True.
        is_mpim (Optional[bool]):
        is_org_shared (Optional[bool]):
        is_pending_ext_shared (Optional[bool]):
        is_private (Optional[bool]):
        is_shared (Optional[bool]):
        last_read (Optional[str]):  Example: 1649869848.627809.
        latest (Optional[SetChannelTopicResponseLatest]):
        name (Optional[str]):  Example: tips-and-tricks.
        name_normalized (Optional[str]):  Example: tips-and-tricks.
        parent_conversation (Optional[str]):
        pending_connected_team_ids (Optional[list[Any]]):
        pending_shared (Optional[list[Any]]):
        previous_names (Optional[list[Any]]):
        purpose (Optional[SetChannelTopicResponsePurpose]):
        shared_team_ids (Optional[list[str]]):  Example: ['T12345678'].
        unlinked (Optional[int]):  Example: 0.0.
        unread_count (Optional[int]):  Example: 1.0.
        unread_count_display (Optional[int]):  Example: 0.0.
    """

    model_config = ConfigDict(extra="allow")

    created: Optional[int] = None
    creator: Optional[str] = None
    id: Optional[str] = None
    is_archived: Optional[bool] = None
    is_channel: Optional[bool] = None
    is_ext_shared: Optional[bool] = None
    is_frozen: Optional[bool] = None
    is_general: Optional[bool] = None
    is_group: Optional[bool] = None
    is_im: Optional[bool] = None
    is_member: Optional[bool] = None
    is_mpim: Optional[bool] = None
    is_org_shared: Optional[bool] = None
    is_pending_ext_shared: Optional[bool] = None
    is_private: Optional[bool] = None
    is_shared: Optional[bool] = None
    last_read: Optional[str] = None
    latest: Optional["SetChannelTopicResponseLatest"] = None
    name: Optional[str] = None
    name_normalized: Optional[str] = None
    parent_conversation: Optional[str] = None
    pending_connected_team_ids: Optional[list[Any]] = None
    pending_shared: Optional[list[Any]] = None
    previous_names: Optional[list[Any]] = None
    purpose: Optional["SetChannelTopicResponsePurpose"] = None
    shared_team_ids: Optional[list[str]] = None
    unlinked: Optional[int] = None
    unread_count: Optional[int] = None
    unread_count_display: Optional[int] = None

    def to_dict(self) -> Dict[str, Any]:
        return self.model_dump(exclude_none=True)

    @classmethod
    def from_dict(cls: Type["SetChannelTopicResponse"], src_dict: Dict[str, Any]):
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
