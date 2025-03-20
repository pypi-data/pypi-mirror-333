from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import Union


T = TypeVar("T", bound="GetUserByEmailResponseProfile")


@_attrs_define
class GetUserByEmailResponseProfile:
    """
    Attributes:
        avatar_hash (Union[Unset, str]):  Example: g6d998d80169.
        display_name (Union[Unset, str]):
        display_name_normalized (Union[Unset, str]):
        email (Union[Unset, str]):  Example: dhandu1995@gmail.com.
        huddle_state (Union[Unset, str]):  Example: default_unset.
        image_192 (Union[Unset, str]):  Example:
            https://secure.gravatar.com/avatar/6d998d801691b9d9198fe83d3f77c9f7.jpg?s=192&d=https%3A%2F%2Fa.slack-
            edge.com%2Fdf10d%2Fimg%2Favatars%2Fava_0025-192.png.
        image_24 (Union[Unset, str]):  Example:
            https://secure.gravatar.com/avatar/6d998d801691b9d9198fe83d3f77c9f7.jpg?s=24&d=https%3A%2F%2Fa.slack-
            edge.com%2Fdf10d%2Fimg%2Favatars%2Fava_0025-24.png.
        image_32 (Union[Unset, str]):  Example:
            https://secure.gravatar.com/avatar/6d998d801691b9d9198fe83d3f77c9f7.jpg?s=32&d=https%3A%2F%2Fa.slack-
            edge.com%2Fdf10d%2Fimg%2Favatars%2Fava_0025-32.png.
        image_48 (Union[Unset, str]):  Example:
            https://secure.gravatar.com/avatar/6d998d801691b9d9198fe83d3f77c9f7.jpg?s=48&d=https%3A%2F%2Fa.slack-
            edge.com%2Fdf10d%2Fimg%2Favatars%2Fava_0025-48.png.
        image_512 (Union[Unset, str]):  Example:
            https://secure.gravatar.com/avatar/6d998d801691b9d9198fe83d3f77c9f7.jpg?s=512&d=https%3A%2F%2Fa.slack-
            edge.com%2Fdf10d%2Fimg%2Favatars%2Fava_0025-512.png.
        image_72 (Union[Unset, str]):  Example:
            https://secure.gravatar.com/avatar/6d998d801691b9d9198fe83d3f77c9f7.jpg?s=72&d=https%3A%2F%2Fa.slack-
            edge.com%2Fdf10d%2Fimg%2Favatars%2Fava_0025-72.png.
        phone (Union[Unset, str]):
        real_name (Union[Unset, str]):  Example: dhandu1995.
        real_name_normalized (Union[Unset, str]):  Example: dhandu1995.
        skype (Union[Unset, str]):
        status_emoji (Union[Unset, str]):
        status_expiration (Union[Unset, int]):  Example: 0.0.
        status_text (Union[Unset, str]):
        status_text_canonical (Union[Unset, str]):
        team (Union[Unset, str]):  Example: T01G1P7CKR8.
        title (Union[Unset, str]):
    """

    avatar_hash: Union[Unset, str] = UNSET
    display_name: Union[Unset, str] = UNSET
    display_name_normalized: Union[Unset, str] = UNSET
    email: Union[Unset, str] = UNSET
    huddle_state: Union[Unset, str] = UNSET
    image_192: Union[Unset, str] = UNSET
    image_24: Union[Unset, str] = UNSET
    image_32: Union[Unset, str] = UNSET
    image_48: Union[Unset, str] = UNSET
    image_512: Union[Unset, str] = UNSET
    image_72: Union[Unset, str] = UNSET
    phone: Union[Unset, str] = UNSET
    real_name: Union[Unset, str] = UNSET
    real_name_normalized: Union[Unset, str] = UNSET
    skype: Union[Unset, str] = UNSET
    status_emoji: Union[Unset, str] = UNSET
    status_expiration: Union[Unset, int] = UNSET
    status_text: Union[Unset, str] = UNSET
    status_text_canonical: Union[Unset, str] = UNSET
    team: Union[Unset, str] = UNSET
    title: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        avatar_hash = self.avatar_hash

        display_name = self.display_name

        display_name_normalized = self.display_name_normalized

        email = self.email

        huddle_state = self.huddle_state

        image_192 = self.image_192

        image_24 = self.image_24

        image_32 = self.image_32

        image_48 = self.image_48

        image_512 = self.image_512

        image_72 = self.image_72

        phone = self.phone

        real_name = self.real_name

        real_name_normalized = self.real_name_normalized

        skype = self.skype

        status_emoji = self.status_emoji

        status_expiration = self.status_expiration

        status_text = self.status_text

        status_text_canonical = self.status_text_canonical

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
        if huddle_state is not UNSET:
            field_dict["huddle_state"] = huddle_state
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
        if status_expiration is not UNSET:
            field_dict["status_expiration"] = status_expiration
        if status_text is not UNSET:
            field_dict["status_text"] = status_text
        if status_text_canonical is not UNSET:
            field_dict["status_text_canonical"] = status_text_canonical
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

        huddle_state = d.pop("huddle_state", UNSET)

        image_192 = d.pop("image_192", UNSET)

        image_24 = d.pop("image_24", UNSET)

        image_32 = d.pop("image_32", UNSET)

        image_48 = d.pop("image_48", UNSET)

        image_512 = d.pop("image_512", UNSET)

        image_72 = d.pop("image_72", UNSET)

        phone = d.pop("phone", UNSET)

        real_name = d.pop("real_name", UNSET)

        real_name_normalized = d.pop("real_name_normalized", UNSET)

        skype = d.pop("skype", UNSET)

        status_emoji = d.pop("status_emoji", UNSET)

        status_expiration = d.pop("status_expiration", UNSET)

        status_text = d.pop("status_text", UNSET)

        status_text_canonical = d.pop("status_text_canonical", UNSET)

        team = d.pop("team", UNSET)

        title = d.pop("title", UNSET)

        get_user_by_email_response_profile = cls(
            avatar_hash=avatar_hash,
            display_name=display_name,
            display_name_normalized=display_name_normalized,
            email=email,
            huddle_state=huddle_state,
            image_192=image_192,
            image_24=image_24,
            image_32=image_32,
            image_48=image_48,
            image_512=image_512,
            image_72=image_72,
            phone=phone,
            real_name=real_name,
            real_name_normalized=real_name_normalized,
            skype=skype,
            status_emoji=status_emoji,
            status_expiration=status_expiration,
            status_text=status_text,
            status_text_canonical=status_text_canonical,
            team=team,
            title=title,
        )

        get_user_by_email_response_profile.additional_properties = d
        return get_user_by_email_response_profile

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
