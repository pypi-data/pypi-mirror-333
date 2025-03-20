from typing import Any, TypeVar, TYPE_CHECKING

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import Union

if TYPE_CHECKING:
    from ..models.send_message_to_user_request_attachments_actions_array_item_ref import (
        SendMessageToUserRequestAttachmentsActionsArrayItemRef,
    )


T = TypeVar("T", bound="SendMessageToUserRequestAttachmentsArrayItemRef")


@_attrs_define
class SendMessageToUserRequestAttachmentsArrayItemRef:
    """
    Attributes:
        actions (Union[Unset, list['SendMessageToUserRequestAttachmentsActionsArrayItemRef']]):
        attachment_type (Union[Unset, str]):  Example: default.
        callback_id (Union[Unset, str]):  Example: wopr_game.
        color (Union[Unset, str]):  Example: #3AA3E3.
        fallback (Union[Unset, str]):  Example: You are unable to choose a game.
        text (Union[Unset, str]):  Example: Choose a game to play.
    """

    actions: Union[
        Unset, list["SendMessageToUserRequestAttachmentsActionsArrayItemRef"]
    ] = UNSET
    attachment_type: Union[Unset, str] = UNSET
    callback_id: Union[Unset, str] = UNSET
    color: Union[Unset, str] = UNSET
    fallback: Union[Unset, str] = UNSET
    text: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:

        actions: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.actions, Unset):
            actions = []
            for componentsschemas_send_message_to_user_request_attachments_actions_item_data in self.actions:
                componentsschemas_send_message_to_user_request_attachments_actions_item = componentsschemas_send_message_to_user_request_attachments_actions_item_data.to_dict()
                actions.append(
                    componentsschemas_send_message_to_user_request_attachments_actions_item
                )

        attachment_type = self.attachment_type

        callback_id = self.callback_id

        color = self.color

        fallback = self.fallback

        text = self.text

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if actions is not UNSET:
            field_dict["actions"] = actions
        if attachment_type is not UNSET:
            field_dict["attachment_type"] = attachment_type
        if callback_id is not UNSET:
            field_dict["callback_id"] = callback_id
        if color is not UNSET:
            field_dict["color"] = color
        if fallback is not UNSET:
            field_dict["fallback"] = fallback
        if text is not UNSET:
            field_dict["text"] = text

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.send_message_to_user_request_attachments_actions_array_item_ref import (
            SendMessageToUserRequestAttachmentsActionsArrayItemRef,
        )

        d = src_dict.copy()
        actions = []
        _actions = d.pop("actions", UNSET)
        for (
            componentsschemas_send_message_to_user_request_attachments_actions_item_data
        ) in _actions or []:
            componentsschemas_send_message_to_user_request_attachments_actions_item = SendMessageToUserRequestAttachmentsActionsArrayItemRef.from_dict(
                componentsschemas_send_message_to_user_request_attachments_actions_item_data
            )

            actions.append(
                componentsschemas_send_message_to_user_request_attachments_actions_item
            )

        attachment_type = d.pop("attachment_type", UNSET)

        callback_id = d.pop("callback_id", UNSET)

        color = d.pop("color", UNSET)

        fallback = d.pop("fallback", UNSET)

        text = d.pop("text", UNSET)

        send_message_to_user_request_attachments_array_item_ref = cls(
            actions=actions,
            attachment_type=attachment_type,
            callback_id=callback_id,
            color=color,
            fallback=fallback,
            text=text,
        )

        send_message_to_user_request_attachments_array_item_ref.additional_properties = d
        return send_message_to_user_request_attachments_array_item_ref

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
