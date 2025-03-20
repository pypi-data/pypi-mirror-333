from typing import Any, TypeVar, TYPE_CHECKING

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import Union

if TYPE_CHECKING:
    from ..models.send_message_response_message_attachments_array_item_ref import (
        SendMessageResponseMessageAttachmentsArrayItemRef,
    )
    from ..models.send_message_response_message_blocks_array_item_ref import (
        SendMessageResponseMessageBlocksArrayItemRef,
    )
    from ..models.send_message_response_message_bot_profile import (
        SendMessageResponseMessageBotProfile,
    )
    from ..models.send_message_response_message_metadata import (
        SendMessageResponseMessageMetadata,
    )
    from ..models.send_message_response_message_root import (
        SendMessageResponseMessageRoot,
    )
    from ..models.send_message_response_message_icons import (
        SendMessageResponseMessageIcons,
    )


T = TypeVar("T", bound="SendMessageResponseMessage")


@_attrs_define
class SendMessageResponseMessage:
    """
    Attributes:
        app_id (Union[Unset, str]):  Example: A02CEJTE85R.
        attachments (Union[Unset, list['SendMessageResponseMessageAttachmentsArrayItemRef']]):
        blocks (Union[Unset, list['SendMessageResponseMessageBlocksArrayItemRef']]):
        bot_id (Union[Unset, str]):  Example: B02CRAP7A23.
        bot_profile (Union[Unset, SendMessageResponseMessageBotProfile]):
        icons (Union[Unset, SendMessageResponseMessageIcons]):
        metadata (Union[Unset, SendMessageResponseMessageMetadata]):
        root (Union[Unset, SendMessageResponseMessageRoot]):
        subtype (Union[Unset, str]):  Example: thread_broadcast.
        team (Union[Unset, str]):  Example: TCU0VUNLT.
        text (Union[Unset, str]):  Example: Would you like to play a game?.
        thread_ts (Union[Unset, str]):  Example: 1675217357.904929.
        ts (Union[Unset, str]):  Example: 1631092102.000400.
        type_ (Union[Unset, str]):  Example: message.
        user (Union[Unset, str]):  Example: UCUFVVCKS.
        username (Union[Unset, str]):  Example: My Bot lalitha new.
    """

    app_id: Union[Unset, str] = UNSET
    attachments: Union[
        Unset, list["SendMessageResponseMessageAttachmentsArrayItemRef"]
    ] = UNSET
    blocks: Union[Unset, list["SendMessageResponseMessageBlocksArrayItemRef"]] = UNSET
    bot_id: Union[Unset, str] = UNSET
    bot_profile: Union[Unset, "SendMessageResponseMessageBotProfile"] = UNSET
    icons: Union[Unset, "SendMessageResponseMessageIcons"] = UNSET
    metadata: Union[Unset, "SendMessageResponseMessageMetadata"] = UNSET
    root: Union[Unset, "SendMessageResponseMessageRoot"] = UNSET
    subtype: Union[Unset, str] = UNSET
    team: Union[Unset, str] = UNSET
    text: Union[Unset, str] = UNSET
    thread_ts: Union[Unset, str] = UNSET
    ts: Union[Unset, str] = UNSET
    type_: Union[Unset, str] = UNSET
    user: Union[Unset, str] = UNSET
    username: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:

        app_id = self.app_id

        attachments: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.attachments, Unset):
            attachments = []
            for (
                componentsschemas_send_message_response_message_attachments_item_data
            ) in self.attachments:
                componentsschemas_send_message_response_message_attachments_item = componentsschemas_send_message_response_message_attachments_item_data.to_dict()
                attachments.append(
                    componentsschemas_send_message_response_message_attachments_item
                )

        blocks: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.blocks, Unset):
            blocks = []
            for (
                componentsschemas_send_message_response_message_blocks_item_data
            ) in self.blocks:
                componentsschemas_send_message_response_message_blocks_item = componentsschemas_send_message_response_message_blocks_item_data.to_dict()
                blocks.append(
                    componentsschemas_send_message_response_message_blocks_item
                )

        bot_id = self.bot_id

        bot_profile: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.bot_profile, Unset):
            bot_profile = self.bot_profile.to_dict()

        icons: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.icons, Unset):
            icons = self.icons.to_dict()

        metadata: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.metadata, Unset):
            metadata = self.metadata.to_dict()

        root: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.root, Unset):
            root = self.root.to_dict()

        subtype = self.subtype

        team = self.team

        text = self.text

        thread_ts = self.thread_ts

        ts = self.ts

        type_ = self.type_

        user = self.user

        username = self.username

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if app_id is not UNSET:
            field_dict["app_id"] = app_id
        if attachments is not UNSET:
            field_dict["attachments"] = attachments
        if blocks is not UNSET:
            field_dict["blocks"] = blocks
        if bot_id is not UNSET:
            field_dict["bot_id"] = bot_id
        if bot_profile is not UNSET:
            field_dict["bot_profile"] = bot_profile
        if icons is not UNSET:
            field_dict["icons"] = icons
        if metadata is not UNSET:
            field_dict["metadata"] = metadata
        if root is not UNSET:
            field_dict["root"] = root
        if subtype is not UNSET:
            field_dict["subtype"] = subtype
        if team is not UNSET:
            field_dict["team"] = team
        if text is not UNSET:
            field_dict["text"] = text
        if thread_ts is not UNSET:
            field_dict["thread_ts"] = thread_ts
        if ts is not UNSET:
            field_dict["ts"] = ts
        if type_ is not UNSET:
            field_dict["type"] = type_
        if user is not UNSET:
            field_dict["user"] = user
        if username is not UNSET:
            field_dict["username"] = username

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.send_message_response_message_attachments_array_item_ref import (
            SendMessageResponseMessageAttachmentsArrayItemRef,
        )
        from ..models.send_message_response_message_blocks_array_item_ref import (
            SendMessageResponseMessageBlocksArrayItemRef,
        )
        from ..models.send_message_response_message_bot_profile import (
            SendMessageResponseMessageBotProfile,
        )
        from ..models.send_message_response_message_metadata import (
            SendMessageResponseMessageMetadata,
        )
        from ..models.send_message_response_message_root import (
            SendMessageResponseMessageRoot,
        )
        from ..models.send_message_response_message_icons import (
            SendMessageResponseMessageIcons,
        )

        d = src_dict.copy()
        app_id = d.pop("app_id", UNSET)

        attachments = []
        _attachments = d.pop("attachments", UNSET)
        for componentsschemas_send_message_response_message_attachments_item_data in (
            _attachments or []
        ):
            componentsschemas_send_message_response_message_attachments_item = SendMessageResponseMessageAttachmentsArrayItemRef.from_dict(
                componentsschemas_send_message_response_message_attachments_item_data
            )

            attachments.append(
                componentsschemas_send_message_response_message_attachments_item
            )

        blocks = []
        _blocks = d.pop("blocks", UNSET)
        for componentsschemas_send_message_response_message_blocks_item_data in (
            _blocks or []
        ):
            componentsschemas_send_message_response_message_blocks_item = (
                SendMessageResponseMessageBlocksArrayItemRef.from_dict(
                    componentsschemas_send_message_response_message_blocks_item_data
                )
            )

            blocks.append(componentsschemas_send_message_response_message_blocks_item)

        bot_id = d.pop("bot_id", UNSET)

        _bot_profile = d.pop("bot_profile", UNSET)
        bot_profile: Union[Unset, SendMessageResponseMessageBotProfile]
        if isinstance(_bot_profile, Unset):
            bot_profile = UNSET
        else:
            bot_profile = SendMessageResponseMessageBotProfile.from_dict(_bot_profile)

        _icons = d.pop("icons", UNSET)
        icons: Union[Unset, SendMessageResponseMessageIcons]
        if isinstance(_icons, Unset):
            icons = UNSET
        else:
            icons = SendMessageResponseMessageIcons.from_dict(_icons)

        _metadata = d.pop("metadata", UNSET)
        metadata: Union[Unset, SendMessageResponseMessageMetadata]
        if isinstance(_metadata, Unset):
            metadata = UNSET
        else:
            metadata = SendMessageResponseMessageMetadata.from_dict(_metadata)

        _root = d.pop("root", UNSET)
        root: Union[Unset, SendMessageResponseMessageRoot]
        if isinstance(_root, Unset):
            root = UNSET
        else:
            root = SendMessageResponseMessageRoot.from_dict(_root)

        subtype = d.pop("subtype", UNSET)

        team = d.pop("team", UNSET)

        text = d.pop("text", UNSET)

        thread_ts = d.pop("thread_ts", UNSET)

        ts = d.pop("ts", UNSET)

        type_ = d.pop("type", UNSET)

        user = d.pop("user", UNSET)

        username = d.pop("username", UNSET)

        send_message_response_message = cls(
            app_id=app_id,
            attachments=attachments,
            blocks=blocks,
            bot_id=bot_id,
            bot_profile=bot_profile,
            icons=icons,
            metadata=metadata,
            root=root,
            subtype=subtype,
            team=team,
            text=text,
            thread_ts=thread_ts,
            ts=ts,
            type_=type_,
            user=user,
            username=username,
        )

        send_message_response_message.additional_properties = d
        return send_message_response_message

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
