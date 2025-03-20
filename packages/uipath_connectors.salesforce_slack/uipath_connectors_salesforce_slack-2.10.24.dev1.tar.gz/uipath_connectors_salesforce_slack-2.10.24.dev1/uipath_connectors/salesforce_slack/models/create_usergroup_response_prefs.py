from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import cast
from typing import Union


T = TypeVar("T", bound="CreateUsergroupResponsePrefs")


@_attrs_define
class CreateUsergroupResponsePrefs:
    """
    Attributes:
        channels (Union[Unset, list[str]]):
        groups (Union[Unset, list[str]]):
    """

    channels: Union[Unset, list[str]] = UNSET
    groups: Union[Unset, list[str]] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        channels: Union[Unset, list[str]] = UNSET
        if not isinstance(self.channels, Unset):
            channels = self.channels

        groups: Union[Unset, list[str]] = UNSET
        if not isinstance(self.groups, Unset):
            groups = self.groups

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if channels is not UNSET:
            field_dict["channels"] = channels
        if groups is not UNSET:
            field_dict["groups"] = groups

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        channels = cast(list[str], d.pop("channels", UNSET))

        groups = cast(list[str], d.pop("groups", UNSET))

        create_usergroup_response_prefs = cls(
            channels=channels,
            groups=groups,
        )

        create_usergroup_response_prefs.additional_properties = d
        return create_usergroup_response_prefs

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
