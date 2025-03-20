from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import Union


T = TypeVar("T", bound="SetChannelTopicResponseLatest")


@_attrs_define
class SetChannelTopicResponseLatest:
    """
    Attributes:
        subtype (Union[Unset, str]):  Example: channel_topic.
        text (Union[Unset, str]):  Example: set the channel topic: Apply topically for best effects.
        topic (Union[Unset, str]):  Example: Apply topically for best effects.
        ts (Union[Unset, str]):  Example: 1649952691.429799.
        type_ (Union[Unset, str]):  Example: message.
        user (Union[Unset, str]):  Example: U12345678.
    """

    subtype: Union[Unset, str] = UNSET
    text: Union[Unset, str] = UNSET
    topic: Union[Unset, str] = UNSET
    ts: Union[Unset, str] = UNSET
    type_: Union[Unset, str] = UNSET
    user: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        subtype = self.subtype

        text = self.text

        topic = self.topic

        ts = self.ts

        type_ = self.type_

        user = self.user

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if subtype is not UNSET:
            field_dict["subtype"] = subtype
        if text is not UNSET:
            field_dict["text"] = text
        if topic is not UNSET:
            field_dict["topic"] = topic
        if ts is not UNSET:
            field_dict["ts"] = ts
        if type_ is not UNSET:
            field_dict["type"] = type_
        if user is not UNSET:
            field_dict["user"] = user

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        subtype = d.pop("subtype", UNSET)

        text = d.pop("text", UNSET)

        topic = d.pop("topic", UNSET)

        ts = d.pop("ts", UNSET)

        type_ = d.pop("type", UNSET)

        user = d.pop("user", UNSET)

        set_channel_topic_response_latest = cls(
            subtype=subtype,
            text=text,
            topic=topic,
            ts=ts,
            type_=type_,
            user=user,
        )

        set_channel_topic_response_latest.additional_properties = d
        return set_channel_topic_response_latest

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
