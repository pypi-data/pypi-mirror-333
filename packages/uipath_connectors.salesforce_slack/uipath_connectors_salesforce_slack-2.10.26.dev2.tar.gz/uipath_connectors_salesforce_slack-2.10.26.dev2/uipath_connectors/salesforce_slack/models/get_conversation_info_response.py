from typing import Any, Dict, Type, Optional
from pydantic import BaseModel, ConfigDict

from ..models.get_conversation_info_response_topic import (
    GetConversationInfoResponseTopic,
)
from ..models.get_conversation_info_response_purpose import (
    GetConversationInfoResponsePurpose,
)


class GetConversationInfoResponse(BaseModel):
    """
    Attributes:
        created (Optional[int]):  Example: 1.629792267E9.
        creator (Optional[str]):  Example: UCUFVVCKS.
        id (Optional[str]):  Example: C02C4TL46CT.
        is_archived (Optional[bool]):
        is_channel (Optional[bool]):  Example: True.
        is_ext_shared (Optional[bool]):
        is_general (Optional[bool]):
        is_group (Optional[bool]):
        is_im (Optional[bool]):
        is_member (Optional[bool]):  Example: True.
        is_mpim (Optional[bool]):
        is_org_shared (Optional[bool]):
        is_pending_ext_shared (Optional[bool]):
        is_private (Optional[bool]):
        is_shared (Optional[bool]):
        last_read (Optional[str]):  Example: 1631093304.000300.
        locale (Optional[str]):  Example: en-US.
        name (Optional[str]):  Example: periodic-test-3.
        name_normalized (Optional[str]):  Example: periodic-test-3.
        num_members (Optional[int]):  Example: 1.0.
        purpose (Optional[GetConversationInfoResponsePurpose]):
        shared_team_ids (Optional[list[str]]):  Example: ['TCU0VUNLT'].
        topic (Optional[GetConversationInfoResponseTopic]):
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
    is_org_shared: Optional[bool] = None
    is_pending_ext_shared: Optional[bool] = None
    is_private: Optional[bool] = None
    is_shared: Optional[bool] = None
    last_read: Optional[str] = None
    locale: Optional[str] = None
    name: Optional[str] = None
    name_normalized: Optional[str] = None
    num_members: Optional[int] = None
    purpose: Optional["GetConversationInfoResponsePurpose"] = None
    shared_team_ids: Optional[list[str]] = None
    topic: Optional["GetConversationInfoResponseTopic"] = None
    unlinked: Optional[int] = None

    def to_dict(self) -> Dict[str, Any]:
        return self.model_dump(exclude_none=True)

    @classmethod
    def from_dict(cls: Type["GetConversationInfoResponse"], src_dict: Dict[str, Any]):
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
