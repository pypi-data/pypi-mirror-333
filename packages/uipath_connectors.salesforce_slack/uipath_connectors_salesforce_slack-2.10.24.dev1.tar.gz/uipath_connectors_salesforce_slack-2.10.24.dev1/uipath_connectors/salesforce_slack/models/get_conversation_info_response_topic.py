from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import Union


T = TypeVar("T", bound="GetConversationInfoResponseTopic")


@_attrs_define
class GetConversationInfoResponseTopic:
    """
    Attributes:
        creator (Union[Unset, str]):
        last_set (Union[Unset, int]):  Example: 0.0.
        value (Union[Unset, str]):
    """

    creator: Union[Unset, str] = UNSET
    last_set: Union[Unset, int] = UNSET
    value: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        creator = self.creator

        last_set = self.last_set

        value = self.value

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if creator is not UNSET:
            field_dict["creator"] = creator
        if last_set is not UNSET:
            field_dict["last_set"] = last_set
        if value is not UNSET:
            field_dict["value"] = value

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        creator = d.pop("creator", UNSET)

        last_set = d.pop("last_set", UNSET)

        value = d.pop("value", UNSET)

        get_conversation_info_response_topic = cls(
            creator=creator,
            last_set=last_set,
            value=value,
        )

        get_conversation_info_response_topic.additional_properties = d
        return get_conversation_info_response_topic

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
