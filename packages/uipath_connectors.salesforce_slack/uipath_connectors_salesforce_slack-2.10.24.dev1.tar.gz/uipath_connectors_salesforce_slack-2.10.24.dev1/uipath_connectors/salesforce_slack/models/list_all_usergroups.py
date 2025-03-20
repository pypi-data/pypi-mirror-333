from typing import Any, TypeVar, TYPE_CHECKING

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import Union

if TYPE_CHECKING:
    from ..models.list_all_usergroups_usergroups_array_item_ref import (
        ListAllUsergroupsUsergroupsArrayItemRef,
    )


T = TypeVar("T", bound="ListAllUsergroups")


@_attrs_define
class ListAllUsergroups:
    """
    Attributes:
        ok (Union[Unset, bool]):
        usergroups (Union[Unset, list['ListAllUsergroupsUsergroupsArrayItemRef']]):
    """

    ok: Union[Unset, bool] = UNSET
    usergroups: Union[Unset, list["ListAllUsergroupsUsergroupsArrayItemRef"]] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:

        ok = self.ok

        usergroups: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.usergroups, Unset):
            usergroups = []
            for (
                componentsschemas_list_all_usergroups_usergroups_item_data
            ) in self.usergroups:
                componentsschemas_list_all_usergroups_usergroups_item = (
                    componentsschemas_list_all_usergroups_usergroups_item_data.to_dict()
                )
                usergroups.append(componentsschemas_list_all_usergroups_usergroups_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if ok is not UNSET:
            field_dict["ok"] = ok
        if usergroups is not UNSET:
            field_dict["usergroups"] = usergroups

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.list_all_usergroups_usergroups_array_item_ref import (
            ListAllUsergroupsUsergroupsArrayItemRef,
        )

        d = src_dict.copy()
        ok = d.pop("ok", UNSET)

        usergroups = []
        _usergroups = d.pop("usergroups", UNSET)
        for componentsschemas_list_all_usergroups_usergroups_item_data in (
            _usergroups or []
        ):
            componentsschemas_list_all_usergroups_usergroups_item = (
                ListAllUsergroupsUsergroupsArrayItemRef.from_dict(
                    componentsschemas_list_all_usergroups_usergroups_item_data
                )
            )

            usergroups.append(componentsschemas_list_all_usergroups_usergroups_item)

        list_all_usergroups = cls(
            ok=ok,
            usergroups=usergroups,
        )

        list_all_usergroups.additional_properties = d
        return list_all_usergroups

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
