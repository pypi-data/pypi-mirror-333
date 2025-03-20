from typing import Any, TypeVar, TYPE_CHECKING

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import cast
from typing import Union

if TYPE_CHECKING:
    from ..models.add_users_to_usergroup_response_usergroup_prefs import (
        AddUsersToUsergroupResponseUsergroupPrefs,
    )


T = TypeVar("T", bound="AddUsersToUsergroupResponseUsergroup")


@_attrs_define
class AddUsersToUsergroupResponseUsergroup:
    """
    Attributes:
        auto_provision (Union[Unset, bool]):
        channel_count (Union[Unset, int]):  Example: 0.0.
        created_by (Union[Unset, str]):  Example: U02K95UU71Q.
        date_create (Union[Unset, int]):  Example: 1.676803736E9.
        date_delete (Union[Unset, int]):  Example: 0.0.
        date_update (Union[Unset, int]):  Example: 1.683785723E9.
        description (Union[Unset, str]):  Example: testing.
        enterprise_subteam_id (Union[Unset, str]):
        handle (Union[Unset, str]):  Example: update-test-team-29468.
        id (Union[Unset, str]):  Example: S04Q3GYSMJS.
        is_external (Union[Unset, bool]):
        is_subteam (Union[Unset, bool]):  Example: True.
        is_usergroup (Union[Unset, bool]):  Example: True.
        name (Union[Unset, str]):  Example: Alpha Test Team 23840.
        prefs (Union[Unset, AddUsersToUsergroupResponseUsergroupPrefs]):
        team_id (Union[Unset, str]):  Example: T02KZCJHY1W.
        updated_by (Union[Unset, str]):  Example: U02K95UU71Q.
        user_count (Union[Unset, int]):  Example: 3.0.
        users (Union[Unset, list[str]]):  Example: ['U02K95UU71Q', 'U04Q3GTCF7G', 'U04QA5052EN'].
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
    prefs: Union[Unset, "AddUsersToUsergroupResponseUsergroupPrefs"] = UNSET
    team_id: Union[Unset, str] = UNSET
    updated_by: Union[Unset, str] = UNSET
    user_count: Union[Unset, int] = UNSET
    users: Union[Unset, list[str]] = UNSET
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

        updated_by = self.updated_by

        user_count = self.user_count

        users: Union[Unset, list[str]] = UNSET
        if not isinstance(self.users, Unset):
            users = self.users

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
        if updated_by is not UNSET:
            field_dict["updated_by"] = updated_by
        if user_count is not UNSET:
            field_dict["user_count"] = user_count
        if users is not UNSET:
            field_dict["users"] = users

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.add_users_to_usergroup_response_usergroup_prefs import (
            AddUsersToUsergroupResponseUsergroupPrefs,
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
        prefs: Union[Unset, AddUsersToUsergroupResponseUsergroupPrefs]
        if isinstance(_prefs, Unset):
            prefs = UNSET
        else:
            prefs = AddUsersToUsergroupResponseUsergroupPrefs.from_dict(_prefs)

        team_id = d.pop("team_id", UNSET)

        updated_by = d.pop("updated_by", UNSET)

        user_count = d.pop("user_count", UNSET)

        users = cast(list[str], d.pop("users", UNSET))

        add_users_to_usergroup_response_usergroup = cls(
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
            updated_by=updated_by,
            user_count=user_count,
            users=users,
        )

        add_users_to_usergroup_response_usergroup.additional_properties = d
        return add_users_to_usergroup_response_usergroup

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
