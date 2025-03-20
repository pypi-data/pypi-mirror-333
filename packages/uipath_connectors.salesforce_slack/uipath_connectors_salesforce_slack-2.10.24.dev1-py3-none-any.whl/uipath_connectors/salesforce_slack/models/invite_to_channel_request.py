from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field



T = TypeVar("T", bound="InviteToChannelRequest")


@_attrs_define
class InviteToChannelRequest:
    """
    Attributes:
        users (str): User IDs Example: U02K95UU71Q,U04SVS31YMP.
        channel (str): Channel ID
    """

    users: str
    channel: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        users = self.users

        channel = self.channel

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "users": users,
                "channel": channel,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        users = d.pop("users")

        channel = d.pop("channel")

        invite_to_channel_request = cls(
            users=users,
            channel=channel,
        )

        invite_to_channel_request.additional_properties = d
        return invite_to_channel_request

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
