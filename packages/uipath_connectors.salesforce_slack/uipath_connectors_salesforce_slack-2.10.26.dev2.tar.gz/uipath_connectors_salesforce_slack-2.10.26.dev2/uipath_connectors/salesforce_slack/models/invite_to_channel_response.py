from typing import Any, Dict, Type, Optional
from pydantic import BaseModel, ConfigDict

from ..models.invite_to_channel_response_topic import InviteToChannelResponseTopic
from ..models.invite_to_channel_response_purpose import InviteToChannelResponsePurpose


class InviteToChannelResponse(BaseModel):
    """
    Attributes:
        created (Optional[int]):
        creator (Optional[str]):
        id (Optional[str]):
        is_archived (Optional[bool]):
        is_channel (Optional[bool]):
        is_ext_shared (Optional[bool]):
        is_general (Optional[bool]):
        is_group (Optional[bool]):
        is_im (Optional[bool]):
        is_member (Optional[bool]):
        is_mpim (Optional[bool]):
        is_org_shared (Optional[bool]):
        is_pending_ext_shared (Optional[bool]):
        is_private (Optional[bool]):
        is_read_only (Optional[bool]):
        is_shared (Optional[bool]):
        last_read (Optional[str]):
        name (Optional[str]):
        name_normalized (Optional[str]):
        pending_shared (Optional[list[str]]):
        previous_names (Optional[list[str]]):
        purpose (Optional[InviteToChannelResponsePurpose]):
        topic (Optional[InviteToChannelResponseTopic]):
        unlinked (Optional[int]):
        context_team_id (Optional[str]):  Example: T01G1P7CKR8.
        shared_team_ids (Optional[list[str]]):  Example: ['T01G1P7CKR8'].
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
    is_org_shared: Optional[bool] = None
    is_pending_ext_shared: Optional[bool] = None
    is_private: Optional[bool] = None
    is_read_only: Optional[bool] = None
    is_shared: Optional[bool] = None
    last_read: Optional[str] = None
    name: Optional[str] = None
    name_normalized: Optional[str] = None
    pending_shared: Optional[list[str]] = None
    previous_names: Optional[list[str]] = None
    purpose: Optional["InviteToChannelResponsePurpose"] = None
    topic: Optional["InviteToChannelResponseTopic"] = None
    unlinked: Optional[int] = None
    context_team_id: Optional[str] = None
    shared_team_ids: Optional[list[str]] = None

    def to_dict(self) -> Dict[str, Any]:
        return self.model_dump(exclude_none=True)

    @classmethod
    def from_dict(cls: Type["InviteToChannelResponse"], src_dict: Dict[str, Any]):
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
