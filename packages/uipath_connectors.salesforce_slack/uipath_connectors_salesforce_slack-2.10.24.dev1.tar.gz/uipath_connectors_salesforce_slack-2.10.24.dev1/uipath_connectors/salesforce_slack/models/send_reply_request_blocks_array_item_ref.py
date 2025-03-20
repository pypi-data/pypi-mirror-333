from typing import Any, TypeVar, TYPE_CHECKING

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import Union

if TYPE_CHECKING:
    from ..models.send_reply_request_blocks_text import SendReplyRequestBlocksText


T = TypeVar("T", bound="SendReplyRequestBlocksArrayItemRef")


@_attrs_define
class SendReplyRequestBlocksArrayItemRef:
    """
    Attributes:
        text (Union[Unset, SendReplyRequestBlocksText]):
        type_ (Union[Unset, str]):  Example: section.
    """

    text: Union[Unset, "SendReplyRequestBlocksText"] = UNSET
    type_: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:

        text: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.text, Unset):
            text = self.text.to_dict()

        type_ = self.type_

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if text is not UNSET:
            field_dict["text"] = text
        if type_ is not UNSET:
            field_dict["type"] = type_

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.send_reply_request_blocks_text import SendReplyRequestBlocksText

        d = src_dict.copy()
        _text = d.pop("text", UNSET)
        text: Union[Unset, SendReplyRequestBlocksText]
        if isinstance(_text, Unset):
            text = UNSET
        else:
            text = SendReplyRequestBlocksText.from_dict(_text)

        type_ = d.pop("type", UNSET)

        send_reply_request_blocks_array_item_ref = cls(
            text=text,
            type_=type_,
        )

        send_reply_request_blocks_array_item_ref.additional_properties = d
        return send_reply_request_blocks_array_item_ref

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
