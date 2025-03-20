from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import Union


T = TypeVar("T", bound="SendMessageRequestAttachmentsActionsConfirm")


@_attrs_define
class SendMessageRequestAttachmentsActionsConfirm:
    """
    Attributes:
        dismiss_text (Union[Unset, str]):  Example: No.
        ok_text (Union[Unset, str]):  Example: Yes.
        text (Union[Unset, str]):  Example: Wouldn't you prefer a good game of chess?.
        title (Union[Unset, str]):  Example: Are you sure?.
    """

    dismiss_text: Union[Unset, str] = UNSET
    ok_text: Union[Unset, str] = UNSET
    text: Union[Unset, str] = UNSET
    title: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        dismiss_text = self.dismiss_text

        ok_text = self.ok_text

        text = self.text

        title = self.title

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if dismiss_text is not UNSET:
            field_dict["dismiss_text"] = dismiss_text
        if ok_text is not UNSET:
            field_dict["ok_text"] = ok_text
        if text is not UNSET:
            field_dict["text"] = text
        if title is not UNSET:
            field_dict["title"] = title

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        dismiss_text = d.pop("dismiss_text", UNSET)

        ok_text = d.pop("ok_text", UNSET)

        text = d.pop("text", UNSET)

        title = d.pop("title", UNSET)

        send_message_request_attachments_actions_confirm = cls(
            dismiss_text=dismiss_text,
            ok_text=ok_text,
            text=text,
            title=title,
        )

        send_message_request_attachments_actions_confirm.additional_properties = d
        return send_message_request_attachments_actions_confirm

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
