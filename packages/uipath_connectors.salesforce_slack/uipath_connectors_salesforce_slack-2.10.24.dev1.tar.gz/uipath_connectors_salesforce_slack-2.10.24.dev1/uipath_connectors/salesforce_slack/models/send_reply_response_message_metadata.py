from typing import Any, TypeVar, TYPE_CHECKING

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import Union

if TYPE_CHECKING:
    from ..models.send_reply_response_message_metadata_event_payload import (
        SendReplyResponseMessageMetadataEventPayload,
    )


T = TypeVar("T", bound="SendReplyResponseMessageMetadata")


@_attrs_define
class SendReplyResponseMessageMetadata:
    """
    Attributes:
        event_payload (Union[Unset, SendReplyResponseMessageMetadataEventPayload]):
        event_type (Union[Unset, str]):  Example: task_created.
    """

    event_payload: Union[Unset, "SendReplyResponseMessageMetadataEventPayload"] = UNSET
    event_type: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:

        event_payload: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.event_payload, Unset):
            event_payload = self.event_payload.to_dict()

        event_type = self.event_type

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if event_payload is not UNSET:
            field_dict["event_payload"] = event_payload
        if event_type is not UNSET:
            field_dict["event_type"] = event_type

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.send_reply_response_message_metadata_event_payload import (
            SendReplyResponseMessageMetadataEventPayload,
        )

        d = src_dict.copy()
        _event_payload = d.pop("event_payload", UNSET)
        event_payload: Union[Unset, SendReplyResponseMessageMetadataEventPayload]
        if isinstance(_event_payload, Unset):
            event_payload = UNSET
        else:
            event_payload = SendReplyResponseMessageMetadataEventPayload.from_dict(
                _event_payload
            )

        event_type = d.pop("event_type", UNSET)

        send_reply_response_message_metadata = cls(
            event_payload=event_payload,
            event_type=event_type,
        )

        send_reply_response_message_metadata.additional_properties = d
        return send_reply_response_message_metadata

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
