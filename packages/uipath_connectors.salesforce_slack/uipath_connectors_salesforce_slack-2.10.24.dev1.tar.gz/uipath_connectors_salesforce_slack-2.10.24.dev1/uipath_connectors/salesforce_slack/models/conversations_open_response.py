from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import Union


T = TypeVar("T", bound="ConversationsOpenResponse")


@_attrs_define
class ConversationsOpenResponse:
    """
    Attributes:
        created (Union[Unset, int]):  Example: 1.460147748E9.
        id (Union[Unset, str]):  Example: D069C7QFK.
        is_im (Union[Unset, bool]):  Example: True.
        is_open (Union[Unset, bool]):  Example: True.
        is_org_shared (Union[Unset, bool]):
        last_read (Union[Unset, str]):  Example: 0000000000.000000.
        latest (Union[Unset, str]):
        priority (Union[Unset, int]):  Example: 0.0.
        unread_count (Union[Unset, int]):  Example: 0.0.
        unread_count_display (Union[Unset, int]):  Example: 0.0.
        user (Union[Unset, str]):  Example: U069C7QF3.
    """

    created: Union[Unset, int] = UNSET
    id: Union[Unset, str] = UNSET
    is_im: Union[Unset, bool] = UNSET
    is_open: Union[Unset, bool] = UNSET
    is_org_shared: Union[Unset, bool] = UNSET
    last_read: Union[Unset, str] = UNSET
    latest: Union[Unset, str] = UNSET
    priority: Union[Unset, int] = UNSET
    unread_count: Union[Unset, int] = UNSET
    unread_count_display: Union[Unset, int] = UNSET
    user: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        created = self.created

        id = self.id

        is_im = self.is_im

        is_open = self.is_open

        is_org_shared = self.is_org_shared

        last_read = self.last_read

        latest = self.latest

        priority = self.priority

        unread_count = self.unread_count

        unread_count_display = self.unread_count_display

        user = self.user

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if created is not UNSET:
            field_dict["created"] = created
        if id is not UNSET:
            field_dict["id"] = id
        if is_im is not UNSET:
            field_dict["is_im"] = is_im
        if is_open is not UNSET:
            field_dict["is_open"] = is_open
        if is_org_shared is not UNSET:
            field_dict["is_org_shared"] = is_org_shared
        if last_read is not UNSET:
            field_dict["last_read"] = last_read
        if latest is not UNSET:
            field_dict["latest"] = latest
        if priority is not UNSET:
            field_dict["priority"] = priority
        if unread_count is not UNSET:
            field_dict["unread_count"] = unread_count
        if unread_count_display is not UNSET:
            field_dict["unread_count_display"] = unread_count_display
        if user is not UNSET:
            field_dict["user"] = user

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        created = d.pop("created", UNSET)

        id = d.pop("id", UNSET)

        is_im = d.pop("is_im", UNSET)

        is_open = d.pop("is_open", UNSET)

        is_org_shared = d.pop("is_org_shared", UNSET)

        last_read = d.pop("last_read", UNSET)

        latest = d.pop("latest", UNSET)

        priority = d.pop("priority", UNSET)

        unread_count = d.pop("unread_count", UNSET)

        unread_count_display = d.pop("unread_count_display", UNSET)

        user = d.pop("user", UNSET)

        conversations_open_response = cls(
            created=created,
            id=id,
            is_im=is_im,
            is_open=is_open,
            is_org_shared=is_org_shared,
            last_read=last_read,
            latest=latest,
            priority=priority,
            unread_count=unread_count,
            unread_count_display=unread_count_display,
            user=user,
        )

        conversations_open_response.additional_properties = d
        return conversations_open_response

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
