from typing import Any, TypeVar, TYPE_CHECKING

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import Union

if TYPE_CHECKING:
    from ..models.send_reply_response_message_attachments_actions_array_item_ref import (
        SendReplyResponseMessageAttachmentsActionsArrayItemRef,
    )


T = TypeVar("T", bound="SendReplyResponseMessageAttachmentsArrayItemRef")


@_attrs_define
class SendReplyResponseMessageAttachmentsArrayItemRef:
    """
    Attributes:
        actions (Union[Unset, list['SendReplyResponseMessageAttachmentsActionsArrayItemRef']]):
        callback_id (Union[Unset, str]):  Example: wopr_game.
        color (Union[Unset, str]):  Example: 3AA3E3.
        fallback (Union[Unset, str]):  Example: You are unable to choose a game.
        id (Union[Unset, int]):  Example: 1.0.
        text (Union[Unset, str]):  Example: Choose a game to play.
    """

    actions: Union[
        Unset, list["SendReplyResponseMessageAttachmentsActionsArrayItemRef"]
    ] = UNSET
    callback_id: Union[Unset, str] = UNSET
    color: Union[Unset, str] = UNSET
    fallback: Union[Unset, str] = UNSET
    id: Union[Unset, int] = UNSET
    text: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:

        actions: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.actions, Unset):
            actions = []
            for componentsschemas_send_reply_response_message_attachments_actions_item_data in self.actions:
                componentsschemas_send_reply_response_message_attachments_actions_item = componentsschemas_send_reply_response_message_attachments_actions_item_data.to_dict()
                actions.append(
                    componentsschemas_send_reply_response_message_attachments_actions_item
                )

        callback_id = self.callback_id

        color = self.color

        fallback = self.fallback

        id = self.id

        text = self.text

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if actions is not UNSET:
            field_dict["actions"] = actions
        if callback_id is not UNSET:
            field_dict["callback_id"] = callback_id
        if color is not UNSET:
            field_dict["color"] = color
        if fallback is not UNSET:
            field_dict["fallback"] = fallback
        if id is not UNSET:
            field_dict["id"] = id
        if text is not UNSET:
            field_dict["text"] = text

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.send_reply_response_message_attachments_actions_array_item_ref import (
            SendReplyResponseMessageAttachmentsActionsArrayItemRef,
        )

        d = src_dict.copy()
        actions = []
        _actions = d.pop("actions", UNSET)
        for (
            componentsschemas_send_reply_response_message_attachments_actions_item_data
        ) in _actions or []:
            componentsschemas_send_reply_response_message_attachments_actions_item = SendReplyResponseMessageAttachmentsActionsArrayItemRef.from_dict(
                componentsschemas_send_reply_response_message_attachments_actions_item_data
            )

            actions.append(
                componentsschemas_send_reply_response_message_attachments_actions_item
            )

        callback_id = d.pop("callback_id", UNSET)

        color = d.pop("color", UNSET)

        fallback = d.pop("fallback", UNSET)

        id = d.pop("id", UNSET)

        text = d.pop("text", UNSET)

        send_reply_response_message_attachments_array_item_ref = cls(
            actions=actions,
            callback_id=callback_id,
            color=color,
            fallback=fallback,
            id=id,
            text=text,
        )

        send_reply_response_message_attachments_array_item_ref.additional_properties = d
        return send_reply_response_message_attachments_array_item_ref

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
