from typing import Any, Dict, Type, Optional
from pydantic import BaseModel, ConfigDict

from ..models.list_all_users_profile import ListAllUsersProfile


class ListAllUsers(BaseModel):
    """
    Attributes:
        color (Optional[str]):  Example: 9f69e7.
        deleted (Optional[bool]):
        has_2fa (Optional[bool]):
        id (Optional[str]):  Example: W012A3CDE.
        is_admin (Optional[bool]):  Example: True.
        is_app_user (Optional[bool]):
        is_bot (Optional[bool]):
        is_owner (Optional[bool]):
        is_primary_owner (Optional[bool]):
        is_restricted (Optional[bool]):
        is_ultra_restricted (Optional[bool]):
        name (Optional[str]):  Example: spengler.
        profile (Optional[ListAllUsersProfile]):
        real_name (Optional[str]):  Example: spengler.
        team_id (Optional[str]):  Example: T012AB3C4.
        tz (Optional[str]):  Example: America/Los_Angeles.
        tz_label (Optional[str]):  Example: Pacific Daylight Time.
        tz_offset (Optional[int]):  Example: -25200.0.
        updated (Optional[int]):  Example: 1.502138686E9.
    """

    model_config = ConfigDict(extra="allow")

    color: Optional[str] = None
    deleted: Optional[bool] = None
    has_2fa: Optional[bool] = None
    id: Optional[str] = None
    is_admin: Optional[bool] = None
    is_app_user: Optional[bool] = None
    is_bot: Optional[bool] = None
    is_owner: Optional[bool] = None
    is_primary_owner: Optional[bool] = None
    is_restricted: Optional[bool] = None
    is_ultra_restricted: Optional[bool] = None
    name: Optional[str] = None
    profile: Optional["ListAllUsersProfile"] = None
    real_name: Optional[str] = None
    team_id: Optional[str] = None
    tz: Optional[str] = None
    tz_label: Optional[str] = None
    tz_offset: Optional[int] = None
    updated: Optional[int] = None

    def to_dict(self) -> Dict[str, Any]:
        return self.model_dump(exclude_none=True)

    @classmethod
    def from_dict(cls: Type["ListAllUsers"], src_dict: Dict[str, Any]):
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
