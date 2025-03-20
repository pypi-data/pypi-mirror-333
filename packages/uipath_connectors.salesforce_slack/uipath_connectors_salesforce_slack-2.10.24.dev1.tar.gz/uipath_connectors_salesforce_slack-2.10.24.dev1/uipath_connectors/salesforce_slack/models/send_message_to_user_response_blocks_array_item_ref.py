from typing import Any, TypeVar, TYPE_CHECKING

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import Union

if TYPE_CHECKING:
    from ..models.send_message_to_user_response_blocks_text import (
        SendMessageToUserResponseBlocksText,
    )


T = TypeVar("T", bound="SendMessageToUserResponseBlocksArrayItemRef")


@_attrs_define
class SendMessageToUserResponseBlocksArrayItemRef:
    """
    Attributes:
        block_id (Union[Unset, str]):  Example: ZU=Pr.
        text (Union[Unset, SendMessageToUserResponseBlocksText]):
        type_ (Union[Unset, str]):  Example: section.
    """

    block_id: Union[Unset, str] = UNSET
    text: Union[Unset, "SendMessageToUserResponseBlocksText"] = UNSET
    type_: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:

        block_id = self.block_id

        text: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.text, Unset):
            text = self.text.to_dict()

        type_ = self.type_

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if block_id is not UNSET:
            field_dict["block_id"] = block_id
        if text is not UNSET:
            field_dict["text"] = text
        if type_ is not UNSET:
            field_dict["type"] = type_

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.send_message_to_user_response_blocks_text import (
            SendMessageToUserResponseBlocksText,
        )

        d = src_dict.copy()
        block_id = d.pop("block_id", UNSET)

        _text = d.pop("text", UNSET)
        text: Union[Unset, SendMessageToUserResponseBlocksText]
        if isinstance(_text, Unset):
            text = UNSET
        else:
            text = SendMessageToUserResponseBlocksText.from_dict(_text)

        type_ = d.pop("type", UNSET)

        send_message_to_user_response_blocks_array_item_ref = cls(
            block_id=block_id,
            text=text,
            type_=type_,
        )

        send_message_to_user_response_blocks_array_item_ref.additional_properties = d
        return send_message_to_user_response_blocks_array_item_ref

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
