from typing import Any, TypeVar, TYPE_CHECKING

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import Union

if TYPE_CHECKING:
    from ..models.add_users_to_usergroup_response_response_metadata import (
        AddUsersToUsergroupResponseResponseMetadata,
    )
    from ..models.add_users_to_usergroup_response_usergroup import (
        AddUsersToUsergroupResponseUsergroup,
    )


T = TypeVar("T", bound="AddUsersToUsergroupResponse")


@_attrs_define
class AddUsersToUsergroupResponse:
    """
    Attributes:
        ok (Union[Unset, bool]):  Example: True.
        response_metadata (Union[Unset, AddUsersToUsergroupResponseResponseMetadata]):
        usergroup (Union[Unset, AddUsersToUsergroupResponseUsergroup]):
        warning (Union[Unset, str]):  Example: missing_charset.
    """

    ok: Union[Unset, bool] = UNSET
    response_metadata: Union[Unset, "AddUsersToUsergroupResponseResponseMetadata"] = (
        UNSET
    )
    usergroup: Union[Unset, "AddUsersToUsergroupResponseUsergroup"] = UNSET
    warning: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:

        ok = self.ok

        response_metadata: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.response_metadata, Unset):
            response_metadata = self.response_metadata.to_dict()

        usergroup: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.usergroup, Unset):
            usergroup = self.usergroup.to_dict()

        warning = self.warning

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if ok is not UNSET:
            field_dict["ok"] = ok
        if response_metadata is not UNSET:
            field_dict["response_metadata"] = response_metadata
        if usergroup is not UNSET:
            field_dict["usergroup"] = usergroup
        if warning is not UNSET:
            field_dict["warning"] = warning

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.add_users_to_usergroup_response_response_metadata import (
            AddUsersToUsergroupResponseResponseMetadata,
        )
        from ..models.add_users_to_usergroup_response_usergroup import (
            AddUsersToUsergroupResponseUsergroup,
        )

        d = src_dict.copy()
        ok = d.pop("ok", UNSET)

        _response_metadata = d.pop("response_metadata", UNSET)
        response_metadata: Union[Unset, AddUsersToUsergroupResponseResponseMetadata]
        if isinstance(_response_metadata, Unset):
            response_metadata = UNSET
        else:
            response_metadata = AddUsersToUsergroupResponseResponseMetadata.from_dict(
                _response_metadata
            )

        _usergroup = d.pop("usergroup", UNSET)
        usergroup: Union[Unset, AddUsersToUsergroupResponseUsergroup]
        if isinstance(_usergroup, Unset):
            usergroup = UNSET
        else:
            usergroup = AddUsersToUsergroupResponseUsergroup.from_dict(_usergroup)

        warning = d.pop("warning", UNSET)

        add_users_to_usergroup_response = cls(
            ok=ok,
            response_metadata=response_metadata,
            usergroup=usergroup,
            warning=warning,
        )

        add_users_to_usergroup_response.additional_properties = d
        return add_users_to_usergroup_response

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
