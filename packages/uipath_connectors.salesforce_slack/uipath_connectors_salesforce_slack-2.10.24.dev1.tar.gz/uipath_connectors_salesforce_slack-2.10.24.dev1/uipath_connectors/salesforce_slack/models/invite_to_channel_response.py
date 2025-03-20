from typing import Any, TypeVar, TYPE_CHECKING

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import cast
from typing import Union

if TYPE_CHECKING:
    from ..models.invite_to_channel_response_topic import InviteToChannelResponseTopic
    from ..models.invite_to_channel_response_purpose import (
        InviteToChannelResponsePurpose,
    )


T = TypeVar("T", bound="InviteToChannelResponse")


@_attrs_define
class InviteToChannelResponse:
    """
    Attributes:
        created (Union[Unset, int]):
        creator (Union[Unset, str]):
        id (Union[Unset, str]):
        is_archived (Union[Unset, bool]):
        is_channel (Union[Unset, bool]):
        is_ext_shared (Union[Unset, bool]):
        is_general (Union[Unset, bool]):
        is_group (Union[Unset, bool]):
        is_im (Union[Unset, bool]):
        is_member (Union[Unset, bool]):
        is_mpim (Union[Unset, bool]):
        is_org_shared (Union[Unset, bool]):
        is_pending_ext_shared (Union[Unset, bool]):
        is_private (Union[Unset, bool]):
        is_read_only (Union[Unset, bool]):
        is_shared (Union[Unset, bool]):
        last_read (Union[Unset, str]):
        name (Union[Unset, str]):
        name_normalized (Union[Unset, str]):
        pending_shared (Union[Unset, list[str]]):
        previous_names (Union[Unset, list[str]]):
        purpose (Union[Unset, InviteToChannelResponsePurpose]):
        topic (Union[Unset, InviteToChannelResponseTopic]):
        unlinked (Union[Unset, int]):
        context_team_id (Union[Unset, str]):  Example: T01G1P7CKR8.
        shared_team_ids (Union[Unset, list[str]]):  Example: ['T01G1P7CKR8'].
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
    is_org_shared: Union[Unset, bool] = UNSET
    is_pending_ext_shared: Union[Unset, bool] = UNSET
    is_private: Union[Unset, bool] = UNSET
    is_read_only: Union[Unset, bool] = UNSET
    is_shared: Union[Unset, bool] = UNSET
    last_read: Union[Unset, str] = UNSET
    name: Union[Unset, str] = UNSET
    name_normalized: Union[Unset, str] = UNSET
    pending_shared: Union[Unset, list[str]] = UNSET
    previous_names: Union[Unset, list[str]] = UNSET
    purpose: Union[Unset, "InviteToChannelResponsePurpose"] = UNSET
    topic: Union[Unset, "InviteToChannelResponseTopic"] = UNSET
    unlinked: Union[Unset, int] = UNSET
    context_team_id: Union[Unset, str] = UNSET
    shared_team_ids: Union[Unset, list[str]] = UNSET
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

        is_org_shared = self.is_org_shared

        is_pending_ext_shared = self.is_pending_ext_shared

        is_private = self.is_private

        is_read_only = self.is_read_only

        is_shared = self.is_shared

        last_read = self.last_read

        name = self.name

        name_normalized = self.name_normalized

        pending_shared: Union[Unset, list[str]] = UNSET
        if not isinstance(self.pending_shared, Unset):
            pending_shared = self.pending_shared

        previous_names: Union[Unset, list[str]] = UNSET
        if not isinstance(self.previous_names, Unset):
            previous_names = self.previous_names

        purpose: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.purpose, Unset):
            purpose = self.purpose.to_dict()

        topic: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.topic, Unset):
            topic = self.topic.to_dict()

        unlinked = self.unlinked

        context_team_id = self.context_team_id

        shared_team_ids: Union[Unset, list[str]] = UNSET
        if not isinstance(self.shared_team_ids, Unset):
            shared_team_ids = self.shared_team_ids

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
        if is_org_shared is not UNSET:
            field_dict["is_org_shared"] = is_org_shared
        if is_pending_ext_shared is not UNSET:
            field_dict["is_pending_ext_shared"] = is_pending_ext_shared
        if is_private is not UNSET:
            field_dict["is_private"] = is_private
        if is_read_only is not UNSET:
            field_dict["is_read_only"] = is_read_only
        if is_shared is not UNSET:
            field_dict["is_shared"] = is_shared
        if last_read is not UNSET:
            field_dict["last_read"] = last_read
        if name is not UNSET:
            field_dict["name"] = name
        if name_normalized is not UNSET:
            field_dict["name_normalized"] = name_normalized
        if pending_shared is not UNSET:
            field_dict["pending_shared"] = pending_shared
        if previous_names is not UNSET:
            field_dict["previous_names"] = previous_names
        if purpose is not UNSET:
            field_dict["purpose"] = purpose
        if topic is not UNSET:
            field_dict["topic"] = topic
        if unlinked is not UNSET:
            field_dict["unlinked"] = unlinked
        if context_team_id is not UNSET:
            field_dict["context_team_id"] = context_team_id
        if shared_team_ids is not UNSET:
            field_dict["shared_team_ids"] = shared_team_ids

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.invite_to_channel_response_topic import (
            InviteToChannelResponseTopic,
        )
        from ..models.invite_to_channel_response_purpose import (
            InviteToChannelResponsePurpose,
        )

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

        is_org_shared = d.pop("is_org_shared", UNSET)

        is_pending_ext_shared = d.pop("is_pending_ext_shared", UNSET)

        is_private = d.pop("is_private", UNSET)

        is_read_only = d.pop("is_read_only", UNSET)

        is_shared = d.pop("is_shared", UNSET)

        last_read = d.pop("last_read", UNSET)

        name = d.pop("name", UNSET)

        name_normalized = d.pop("name_normalized", UNSET)

        pending_shared = cast(list[str], d.pop("pending_shared", UNSET))

        previous_names = cast(list[str], d.pop("previous_names", UNSET))

        _purpose = d.pop("purpose", UNSET)
        purpose: Union[Unset, InviteToChannelResponsePurpose]
        if isinstance(_purpose, Unset):
            purpose = UNSET
        else:
            purpose = InviteToChannelResponsePurpose.from_dict(_purpose)

        _topic = d.pop("topic", UNSET)
        topic: Union[Unset, InviteToChannelResponseTopic]
        if isinstance(_topic, Unset):
            topic = UNSET
        else:
            topic = InviteToChannelResponseTopic.from_dict(_topic)

        unlinked = d.pop("unlinked", UNSET)

        context_team_id = d.pop("context_team_id", UNSET)

        shared_team_ids = cast(list[str], d.pop("shared_team_ids", UNSET))

        invite_to_channel_response = cls(
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
            is_org_shared=is_org_shared,
            is_pending_ext_shared=is_pending_ext_shared,
            is_private=is_private,
            is_read_only=is_read_only,
            is_shared=is_shared,
            last_read=last_read,
            name=name,
            name_normalized=name_normalized,
            pending_shared=pending_shared,
            previous_names=previous_names,
            purpose=purpose,
            topic=topic,
            unlinked=unlinked,
            context_team_id=context_team_id,
            shared_team_ids=shared_team_ids,
        )

        invite_to_channel_response.additional_properties = d
        return invite_to_channel_response

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
