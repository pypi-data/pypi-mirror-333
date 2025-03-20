from typing import Any, Dict, Type, Optional
from pydantic import BaseModel, ConfigDict

from ..models.create_usergroup_response_prefs import CreateUsergroupResponsePrefs


class CreateUsergroupResponse(BaseModel):
    """
    Attributes:
        auto_type (Optional[str]):
        created_by (Optional[str]):  Example: U060RNRCZ.
        date_create (Optional[int]):  Example: 1.446746793E9.
        date_delete (Optional[int]):  Example: 0.0.
        date_update (Optional[int]):  Example: 1.446746793E9.
        deleted_by (Optional[str]):
        description (Optional[str]): A short description of the user group Example: Marketing gurus, PR experts and
            product advocates..
        handle (Optional[str]): A mention handle that is unique among channels, users and user groups. For example,
            @test_usergroup Example: marketing-team.
        id (Optional[str]): The unique id of the conversauser group. Example: S0615G0KT.
        is_external (Optional[bool]):
        is_usergroup (Optional[bool]):  Example: True.
        name (Optional[str]): A name for the user group. Must be unique among user groups Example: Marketing Team.
        prefs (Optional[CreateUsergroupResponsePrefs]):
        team_id (Optional[str]):  Example: T060RNRCH.
        updated_by (Optional[str]):  Example: U060RNRCZ.
        user_count (Optional[int]):  Example: 0.
    """

    model_config = ConfigDict(extra="allow")

    auto_type: Optional[str] = None
    created_by: Optional[str] = None
    date_create: Optional[int] = None
    date_delete: Optional[int] = None
    date_update: Optional[int] = None
    deleted_by: Optional[str] = None
    description: Optional[str] = None
    handle: Optional[str] = None
    id: Optional[str] = None
    is_external: Optional[bool] = None
    is_usergroup: Optional[bool] = None
    name: Optional[str] = None
    prefs: Optional["CreateUsergroupResponsePrefs"] = None
    team_id: Optional[str] = None
    updated_by: Optional[str] = None
    user_count: Optional[int] = None

    def to_dict(self) -> Dict[str, Any]:
        return self.model_dump(exclude_none=True)

    @classmethod
    def from_dict(cls: Type["CreateUsergroupResponse"], src_dict: Dict[str, Any]):
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
