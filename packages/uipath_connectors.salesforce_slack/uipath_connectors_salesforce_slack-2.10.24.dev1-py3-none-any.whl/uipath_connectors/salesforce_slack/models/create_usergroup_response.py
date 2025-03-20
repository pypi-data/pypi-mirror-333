from typing import Any, TypeVar, TYPE_CHECKING

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import Union

if TYPE_CHECKING:
    from ..models.create_usergroup_response_prefs import CreateUsergroupResponsePrefs


T = TypeVar("T", bound="CreateUsergroupResponse")


@_attrs_define
class CreateUsergroupResponse:
    """
    Attributes:
        auto_type (Union[Unset, str]):
        created_by (Union[Unset, str]):  Example: U060RNRCZ.
        date_create (Union[Unset, int]):  Example: 1.446746793E9.
        date_delete (Union[Unset, int]):  Example: 0.0.
        date_update (Union[Unset, int]):  Example: 1.446746793E9.
        deleted_by (Union[Unset, str]):
        description (Union[Unset, str]): A short description of the user group Example: Marketing gurus, PR experts and
            product advocates..
        handle (Union[Unset, str]): A mention handle that is unique among channels, users and user groups. For example,
            @test_usergroup Example: marketing-team.
        id (Union[Unset, str]): The unique id of the conversauser group. Example: S0615G0KT.
        is_external (Union[Unset, bool]):
        is_usergroup (Union[Unset, bool]):  Example: True.
        name (Union[Unset, str]): A name for the user group. Must be unique among user groups Example: Marketing Team.
        prefs (Union[Unset, CreateUsergroupResponsePrefs]):
        team_id (Union[Unset, str]):  Example: T060RNRCH.
        updated_by (Union[Unset, str]):  Example: U060RNRCZ.
        user_count (Union[Unset, int]):  Example: 0.
    """

    auto_type: Union[Unset, str] = UNSET
    created_by: Union[Unset, str] = UNSET
    date_create: Union[Unset, int] = UNSET
    date_delete: Union[Unset, int] = UNSET
    date_update: Union[Unset, int] = UNSET
    deleted_by: Union[Unset, str] = UNSET
    description: Union[Unset, str] = UNSET
    handle: Union[Unset, str] = UNSET
    id: Union[Unset, str] = UNSET
    is_external: Union[Unset, bool] = UNSET
    is_usergroup: Union[Unset, bool] = UNSET
    name: Union[Unset, str] = UNSET
    prefs: Union[Unset, "CreateUsergroupResponsePrefs"] = UNSET
    team_id: Union[Unset, str] = UNSET
    updated_by: Union[Unset, str] = UNSET
    user_count: Union[Unset, int] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:

        auto_type = self.auto_type

        created_by = self.created_by

        date_create = self.date_create

        date_delete = self.date_delete

        date_update = self.date_update

        deleted_by = self.deleted_by

        description = self.description

        handle = self.handle

        id = self.id

        is_external = self.is_external

        is_usergroup = self.is_usergroup

        name = self.name

        prefs: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.prefs, Unset):
            prefs = self.prefs.to_dict()

        team_id = self.team_id

        updated_by = self.updated_by

        user_count = self.user_count

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if auto_type is not UNSET:
            field_dict["auto_type"] = auto_type
        if created_by is not UNSET:
            field_dict["created_by"] = created_by
        if date_create is not UNSET:
            field_dict["date_create"] = date_create
        if date_delete is not UNSET:
            field_dict["date_delete"] = date_delete
        if date_update is not UNSET:
            field_dict["date_update"] = date_update
        if deleted_by is not UNSET:
            field_dict["deleted_by"] = deleted_by
        if description is not UNSET:
            field_dict["description"] = description
        if handle is not UNSET:
            field_dict["handle"] = handle
        if id is not UNSET:
            field_dict["id"] = id
        if is_external is not UNSET:
            field_dict["is_external"] = is_external
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

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.create_usergroup_response_prefs import (
            CreateUsergroupResponsePrefs,
        )

        d = src_dict.copy()
        auto_type = d.pop("auto_type", UNSET)

        created_by = d.pop("created_by", UNSET)

        date_create = d.pop("date_create", UNSET)

        date_delete = d.pop("date_delete", UNSET)

        date_update = d.pop("date_update", UNSET)

        deleted_by = d.pop("deleted_by", UNSET)

        description = d.pop("description", UNSET)

        handle = d.pop("handle", UNSET)

        id = d.pop("id", UNSET)

        is_external = d.pop("is_external", UNSET)

        is_usergroup = d.pop("is_usergroup", UNSET)

        name = d.pop("name", UNSET)

        _prefs = d.pop("prefs", UNSET)
        prefs: Union[Unset, CreateUsergroupResponsePrefs]
        if isinstance(_prefs, Unset):
            prefs = UNSET
        else:
            prefs = CreateUsergroupResponsePrefs.from_dict(_prefs)

        team_id = d.pop("team_id", UNSET)

        updated_by = d.pop("updated_by", UNSET)

        user_count = d.pop("user_count", UNSET)

        create_usergroup_response = cls(
            auto_type=auto_type,
            created_by=created_by,
            date_create=date_create,
            date_delete=date_delete,
            date_update=date_update,
            deleted_by=deleted_by,
            description=description,
            handle=handle,
            id=id,
            is_external=is_external,
            is_usergroup=is_usergroup,
            name=name,
            prefs=prefs,
            team_id=team_id,
            updated_by=updated_by,
            user_count=user_count,
        )

        create_usergroup_response.additional_properties = d
        return create_usergroup_response

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
