from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import Union


T = TypeVar("T", bound="ListAllUsersProfile")


@_attrs_define
class ListAllUsersProfile:
    """
    Attributes:
        avatar_hash (Union[Unset, str]):  Example: ge3b51ca72de.
        display_name (Union[Unset, str]):  Example: spengler.
        display_name_normalized (Union[Unset, str]):  Example: spengler.
        email (Union[Unset, str]):  Example: spengler@ghostbusters.example.com.
        first_name (Union[Unset, str]):  Example: Glinda.
        image_1024 (Union[Unset, str]):  Example: https://a.slack-edge.com...png.
        image_192 (Union[Unset, str]):  Example: https://.../avatar/e3b51ca72dee4ef87916ae2b9240df50.jpg.
        image_24 (Union[Unset, str]):  Example: https://.../avatar/e3b51ca72dee4ef87916ae2b9240df50.jpg.
        image_32 (Union[Unset, str]):  Example: https://.../avatar/e3b51ca72dee4ef87916ae2b9240df50.jpg.
        image_48 (Union[Unset, str]):  Example: https://.../avatar/e3b51ca72dee4ef87916ae2b9240df50.jpg.
        image_512 (Union[Unset, str]):  Example: https://.../avatar/e3b51ca72dee4ef87916ae2b9240df50.jpg.
        image_72 (Union[Unset, str]):  Example: https://.../avatar/e3b51ca72dee4ef87916ae2b9240df50.jpg.
        image_original (Union[Unset, str]):  Example: https://a.slack-edge.com...png.
        last_name (Union[Unset, str]):  Example: Southgood.
        phone (Union[Unset, str]):
        real_name (Union[Unset, str]):  Example: Egon Spengler.
        real_name_normalized (Union[Unset, str]):  Example: Egon Spengler.
        skype (Union[Unset, str]):
        status_emoji (Union[Unset, str]):  Example: :books:.
        status_text (Union[Unset, str]):  Example: Print is dead.
        team (Union[Unset, str]):  Example: T012AB3C4.
        title (Union[Unset, str]):  Example: Glinda the Good.
    """

    avatar_hash: Union[Unset, str] = UNSET
    display_name: Union[Unset, str] = UNSET
    display_name_normalized: Union[Unset, str] = UNSET
    email: Union[Unset, str] = UNSET
    first_name: Union[Unset, str] = UNSET
    image_1024: Union[Unset, str] = UNSET
    image_192: Union[Unset, str] = UNSET
    image_24: Union[Unset, str] = UNSET
    image_32: Union[Unset, str] = UNSET
    image_48: Union[Unset, str] = UNSET
    image_512: Union[Unset, str] = UNSET
    image_72: Union[Unset, str] = UNSET
    image_original: Union[Unset, str] = UNSET
    last_name: Union[Unset, str] = UNSET
    phone: Union[Unset, str] = UNSET
    real_name: Union[Unset, str] = UNSET
    real_name_normalized: Union[Unset, str] = UNSET
    skype: Union[Unset, str] = UNSET
    status_emoji: Union[Unset, str] = UNSET
    status_text: Union[Unset, str] = UNSET
    team: Union[Unset, str] = UNSET
    title: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        avatar_hash = self.avatar_hash

        display_name = self.display_name

        display_name_normalized = self.display_name_normalized

        email = self.email

        first_name = self.first_name

        image_1024 = self.image_1024

        image_192 = self.image_192

        image_24 = self.image_24

        image_32 = self.image_32

        image_48 = self.image_48

        image_512 = self.image_512

        image_72 = self.image_72

        image_original = self.image_original

        last_name = self.last_name

        phone = self.phone

        real_name = self.real_name

        real_name_normalized = self.real_name_normalized

        skype = self.skype

        status_emoji = self.status_emoji

        status_text = self.status_text

        team = self.team

        title = self.title

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if avatar_hash is not UNSET:
            field_dict["avatar_hash"] = avatar_hash
        if display_name is not UNSET:
            field_dict["display_name"] = display_name
        if display_name_normalized is not UNSET:
            field_dict["display_name_normalized"] = display_name_normalized
        if email is not UNSET:
            field_dict["email"] = email
        if first_name is not UNSET:
            field_dict["first_name"] = first_name
        if image_1024 is not UNSET:
            field_dict["image_1024"] = image_1024
        if image_192 is not UNSET:
            field_dict["image_192"] = image_192
        if image_24 is not UNSET:
            field_dict["image_24"] = image_24
        if image_32 is not UNSET:
            field_dict["image_32"] = image_32
        if image_48 is not UNSET:
            field_dict["image_48"] = image_48
        if image_512 is not UNSET:
            field_dict["image_512"] = image_512
        if image_72 is not UNSET:
            field_dict["image_72"] = image_72
        if image_original is not UNSET:
            field_dict["image_original"] = image_original
        if last_name is not UNSET:
            field_dict["last_name"] = last_name
        if phone is not UNSET:
            field_dict["phone"] = phone
        if real_name is not UNSET:
            field_dict["real_name"] = real_name
        if real_name_normalized is not UNSET:
            field_dict["real_name_normalized"] = real_name_normalized
        if skype is not UNSET:
            field_dict["skype"] = skype
        if status_emoji is not UNSET:
            field_dict["status_emoji"] = status_emoji
        if status_text is not UNSET:
            field_dict["status_text"] = status_text
        if team is not UNSET:
            field_dict["team"] = team
        if title is not UNSET:
            field_dict["title"] = title

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        avatar_hash = d.pop("avatar_hash", UNSET)

        display_name = d.pop("display_name", UNSET)

        display_name_normalized = d.pop("display_name_normalized", UNSET)

        email = d.pop("email", UNSET)

        first_name = d.pop("first_name", UNSET)

        image_1024 = d.pop("image_1024", UNSET)

        image_192 = d.pop("image_192", UNSET)

        image_24 = d.pop("image_24", UNSET)

        image_32 = d.pop("image_32", UNSET)

        image_48 = d.pop("image_48", UNSET)

        image_512 = d.pop("image_512", UNSET)

        image_72 = d.pop("image_72", UNSET)

        image_original = d.pop("image_original", UNSET)

        last_name = d.pop("last_name", UNSET)

        phone = d.pop("phone", UNSET)

        real_name = d.pop("real_name", UNSET)

        real_name_normalized = d.pop("real_name_normalized", UNSET)

        skype = d.pop("skype", UNSET)

        status_emoji = d.pop("status_emoji", UNSET)

        status_text = d.pop("status_text", UNSET)

        team = d.pop("team", UNSET)

        title = d.pop("title", UNSET)

        list_all_users_profile = cls(
            avatar_hash=avatar_hash,
            display_name=display_name,
            display_name_normalized=display_name_normalized,
            email=email,
            first_name=first_name,
            image_1024=image_1024,
            image_192=image_192,
            image_24=image_24,
            image_32=image_32,
            image_48=image_48,
            image_512=image_512,
            image_72=image_72,
            image_original=image_original,
            last_name=last_name,
            phone=phone,
            real_name=real_name,
            real_name_normalized=real_name_normalized,
            skype=skype,
            status_emoji=status_emoji,
            status_text=status_text,
            team=team,
            title=title,
        )

        list_all_users_profile.additional_properties = d
        return list_all_users_profile

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
