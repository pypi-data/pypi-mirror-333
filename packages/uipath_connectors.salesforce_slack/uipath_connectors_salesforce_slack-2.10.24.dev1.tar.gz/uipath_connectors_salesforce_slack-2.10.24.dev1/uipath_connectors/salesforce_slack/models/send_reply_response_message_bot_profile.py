from typing import Any, TypeVar, TYPE_CHECKING

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import Union

if TYPE_CHECKING:
    from ..models.send_reply_response_message_bot_profile_icons import (
        SendReplyResponseMessageBotProfileIcons,
    )


T = TypeVar("T", bound="SendReplyResponseMessageBotProfile")


@_attrs_define
class SendReplyResponseMessageBotProfile:
    """
    Attributes:
        app_id (Union[Unset, str]):  Example: A44S6RJ2V.
        deleted (Union[Unset, bool]):
        icons (Union[Unset, SendReplyResponseMessageBotProfileIcons]):
        id (Union[Unset, str]):  Example: B02CRAP7A23.
        name (Union[Unset, str]):  Example: CE DEV App.
        team_id (Union[Unset, str]):  Example: TCU0VUNLT.
        updated (Union[Unset, int]):  Example: 1.63056859E9.
    """

    app_id: Union[Unset, str] = UNSET
    deleted: Union[Unset, bool] = UNSET
    icons: Union[Unset, "SendReplyResponseMessageBotProfileIcons"] = UNSET
    id: Union[Unset, str] = UNSET
    name: Union[Unset, str] = UNSET
    team_id: Union[Unset, str] = UNSET
    updated: Union[Unset, int] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:

        app_id = self.app_id

        deleted = self.deleted

        icons: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.icons, Unset):
            icons = self.icons.to_dict()

        id = self.id

        name = self.name

        team_id = self.team_id

        updated = self.updated

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if app_id is not UNSET:
            field_dict["app_id"] = app_id
        if deleted is not UNSET:
            field_dict["deleted"] = deleted
        if icons is not UNSET:
            field_dict["icons"] = icons
        if id is not UNSET:
            field_dict["id"] = id
        if name is not UNSET:
            field_dict["name"] = name
        if team_id is not UNSET:
            field_dict["team_id"] = team_id
        if updated is not UNSET:
            field_dict["updated"] = updated

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.send_reply_response_message_bot_profile_icons import (
            SendReplyResponseMessageBotProfileIcons,
        )

        d = src_dict.copy()
        app_id = d.pop("app_id", UNSET)

        deleted = d.pop("deleted", UNSET)

        _icons = d.pop("icons", UNSET)
        icons: Union[Unset, SendReplyResponseMessageBotProfileIcons]
        if isinstance(_icons, Unset):
            icons = UNSET
        else:
            icons = SendReplyResponseMessageBotProfileIcons.from_dict(_icons)

        id = d.pop("id", UNSET)

        name = d.pop("name", UNSET)

        team_id = d.pop("team_id", UNSET)

        updated = d.pop("updated", UNSET)

        send_reply_response_message_bot_profile = cls(
            app_id=app_id,
            deleted=deleted,
            icons=icons,
            id=id,
            name=name,
            team_id=team_id,
            updated=updated,
        )

        send_reply_response_message_bot_profile.additional_properties = d
        return send_reply_response_message_bot_profile

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
