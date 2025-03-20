from typing import Any, TypeVar, TYPE_CHECKING

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import Union

if TYPE_CHECKING:
    from ..models.get_user_by_email_response_profile import (
        GetUserByEmailResponseProfile,
    )


T = TypeVar("T", bound="GetUserByEmailResponse")


@_attrs_define
class GetUserByEmailResponse:
    """
    Attributes:
        color (Union[Unset, str]):  Example: 9f69e7.
        deleted (Union[Unset, bool]):
        has_2fa (Union[Unset, bool]):
        id (Union[Unset, str]): ID of a user Example: U01FYLMH1D3.
        is_admin (Union[Unset, bool]):  Example: True.
        is_app_user (Union[Unset, bool]):
        is_bot (Union[Unset, bool]):
        is_email_confirmed (Union[Unset, bool]):  Example: True.
        is_owner (Union[Unset, bool]):  Example: True.
        is_primary_owner (Union[Unset, bool]):  Example: True.
        is_restricted (Union[Unset, bool]):
        is_ultra_restricted (Union[Unset, bool]):
        name (Union[Unset, str]):  Example: dhandu1995.
        profile (Union[Unset, GetUserByEmailResponseProfile]):
        real_name (Union[Unset, str]):  Example: dhandu1995.
        team_id (Union[Unset, str]):  Example: T01G1P7CKR8.
        tz (Union[Unset, str]):  Example: Asia/Kolkata.
        tz_label (Union[Unset, str]):  Example: India Standard Time.
        tz_offset (Union[Unset, int]):  Example: 19800.0.
        updated (Union[Unset, int]):  Example: 1.664445309E9.
        who_can_share_contact_card (Union[Unset, str]):  Example: EVERYONE.
    """

    color: Union[Unset, str] = UNSET
    deleted: Union[Unset, bool] = UNSET
    has_2fa: Union[Unset, bool] = UNSET
    id: Union[Unset, str] = UNSET
    is_admin: Union[Unset, bool] = UNSET
    is_app_user: Union[Unset, bool] = UNSET
    is_bot: Union[Unset, bool] = UNSET
    is_email_confirmed: Union[Unset, bool] = UNSET
    is_owner: Union[Unset, bool] = UNSET
    is_primary_owner: Union[Unset, bool] = UNSET
    is_restricted: Union[Unset, bool] = UNSET
    is_ultra_restricted: Union[Unset, bool] = UNSET
    name: Union[Unset, str] = UNSET
    profile: Union[Unset, "GetUserByEmailResponseProfile"] = UNSET
    real_name: Union[Unset, str] = UNSET
    team_id: Union[Unset, str] = UNSET
    tz: Union[Unset, str] = UNSET
    tz_label: Union[Unset, str] = UNSET
    tz_offset: Union[Unset, int] = UNSET
    updated: Union[Unset, int] = UNSET
    who_can_share_contact_card: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:

        color = self.color

        deleted = self.deleted

        has_2fa = self.has_2fa

        id = self.id

        is_admin = self.is_admin

        is_app_user = self.is_app_user

        is_bot = self.is_bot

        is_email_confirmed = self.is_email_confirmed

        is_owner = self.is_owner

        is_primary_owner = self.is_primary_owner

        is_restricted = self.is_restricted

        is_ultra_restricted = self.is_ultra_restricted

        name = self.name

        profile: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.profile, Unset):
            profile = self.profile.to_dict()

        real_name = self.real_name

        team_id = self.team_id

        tz = self.tz

        tz_label = self.tz_label

        tz_offset = self.tz_offset

        updated = self.updated

        who_can_share_contact_card = self.who_can_share_contact_card

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if color is not UNSET:
            field_dict["color"] = color
        if deleted is not UNSET:
            field_dict["deleted"] = deleted
        if has_2fa is not UNSET:
            field_dict["has_2fa"] = has_2fa
        if id is not UNSET:
            field_dict["id"] = id
        if is_admin is not UNSET:
            field_dict["is_admin"] = is_admin
        if is_app_user is not UNSET:
            field_dict["is_app_user"] = is_app_user
        if is_bot is not UNSET:
            field_dict["is_bot"] = is_bot
        if is_email_confirmed is not UNSET:
            field_dict["is_email_confirmed"] = is_email_confirmed
        if is_owner is not UNSET:
            field_dict["is_owner"] = is_owner
        if is_primary_owner is not UNSET:
            field_dict["is_primary_owner"] = is_primary_owner
        if is_restricted is not UNSET:
            field_dict["is_restricted"] = is_restricted
        if is_ultra_restricted is not UNSET:
            field_dict["is_ultra_restricted"] = is_ultra_restricted
        if name is not UNSET:
            field_dict["name"] = name
        if profile is not UNSET:
            field_dict["profile"] = profile
        if real_name is not UNSET:
            field_dict["real_name"] = real_name
        if team_id is not UNSET:
            field_dict["team_id"] = team_id
        if tz is not UNSET:
            field_dict["tz"] = tz
        if tz_label is not UNSET:
            field_dict["tz_label"] = tz_label
        if tz_offset is not UNSET:
            field_dict["tz_offset"] = tz_offset
        if updated is not UNSET:
            field_dict["updated"] = updated
        if who_can_share_contact_card is not UNSET:
            field_dict["who_can_share_contact_card"] = who_can_share_contact_card

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.get_user_by_email_response_profile import (
            GetUserByEmailResponseProfile,
        )

        d = src_dict.copy()
        color = d.pop("color", UNSET)

        deleted = d.pop("deleted", UNSET)

        has_2fa = d.pop("has_2fa", UNSET)

        id = d.pop("id", UNSET)

        is_admin = d.pop("is_admin", UNSET)

        is_app_user = d.pop("is_app_user", UNSET)

        is_bot = d.pop("is_bot", UNSET)

        is_email_confirmed = d.pop("is_email_confirmed", UNSET)

        is_owner = d.pop("is_owner", UNSET)

        is_primary_owner = d.pop("is_primary_owner", UNSET)

        is_restricted = d.pop("is_restricted", UNSET)

        is_ultra_restricted = d.pop("is_ultra_restricted", UNSET)

        name = d.pop("name", UNSET)

        _profile = d.pop("profile", UNSET)
        profile: Union[Unset, GetUserByEmailResponseProfile]
        if isinstance(_profile, Unset):
            profile = UNSET
        else:
            profile = GetUserByEmailResponseProfile.from_dict(_profile)

        real_name = d.pop("real_name", UNSET)

        team_id = d.pop("team_id", UNSET)

        tz = d.pop("tz", UNSET)

        tz_label = d.pop("tz_label", UNSET)

        tz_offset = d.pop("tz_offset", UNSET)

        updated = d.pop("updated", UNSET)

        who_can_share_contact_card = d.pop("who_can_share_contact_card", UNSET)

        get_user_by_email_response = cls(
            color=color,
            deleted=deleted,
            has_2fa=has_2fa,
            id=id,
            is_admin=is_admin,
            is_app_user=is_app_user,
            is_bot=is_bot,
            is_email_confirmed=is_email_confirmed,
            is_owner=is_owner,
            is_primary_owner=is_primary_owner,
            is_restricted=is_restricted,
            is_ultra_restricted=is_ultra_restricted,
            name=name,
            profile=profile,
            real_name=real_name,
            team_id=team_id,
            tz=tz,
            tz_label=tz_label,
            tz_offset=tz_offset,
            updated=updated,
            who_can_share_contact_card=who_can_share_contact_card,
        )

        get_user_by_email_response.additional_properties = d
        return get_user_by_email_response

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
