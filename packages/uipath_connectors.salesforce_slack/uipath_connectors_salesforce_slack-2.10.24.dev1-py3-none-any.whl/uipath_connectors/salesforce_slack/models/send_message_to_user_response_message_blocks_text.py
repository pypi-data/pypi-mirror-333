from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import Union


T = TypeVar("T", bound="SendMessageToUserResponseMessageBlocksText")


@_attrs_define
class SendMessageToUserResponseMessageBlocksText:
    """
    Attributes:
        emoji (Union[Unset, bool]):  Example: True.
        text (Union[Unset, str]):  Example: Hello world.
        type_ (Union[Unset, str]):  Example: plain_text.
    """

    emoji: Union[Unset, bool] = UNSET
    text: Union[Unset, str] = UNSET
    type_: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        emoji = self.emoji

        text = self.text

        type_ = self.type_

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if emoji is not UNSET:
            field_dict["emoji"] = emoji
        if text is not UNSET:
            field_dict["text"] = text
        if type_ is not UNSET:
            field_dict["type"] = type_

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        emoji = d.pop("emoji", UNSET)

        text = d.pop("text", UNSET)

        type_ = d.pop("type", UNSET)

        send_message_to_user_response_message_blocks_text = cls(
            emoji=emoji,
            text=text,
            type_=type_,
        )

        send_message_to_user_response_message_blocks_text.additional_properties = d
        return send_message_to_user_response_message_blocks_text

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
