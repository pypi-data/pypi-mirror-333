from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field



T = TypeVar("T", bound="ConversationsJoinRequest")


@_attrs_define
class ConversationsJoinRequest:
    """
    Attributes:
        channel (str): Public channel ID
    """

    channel: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        channel = self.channel

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "channel": channel,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        channel = d.pop("channel")

        conversations_join_request = cls(
            channel=channel,
        )

        conversations_join_request.additional_properties = d
        return conversations_join_request

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
