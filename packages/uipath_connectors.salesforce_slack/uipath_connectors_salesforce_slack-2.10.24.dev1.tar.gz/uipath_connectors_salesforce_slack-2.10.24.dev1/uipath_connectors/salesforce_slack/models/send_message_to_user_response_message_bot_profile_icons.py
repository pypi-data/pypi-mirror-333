from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import Union


T = TypeVar("T", bound="SendMessageToUserResponseMessageBotProfileIcons")


@_attrs_define
class SendMessageToUserResponseMessageBotProfileIcons:
    """
    Attributes:
        image_36 (Union[Unset, str]):  Example: https://a.slack-edge.com/80588/img/plugins/app/bot_36.png.
        image_48 (Union[Unset, str]):  Example: https://a.slack-edge.com/80588/img/plugins/app/bot_48.png.
        image_72 (Union[Unset, str]):  Example: https://a.slack-edge.com/80588/img/plugins/app/service_72.png.
    """

    image_36: Union[Unset, str] = UNSET
    image_48: Union[Unset, str] = UNSET
    image_72: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        image_36 = self.image_36

        image_48 = self.image_48

        image_72 = self.image_72

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if image_36 is not UNSET:
            field_dict["image_36"] = image_36
        if image_48 is not UNSET:
            field_dict["image_48"] = image_48
        if image_72 is not UNSET:
            field_dict["image_72"] = image_72

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        image_36 = d.pop("image_36", UNSET)

        image_48 = d.pop("image_48", UNSET)

        image_72 = d.pop("image_72", UNSET)

        send_message_to_user_response_message_bot_profile_icons = cls(
            image_36=image_36,
            image_48=image_48,
            image_72=image_72,
        )

        send_message_to_user_response_message_bot_profile_icons.additional_properties = d
        return send_message_to_user_response_message_bot_profile_icons

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
