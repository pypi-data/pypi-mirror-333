from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import Union


T = TypeVar("T", bound="CreateUsergroupRequest")


@_attrs_define
class CreateUsergroupRequest:
    """
    Attributes:
        handle (str): A mention handle that is unique among channels, users and user groups. For example,
            @test_usergroup Example: marketing-team.
        name (str): A name for the user group. Must be unique among user groups Example: Marketing Team.
        channels (Union[Unset, str]): Default Channel IDs Example: D02EBQBE7QS,D04RX3MJHMZ.
        description (Union[Unset, str]): A short description of the user group Example: Marketing gurus, PR experts and
            product advocates..
        include_count (Union[Unset, bool]):  Example: True.
        team_id (Union[Unset, str]):  Example: T060RNRCH.
    """

    handle: str
    name: str
    channels: Union[Unset, str] = UNSET
    description: Union[Unset, str] = UNSET
    include_count: Union[Unset, bool] = UNSET
    team_id: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        handle = self.handle

        name = self.name

        channels = self.channels

        description = self.description

        include_count = self.include_count

        team_id = self.team_id

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "handle": handle,
                "name": name,
            }
        )
        if channels is not UNSET:
            field_dict["channels"] = channels
        if description is not UNSET:
            field_dict["description"] = description
        if include_count is not UNSET:
            field_dict["include_count"] = include_count
        if team_id is not UNSET:
            field_dict["team_id"] = team_id

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        handle = d.pop("handle")

        name = d.pop("name")

        channels = d.pop("channels", UNSET)

        description = d.pop("description", UNSET)

        include_count = d.pop("include_count", UNSET)

        team_id = d.pop("team_id", UNSET)

        create_usergroup_request = cls(
            handle=handle,
            name=name,
            channels=channels,
            description=description,
            include_count=include_count,
            team_id=team_id,
        )

        create_usergroup_request.additional_properties = d
        return create_usergroup_request

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
