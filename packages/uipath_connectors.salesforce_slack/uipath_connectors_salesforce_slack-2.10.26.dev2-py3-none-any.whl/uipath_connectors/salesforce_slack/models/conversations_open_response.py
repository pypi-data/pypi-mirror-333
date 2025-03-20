from typing import Any, Dict, Type, Optional
from pydantic import BaseModel, ConfigDict


class ConversationsOpenResponse(BaseModel):
    """
    Attributes:
        created (Optional[int]):  Example: 1.460147748E9.
        id (Optional[str]):  Example: D069C7QFK.
        is_im (Optional[bool]):  Example: True.
        is_open (Optional[bool]):  Example: True.
        is_org_shared (Optional[bool]):
        last_read (Optional[str]):  Example: 0000000000.000000.
        latest (Optional[str]):
        priority (Optional[int]):  Example: 0.0.
        unread_count (Optional[int]):  Example: 0.0.
        unread_count_display (Optional[int]):  Example: 0.0.
        user (Optional[str]):  Example: U069C7QF3.
    """

    model_config = ConfigDict(extra="allow")

    created: Optional[int] = None
    id: Optional[str] = None
    is_im: Optional[bool] = None
    is_open: Optional[bool] = None
    is_org_shared: Optional[bool] = None
    last_read: Optional[str] = None
    latest: Optional[str] = None
    priority: Optional[int] = None
    unread_count: Optional[int] = None
    unread_count_display: Optional[int] = None
    user: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return self.model_dump(exclude_none=True)

    @classmethod
    def from_dict(cls: Type["ConversationsOpenResponse"], src_dict: Dict[str, Any]):
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
