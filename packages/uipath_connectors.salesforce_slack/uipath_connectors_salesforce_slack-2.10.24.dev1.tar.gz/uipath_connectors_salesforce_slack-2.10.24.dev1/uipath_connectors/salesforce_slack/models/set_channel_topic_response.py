from typing import Any, TypeVar, TYPE_CHECKING

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import cast
from typing import Union

if TYPE_CHECKING:
    from ..models.set_channel_topic_response_latest import SetChannelTopicResponseLatest
    from ..models.set_channel_topic_response_purpose import (
        SetChannelTopicResponsePurpose,
    )


T = TypeVar("T", bound="SetChannelTopicResponse")


@_attrs_define
class SetChannelTopicResponse:
    """
    Attributes:
        created (Union[Unset, int]):  Example: 1.649195947E9.
        creator (Union[Unset, str]):  Example: U12345678.
        id (Union[Unset, str]):  Example: C12345678.
        is_archived (Union[Unset, bool]):
        is_channel (Union[Unset, bool]):  Example: True.
        is_ext_shared (Union[Unset, bool]):
        is_frozen (Union[Unset, bool]):
        is_general (Union[Unset, bool]):
        is_group (Union[Unset, bool]):
        is_im (Union[Unset, bool]):
        is_member (Union[Unset, bool]):  Example: True.
        is_mpim (Union[Unset, bool]):
        is_org_shared (Union[Unset, bool]):
        is_pending_ext_shared (Union[Unset, bool]):
        is_private (Union[Unset, bool]):
        is_shared (Union[Unset, bool]):
        last_read (Union[Unset, str]):  Example: 1649869848.627809.
        latest (Union[Unset, SetChannelTopicResponseLatest]):
        name (Union[Unset, str]):  Example: tips-and-tricks.
        name_normalized (Union[Unset, str]):  Example: tips-and-tricks.
        parent_conversation (Union[Unset, str]):
        pending_connected_team_ids (Union[Unset, list[Any]]):
        pending_shared (Union[Unset, list[Any]]):
        previous_names (Union[Unset, list[Any]]):
        purpose (Union[Unset, SetChannelTopicResponsePurpose]):
        shared_team_ids (Union[Unset, list[str]]):  Example: ['T12345678'].
        unlinked (Union[Unset, int]):  Example: 0.0.
        unread_count (Union[Unset, int]):  Example: 1.0.
        unread_count_display (Union[Unset, int]):  Example: 0.0.
    """

    created: Union[Unset, int] = UNSET
    creator: Union[Unset, str] = UNSET
    id: Union[Unset, str] = UNSET
    is_archived: Union[Unset, bool] = UNSET
    is_channel: Union[Unset, bool] = UNSET
    is_ext_shared: Union[Unset, bool] = UNSET
    is_frozen: Union[Unset, bool] = UNSET
    is_general: Union[Unset, bool] = UNSET
    is_group: Union[Unset, bool] = UNSET
    is_im: Union[Unset, bool] = UNSET
    is_member: Union[Unset, bool] = UNSET
    is_mpim: Union[Unset, bool] = UNSET
    is_org_shared: Union[Unset, bool] = UNSET
    is_pending_ext_shared: Union[Unset, bool] = UNSET
    is_private: Union[Unset, bool] = UNSET
    is_shared: Union[Unset, bool] = UNSET
    last_read: Union[Unset, str] = UNSET
    latest: Union[Unset, "SetChannelTopicResponseLatest"] = UNSET
    name: Union[Unset, str] = UNSET
    name_normalized: Union[Unset, str] = UNSET
    parent_conversation: Union[Unset, str] = UNSET
    pending_connected_team_ids: Union[Unset, list[Any]] = UNSET
    pending_shared: Union[Unset, list[Any]] = UNSET
    previous_names: Union[Unset, list[Any]] = UNSET
    purpose: Union[Unset, "SetChannelTopicResponsePurpose"] = UNSET
    shared_team_ids: Union[Unset, list[str]] = UNSET
    unlinked: Union[Unset, int] = UNSET
    unread_count: Union[Unset, int] = UNSET
    unread_count_display: Union[Unset, int] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:

        created = self.created

        creator = self.creator

        id = self.id

        is_archived = self.is_archived

        is_channel = self.is_channel

        is_ext_shared = self.is_ext_shared

        is_frozen = self.is_frozen

        is_general = self.is_general

        is_group = self.is_group

        is_im = self.is_im

        is_member = self.is_member

        is_mpim = self.is_mpim

        is_org_shared = self.is_org_shared

        is_pending_ext_shared = self.is_pending_ext_shared

        is_private = self.is_private

        is_shared = self.is_shared

        last_read = self.last_read

        latest: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.latest, Unset):
            latest = self.latest.to_dict()

        name = self.name

        name_normalized = self.name_normalized

        parent_conversation = self.parent_conversation

        pending_connected_team_ids: Union[Unset, list[Any]] = UNSET
        if not isinstance(self.pending_connected_team_ids, Unset):
            pending_connected_team_ids = self.pending_connected_team_ids

        pending_shared: Union[Unset, list[Any]] = UNSET
        if not isinstance(self.pending_shared, Unset):
            pending_shared = self.pending_shared

        previous_names: Union[Unset, list[Any]] = UNSET
        if not isinstance(self.previous_names, Unset):
            previous_names = self.previous_names

        purpose: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.purpose, Unset):
            purpose = self.purpose.to_dict()

        shared_team_ids: Union[Unset, list[str]] = UNSET
        if not isinstance(self.shared_team_ids, Unset):
            shared_team_ids = self.shared_team_ids

        unlinked = self.unlinked

        unread_count = self.unread_count

        unread_count_display = self.unread_count_display

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
        if is_frozen is not UNSET:
            field_dict["is_frozen"] = is_frozen
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
        if is_shared is not UNSET:
            field_dict["is_shared"] = is_shared
        if last_read is not UNSET:
            field_dict["last_read"] = last_read
        if latest is not UNSET:
            field_dict["latest"] = latest
        if name is not UNSET:
            field_dict["name"] = name
        if name_normalized is not UNSET:
            field_dict["name_normalized"] = name_normalized
        if parent_conversation is not UNSET:
            field_dict["parent_conversation"] = parent_conversation
        if pending_connected_team_ids is not UNSET:
            field_dict["pending_connected_team_ids"] = pending_connected_team_ids
        if pending_shared is not UNSET:
            field_dict["pending_shared"] = pending_shared
        if previous_names is not UNSET:
            field_dict["previous_names"] = previous_names
        if purpose is not UNSET:
            field_dict["purpose"] = purpose
        if shared_team_ids is not UNSET:
            field_dict["shared_team_ids"] = shared_team_ids
        if unlinked is not UNSET:
            field_dict["unlinked"] = unlinked
        if unread_count is not UNSET:
            field_dict["unread_count"] = unread_count
        if unread_count_display is not UNSET:
            field_dict["unread_count_display"] = unread_count_display

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.set_channel_topic_response_latest import (
            SetChannelTopicResponseLatest,
        )
        from ..models.set_channel_topic_response_purpose import (
            SetChannelTopicResponsePurpose,
        )

        d = src_dict.copy()
        created = d.pop("created", UNSET)

        creator = d.pop("creator", UNSET)

        id = d.pop("id", UNSET)

        is_archived = d.pop("is_archived", UNSET)

        is_channel = d.pop("is_channel", UNSET)

        is_ext_shared = d.pop("is_ext_shared", UNSET)

        is_frozen = d.pop("is_frozen", UNSET)

        is_general = d.pop("is_general", UNSET)

        is_group = d.pop("is_group", UNSET)

        is_im = d.pop("is_im", UNSET)

        is_member = d.pop("is_member", UNSET)

        is_mpim = d.pop("is_mpim", UNSET)

        is_org_shared = d.pop("is_org_shared", UNSET)

        is_pending_ext_shared = d.pop("is_pending_ext_shared", UNSET)

        is_private = d.pop("is_private", UNSET)

        is_shared = d.pop("is_shared", UNSET)

        last_read = d.pop("last_read", UNSET)

        _latest = d.pop("latest", UNSET)
        latest: Union[Unset, SetChannelTopicResponseLatest]
        if isinstance(_latest, Unset):
            latest = UNSET
        else:
            latest = SetChannelTopicResponseLatest.from_dict(_latest)

        name = d.pop("name", UNSET)

        name_normalized = d.pop("name_normalized", UNSET)

        parent_conversation = d.pop("parent_conversation", UNSET)

        pending_connected_team_ids = cast(
            list[Any], d.pop("pending_connected_team_ids", UNSET)
        )

        pending_shared = cast(list[Any], d.pop("pending_shared", UNSET))

        previous_names = cast(list[Any], d.pop("previous_names", UNSET))

        _purpose = d.pop("purpose", UNSET)
        purpose: Union[Unset, SetChannelTopicResponsePurpose]
        if isinstance(_purpose, Unset):
            purpose = UNSET
        else:
            purpose = SetChannelTopicResponsePurpose.from_dict(_purpose)

        shared_team_ids = cast(list[str], d.pop("shared_team_ids", UNSET))

        unlinked = d.pop("unlinked", UNSET)

        unread_count = d.pop("unread_count", UNSET)

        unread_count_display = d.pop("unread_count_display", UNSET)

        set_channel_topic_response = cls(
            created=created,
            creator=creator,
            id=id,
            is_archived=is_archived,
            is_channel=is_channel,
            is_ext_shared=is_ext_shared,
            is_frozen=is_frozen,
            is_general=is_general,
            is_group=is_group,
            is_im=is_im,
            is_member=is_member,
            is_mpim=is_mpim,
            is_org_shared=is_org_shared,
            is_pending_ext_shared=is_pending_ext_shared,
            is_private=is_private,
            is_shared=is_shared,
            last_read=last_read,
            latest=latest,
            name=name,
            name_normalized=name_normalized,
            parent_conversation=parent_conversation,
            pending_connected_team_ids=pending_connected_team_ids,
            pending_shared=pending_shared,
            previous_names=previous_names,
            purpose=purpose,
            shared_team_ids=shared_team_ids,
            unlinked=unlinked,
            unread_count=unread_count,
            unread_count_display=unread_count_display,
        )

        set_channel_topic_response.additional_properties = d
        return set_channel_topic_response

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
