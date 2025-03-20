from typing import Any, Dict, Type, Optional
from pydantic import BaseModel, ConfigDict

from ..models.add_users_to_usergroup_response_usergroup_prefs import (
    AddUsersToUsergroupResponseUsergroupPrefs,
)


class AddUsersToUsergroupResponseUsergroup(BaseModel):
    """
    Attributes:
        auto_provision (Optional[bool]):
        channel_count (Optional[int]):  Example: 0.0.
        created_by (Optional[str]):  Example: U02K95UU71Q.
        date_create (Optional[int]):  Example: 1.676803736E9.
        date_delete (Optional[int]):  Example: 0.0.
        date_update (Optional[int]):  Example: 1.683785723E9.
        description (Optional[str]):  Example: testing.
        enterprise_subteam_id (Optional[str]):
        handle (Optional[str]):  Example: update-test-team-29468.
        id (Optional[str]):  Example: S04Q3GYSMJS.
        is_external (Optional[bool]):
        is_subteam (Optional[bool]):  Example: True.
        is_usergroup (Optional[bool]):  Example: True.
        name (Optional[str]):  Example: Alpha Test Team 23840.
        prefs (Optional[AddUsersToUsergroupResponseUsergroupPrefs]):
        team_id (Optional[str]):  Example: T02KZCJHY1W.
        updated_by (Optional[str]):  Example: U02K95UU71Q.
        user_count (Optional[int]):  Example: 3.0.
        users (Optional[list[str]]):  Example: ['U02K95UU71Q', 'U04Q3GTCF7G', 'U04QA5052EN'].
    """

    model_config = ConfigDict(extra="allow")

    auto_provision: Optional[bool] = None
    channel_count: Optional[int] = None
    created_by: Optional[str] = None
    date_create: Optional[int] = None
    date_delete: Optional[int] = None
    date_update: Optional[int] = None
    description: Optional[str] = None
    enterprise_subteam_id: Optional[str] = None
    handle: Optional[str] = None
    id: Optional[str] = None
    is_external: Optional[bool] = None
    is_subteam: Optional[bool] = None
    is_usergroup: Optional[bool] = None
    name: Optional[str] = None
    prefs: Optional["AddUsersToUsergroupResponseUsergroupPrefs"] = None
    team_id: Optional[str] = None
    updated_by: Optional[str] = None
    user_count: Optional[int] = None
    users: Optional[list[str]] = None

    def to_dict(self) -> Dict[str, Any]:
        return self.model_dump(exclude_none=True)

    @classmethod
    def from_dict(
        cls: Type["AddUsersToUsergroupResponseUsergroup"], src_dict: Dict[str, Any]
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
