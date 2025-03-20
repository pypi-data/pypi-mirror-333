from typing import Any, TypeVar, TYPE_CHECKING

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import cast
from typing import Union

if TYPE_CHECKING:
    from ..models.create_channel_response_purpose import CreateChannelResponsePurpose
    from ..models.create_channel_response_topic import CreateChannelResponseTopic


T = TypeVar("T", bound="CreateChannelResponse")


@_attrs_define
class CreateChannelResponse:
    """
    Attributes:
        created (Union[Unset, int]):  Example: 1.536962679E9.
        creator (Union[Unset, str]):  Example: UCTGFDTEV.
        id (Union[Unset, str]): The ID of the channel Example: CCU0VUWKD.
        is_archived (Union[Unset, bool]):  Example: True.
        is_channel (Union[Unset, bool]):  Example: True.
        is_ext_shared (Union[Unset, bool]):
        is_general (Union[Unset, bool]):
        is_group (Union[Unset, bool]):
        is_im (Union[Unset, bool]):
        is_member (Union[Unset, bool]):
        is_mpim (Union[Unset, bool]):
        is_open (Union[Unset, bool]):  Example: True.
        is_org_shared (Union[Unset, bool]):
        is_pending_ext_shared (Union[Unset, bool]):
        is_private (Union[Unset, bool]): Whether the channel is private or not? Default is false
        is_shared (Union[Unset, bool]):
        last_read (Union[Unset, str]):  Example: 0000000000.000000.
        name (Union[Unset, str]): The name of the channel to create Example: random.
        name_normalized (Union[Unset, str]):  Example: random.
        priority (Union[Unset, int]):  Example: 0.0.
        purpose (Union[Unset, CreateChannelResponsePurpose]):
        shared_team_ids (Union[Unset, list[str]]):  Example: ['TCU0VUNLT'].
        topic (Union[Unset, CreateChannelResponseTopic]):
        unlinked (Union[Unset, int]):  Example: 0.0.
    """

    created: Union[Unset, int] = UNSET
    creator: Union[Unset, str] = UNSET
    id: Union[Unset, str] = UNSET
    is_archived: Union[Unset, bool] = UNSET
    is_channel: Union[Unset, bool] = UNSET
    is_ext_shared: Union[Unset, bool] = UNSET
    is_general: Union[Unset, bool] = UNSET
    is_group: Union[Unset, bool] = UNSET
    is_im: Union[Unset, bool] = UNSET
    is_member: Union[Unset, bool] = UNSET
    is_mpim: Union[Unset, bool] = UNSET
    is_open: Union[Unset, bool] = UNSET
    is_org_shared: Union[Unset, bool] = UNSET
    is_pending_ext_shared: Union[Unset, bool] = UNSET
    is_private: Union[Unset, bool] = UNSET
    is_shared: Union[Unset, bool] = UNSET
    last_read: Union[Unset, str] = UNSET
    name: Union[Unset, str] = UNSET
    name_normalized: Union[Unset, str] = UNSET
    priority: Union[Unset, int] = UNSET
    purpose: Union[Unset, "CreateChannelResponsePurpose"] = UNSET
    shared_team_ids: Union[Unset, list[str]] = UNSET
    topic: Union[Unset, "CreateChannelResponseTopic"] = UNSET
    unlinked: Union[Unset, int] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:

        created = self.created

        creator = self.creator

        id = self.id

        is_archived = self.is_archived

        is_channel = self.is_channel

        is_ext_shared = self.is_ext_shared

        is_general = self.is_general

        is_group = self.is_group

        is_im = self.is_im

        is_member = self.is_member

        is_mpim = self.is_mpim

        is_open = self.is_open

        is_org_shared = self.is_org_shared

        is_pending_ext_shared = self.is_pending_ext_shared

        is_private = self.is_private

        is_shared = self.is_shared

        last_read = self.last_read

        name = self.name

        name_normalized = self.name_normalized

        priority = self.priority

        purpose: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.purpose, Unset):
            purpose = self.purpose.to_dict()

        shared_team_ids: Union[Unset, list[str]] = UNSET
        if not isinstance(self.shared_team_ids, Unset):
            shared_team_ids = self.shared_team_ids

        topic: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.topic, Unset):
            topic = self.topic.to_dict()

        unlinked = self.unlinked

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if created is not UNSET:
            field_dict["created"] = created
        if creator is not UNSET:
            field_dict["creator"] = creator
        if id is not UNSET:
            field_dict["id"] = id
        if is_archived is not UNSET:
            field_dict["is_archived"] = is_archived
        if is_channel is not UNSET:
            field_dict["is_channel"] = is_channel
        if is_ext_shared is not UNSET:
            field_dict["is_ext_shared"] = is_ext_shared
        if is_general is not UNSET:
            field_dict["is_general"] = is_general
        if is_group is not UNSET:
            field_dict["is_group"] = is_group
        if is_im is not UNSET:
            field_dict["is_im"] = is_im
        if is_member is not UNSET:
            field_dict["is_member"] = is_member
        if is_mpim is not UNSET:
            field_dict["is_mpim"] = is_mpim
        if is_open is not UNSET:
            field_dict["is_open"] = is_open
        if is_org_shared is not UNSET:
            field_dict["is_org_shared"] = is_org_shared
        if is_pending_ext_shared is not UNSET:
            field_dict["is_pending_ext_shared"] = is_pending_ext_shared
        if is_private is not UNSET:
            field_dict["is_private"] = is_private
        if is_shared is not UNSET:
            field_dict["is_shared"] = is_shared
        if last_read is not UNSET:
            field_dict["last_read"] = last_read
        if name is not UNSET:
            field_dict["name"] = name
        if name_normalized is not UNSET:
            field_dict["name_normalized"] = name_normalized
        if priority is not UNSET:
            field_dict["priority"] = priority
        if purpose is not UNSET:
            field_dict["purpose"] = purpose
        if shared_team_ids is not UNSET:
            field_dict["shared_team_ids"] = shared_team_ids
        if topic is not UNSET:
            field_dict["topic"] = topic
        if unlinked is not UNSET:
            field_dict["unlinked"] = unlinked

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.create_channel_response_purpose import (
            CreateChannelResponsePurpose,
        )
        from ..models.create_channel_response_topic import CreateChannelResponseTopic

        d = src_dict.copy()
        created = d.pop("created", UNSET)

        creator = d.pop("creator", UNSET)

        id = d.pop("id", UNSET)

        is_archived = d.pop("is_archived", UNSET)

        is_channel = d.pop("is_channel", UNSET)

        is_ext_shared = d.pop("is_ext_shared", UNSET)

        is_general = d.pop("is_general", UNSET)

        is_group = d.pop("is_group", UNSET)

        is_im = d.pop("is_im", UNSET)

        is_member = d.pop("is_member", UNSET)

        is_mpim = d.pop("is_mpim", UNSET)

        is_open = d.pop("is_open", UNSET)

        is_org_shared = d.pop("is_org_shared", UNSET)

        is_pending_ext_shared = d.pop("is_pending_ext_shared", UNSET)

        is_private = d.pop("is_private", UNSET)

        is_shared = d.pop("is_shared", UNSET)

        last_read = d.pop("last_read", UNSET)

        name = d.pop("name", UNSET)

        name_normalized = d.pop("name_normalized", UNSET)

        priority = d.pop("priority", UNSET)

        _purpose = d.pop("purpose", UNSET)
        purpose: Union[Unset, CreateChannelResponsePurpose]
        if isinstance(_purpose, Unset):
            purpose = UNSET
        else:
            purpose = CreateChannelResponsePurpose.from_dict(_purpose)

        shared_team_ids = cast(list[str], d.pop("shared_team_ids", UNSET))

        _topic = d.pop("topic", UNSET)
        topic: Union[Unset, CreateChannelResponseTopic]
        if isinstance(_topic, Unset):
            topic = UNSET
        else:
            topic = CreateChannelResponseTopic.from_dict(_topic)

        unlinked = d.pop("unlinked", UNSET)

        create_channel_response = cls(
            created=created,
            creator=creator,
            id=id,
            is_archived=is_archived,
            is_channel=is_channel,
            is_ext_shared=is_ext_shared,
            is_general=is_general,
            is_group=is_group,
            is_im=is_im,
            is_member=is_member,
            is_mpim=is_mpim,
            is_open=is_open,
            is_org_shared=is_org_shared,
            is_pending_ext_shared=is_pending_ext_shared,
            is_private=is_private,
            is_shared=is_shared,
            last_read=last_read,
            name=name,
            name_normalized=name_normalized,
            priority=priority,
            purpose=purpose,
            shared_team_ids=shared_team_ids,
            topic=topic,
            unlinked=unlinked,
        )

        create_channel_response.additional_properties = d
        return create_channel_response

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
