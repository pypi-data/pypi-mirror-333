from typing import Any, TypeVar, TYPE_CHECKING

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import Union

if TYPE_CHECKING:
    from ..models.list_all_usergroups_usergroups_prefs import (
        ListAllUsergroupsUsergroupsPrefs,
    )


T = TypeVar("T", bound="ListAllUsergroupsUsergroupsArrayItemRef")


@_attrs_define
class ListAllUsergroupsUsergroupsArrayItemRef:
    """
    Attributes:
        auto_provision (Union[Unset, bool]):
        channel_count (Union[Unset, int]):
        created_by (Union[Unset, str]):
        date_create (Union[Unset, int]):
        date_delete (Union[Unset, int]):
        date_update (Union[Unset, int]):
        description (Union[Unset, str]):
        enterprise_subteam_id (Union[Unset, str]):
        handle (Union[Unset, str]):
        id (Union[Unset, str]):
        is_external (Union[Unset, bool]):
        is_subteam (Union[Unset, bool]):
        is_usergroup (Union[Unset, bool]):
        name (Union[Unset, str]):
        prefs (Union[Unset, ListAllUsergroupsUsergroupsPrefs]):
        team_id (Union[Unset, str]):
        user_count (Union[Unset, int]):
    """

    auto_provision: Union[Unset, bool] = UNSET
    channel_count: Union[Unset, int] = UNSET
    created_by: Union[Unset, str] = UNSET
    date_create: Union[Unset, int] = UNSET
    date_delete: Union[Unset, int] = UNSET
    date_update: Union[Unset, int] = UNSET
    description: Union[Unset, str] = UNSET
    enterprise_subteam_id: Union[Unset, str] = UNSET
    handle: Union[Unset, str] = UNSET
    id: Union[Unset, str] = UNSET
    is_external: Union[Unset, bool] = UNSET
    is_subteam: Union[Unset, bool] = UNSET
    is_usergroup: Union[Unset, bool] = UNSET
    name: Union[Unset, str] = UNSET
    prefs: Union[Unset, "ListAllUsergroupsUsergroupsPrefs"] = UNSET
    team_id: Union[Unset, str] = UNSET
    user_count: Union[Unset, int] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:

        auto_provision = self.auto_provision

        channel_count = self.channel_count

        created_by = self.created_by

        date_create = self.date_create

        date_delete = self.date_delete

        date_update = self.date_update

        description = self.description

        enterprise_subteam_id = self.enterprise_subteam_id

        handle = self.handle

        id = self.id

        is_external = self.is_external

        is_subteam = self.is_subteam

        is_usergroup = self.is_usergroup

        name = self.name

        prefs: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.prefs, Unset):
            prefs = self.prefs.to_dict()

        team_id = self.team_id

        user_count = self.user_count

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if auto_provision is not UNSET:
            field_dict["auto_provision"] = auto_provision
        if channel_count is not UNSET:
            field_dict["channel_count"] = channel_count
        if created_by is not UNSET:
            field_dict["created_by"] = created_by
        if date_create is not UNSET:
            field_dict["date_create"] = date_create
        if date_delete is not UNSET:
            field_dict["date_delete"] = date_delete
        if date_update is not UNSET:
            field_dict["date_update"] = date_update
        if description is not UNSET:
            field_dict["description"] = description
        if enterprise_subteam_id is not UNSET:
            field_dict["enterprise_subteam_id"] = enterprise_subteam_id
        if handle is not UNSET:
            field_dict["handle"] = handle
        if id is not UNSET:
            field_dict["id"] = id
        if is_external is not UNSET:
            field_dict["is_external"] = is_external
        if is_subteam is not UNSET:
            field_dict["is_subteam"] = is_subteam
        if is_usergroup is not UNSET:
            field_dict["is_usergroup"] = is_usergroup
        if name is not UNSET:
            field_dict["name"] = name
        if prefs is not UNSET:
            field_dict["prefs"] = prefs
        if team_id is not UNSET:
            field_dict["team_id"] = team_id
        if user_count is not UNSET:
            field_dict["user_count"] = user_count

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.list_all_usergroups_usergroups_prefs import (
            ListAllUsergroupsUsergroupsPrefs,
        )

        d = src_dict.copy()
        auto_provision = d.pop("auto_provision", UNSET)

        channel_count = d.pop("channel_count", UNSET)

        created_by = d.pop("created_by", UNSET)

        date_create = d.pop("date_create", UNSET)

        date_delete = d.pop("date_delete", UNSET)

        date_update = d.pop("date_update", UNSET)

        description = d.pop("description", UNSET)

        enterprise_subteam_id = d.pop("enterprise_subteam_id", UNSET)

        handle = d.pop("handle", UNSET)

        id = d.pop("id", UNSET)

        is_external = d.pop("is_external", UNSET)

        is_subteam = d.pop("is_subteam", UNSET)

        is_usergroup = d.pop("is_usergroup", UNSET)

        name = d.pop("name", UNSET)

        _prefs = d.pop("prefs", UNSET)
        prefs: Union[Unset, ListAllUsergroupsUsergroupsPrefs]
        if isinstance(_prefs, Unset):
            prefs = UNSET
        else:
            prefs = ListAllUsergroupsUsergroupsPrefs.from_dict(_prefs)

        team_id = d.pop("team_id", UNSET)

        user_count = d.pop("user_count", UNSET)

        list_all_usergroups_usergroups_array_item_ref = cls(
            auto_provision=auto_provision,
            channel_count=channel_count,
            created_by=created_by,
            date_create=date_create,
            date_delete=date_delete,
            date_update=date_update,
            description=description,
            enterprise_subteam_id=enterprise_subteam_id,
            handle=handle,
            id=id,
            is_external=is_external,
            is_subteam=is_subteam,
            is_usergroup=is_usergroup,
            name=name,
            prefs=prefs,
            team_id=team_id,
            user_count=user_count,
        )

        list_all_usergroups_usergroups_array_item_ref.additional_properties = d
        return list_all_usergroups_usergroups_array_item_ref

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
