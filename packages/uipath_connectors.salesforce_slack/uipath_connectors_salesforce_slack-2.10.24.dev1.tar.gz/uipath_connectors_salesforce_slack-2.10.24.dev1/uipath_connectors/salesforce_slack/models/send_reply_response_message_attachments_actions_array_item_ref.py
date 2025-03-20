from typing import Any, TypeVar, TYPE_CHECKING

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import Union

if TYPE_CHECKING:
    from ..models.send_reply_response_message_attachments_actions_confirm import (
        SendReplyResponseMessageAttachmentsActionsConfirm,
    )


T = TypeVar("T", bound="SendReplyResponseMessageAttachmentsActionsArrayItemRef")


@_attrs_define
class SendReplyResponseMessageAttachmentsActionsArrayItemRef:
    """
    Attributes:
        confirm (Union[Unset, SendReplyResponseMessageAttachmentsActionsConfirm]):
        id (Union[Unset, str]):  Example: 1.
        name (Union[Unset, str]):  Example: game.
        style (Union[Unset, str]):
        text (Union[Unset, str]):  Example: Chess.
        type_ (Union[Unset, str]):  Example: button.
        value (Union[Unset, str]):  Example: chess.
    """

    confirm: Union[Unset, "SendReplyResponseMessageAttachmentsActionsConfirm"] = UNSET
    id: Union[Unset, str] = UNSET
    name: Union[Unset, str] = UNSET
    style: Union[Unset, str] = UNSET
    text: Union[Unset, str] = UNSET
    type_: Union[Unset, str] = UNSET
    value: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:

        confirm: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.confirm, Unset):
            confirm = self.confirm.to_dict()

        id = self.id

        name = self.name

        style = self.style

        text = self.text

        type_ = self.type_

        value = self.value

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if confirm is not UNSET:
            field_dict["confirm"] = confirm
        if id is not UNSET:
            field_dict["id"] = id
        if name is not UNSET:
            field_dict["name"] = name
        if style is not UNSET:
            field_dict["style"] = style
        if text is not UNSET:
            field_dict["text"] = text
        if type_ is not UNSET:
            field_dict["type"] = type_
        if value is not UNSET:
            field_dict["value"] = value

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.send_reply_response_message_attachments_actions_confirm import (
            SendReplyResponseMessageAttachmentsActionsConfirm,
        )

        d = src_dict.copy()
        _confirm = d.pop("confirm", UNSET)
        confirm: Union[Unset, SendReplyResponseMessageAttachmentsActionsConfirm]
        if isinstance(_confirm, Unset):
            confirm = UNSET
        else:
            confirm = SendReplyResponseMessageAttachmentsActionsConfirm.from_dict(
                _confirm
            )

        id = d.pop("id", UNSET)

        name = d.pop("name", UNSET)

        style = d.pop("style", UNSET)

        text = d.pop("text", UNSET)

        type_ = d.pop("type", UNSET)

        value = d.pop("value", UNSET)

        send_reply_response_message_attachments_actions_array_item_ref = cls(
            confirm=confirm,
            id=id,
            name=name,
            style=style,
            text=text,
            type_=type_,
            value=value,
        )

        send_reply_response_message_attachments_actions_array_item_ref.additional_properties = d
        return send_reply_response_message_attachments_actions_array_item_ref

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
