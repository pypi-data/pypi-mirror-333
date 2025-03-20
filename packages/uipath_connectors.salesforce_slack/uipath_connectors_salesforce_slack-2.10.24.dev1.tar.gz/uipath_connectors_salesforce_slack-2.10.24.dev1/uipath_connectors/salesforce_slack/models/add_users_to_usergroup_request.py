from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import cast
from typing import Union


T = TypeVar("T", bound="AddUsersToUsergroupRequest")


@_attrs_define
class AddUsersToUsergroupRequest:
    """
    Attributes:
        usergroup_id (str): User group ID Example: string.
        include_count (Union[Unset, bool]):  Example: True.
        users (Union[Unset, list[str]]):  Example: ['string'].
    """

    usergroup_id: str
    include_count: Union[Unset, bool] = UNSET
    users: Union[Unset, list[str]] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        usergroup_id = self.usergroup_id

        include_count = self.include_count

        users: Union[Unset, list[str]] = UNSET
        if not isinstance(self.users, Unset):
            users = self.users

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "usergroupId": usergroup_id,
            }
        )
        if include_count is not UNSET:
            field_dict["include_count"] = include_count
        if users is not UNSET:
            field_dict["users"] = users

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        usergroup_id = d.pop("usergroupId")

        include_count = d.pop("include_count", UNSET)

        users = cast(list[str], d.pop("users", UNSET))

        add_users_to_usergroup_request = cls(
            usergroup_id=usergroup_id,
            include_count=include_count,
            users=users,
        )

        add_users_to_usergroup_request.additional_properties = d
        return add_users_to_usergroup_request

    @property
    def additional_keys(self) -> list[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
