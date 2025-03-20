from typing import Any, TypeVar, TYPE_CHECKING

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import cast
from typing import Union

if TYPE_CHECKING:
    from ..models.send_message_to_user_response_root_icons import (
        SendMessageToUserResponseRootIcons,
    )
    from ..models.send_message_to_user_response_root_metadata import (
        SendMessageToUserResponseRootMetadata,
    )
    from ..models.send_message_to_user_response_root_blocks_array_item_ref import (
        SendMessageToUserResponseRootBlocksArrayItemRef,
    )


T = TypeVar("T", bound="SendMessageToUserResponseRoot")


@_attrs_define
class SendMessageToUserResponseRoot:
    """
    Attributes:
        app_id (Union[Unset, str]):  Example: A02CEJTE85R.
        blocks (Union[Unset, list['SendMessageToUserResponseRootBlocksArrayItemRef']]):
        bot_id (Union[Unset, str]):  Example: B02DYM5F1ST.
        icons (Union[Unset, SendMessageToUserResponseRootIcons]):
        is_locked (Union[Unset, bool]):
        latest_reply (Union[Unset, str]):  Example: 1675233584.607969.
        metadata (Union[Unset, SendMessageToUserResponseRootMetadata]):
        reply_count (Union[Unset, int]):  Example: 4.0.
        reply_users (Union[Unset, list[str]]):  Example: ['B02DYM5F1ST'].
        reply_users_count (Union[Unset, int]):  Example: 1.0.
        subscribed (Union[Unset, bool]):
        subtype (Union[Unset, str]):  Example: bot_message.
        text (Union[Unset, str]):  Example: failtest.
        thread_ts (Union[Unset, str]):  Example: 1675217357.904929.
        ts (Union[Unset, str]):  Example: 1675217357.904929.
        type_ (Union[Unset, str]):  Example: message.
        username (Union[Unset, str]):  Example: UiPath for Slack Staging.
    """

    app_id: Union[Unset, str] = UNSET
    blocks: Union[Unset, list["SendMessageToUserResponseRootBlocksArrayItemRef"]] = (
        UNSET
    )
    bot_id: Union[Unset, str] = UNSET
    icons: Union[Unset, "SendMessageToUserResponseRootIcons"] = UNSET
    is_locked: Union[Unset, bool] = UNSET
    latest_reply: Union[Unset, str] = UNSET
    metadata: Union[Unset, "SendMessageToUserResponseRootMetadata"] = UNSET
    reply_count: Union[Unset, int] = UNSET
    reply_users: Union[Unset, list[str]] = UNSET
    reply_users_count: Union[Unset, int] = UNSET
    subscribed: Union[Unset, bool] = UNSET
    subtype: Union[Unset, str] = UNSET
    text: Union[Unset, str] = UNSET
    thread_ts: Union[Unset, str] = UNSET
    ts: Union[Unset, str] = UNSET
    type_: Union[Unset, str] = UNSET
    username: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:

        app_id = self.app_id

        blocks: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.blocks, Unset):
            blocks = []
            for (
                componentsschemas_send_message_to_user_response_root_blocks_item_data
            ) in self.blocks:
                componentsschemas_send_message_to_user_response_root_blocks_item = componentsschemas_send_message_to_user_response_root_blocks_item_data.to_dict()
                blocks.append(
                    componentsschemas_send_message_to_user_response_root_blocks_item
                )

        bot_id = self.bot_id

        icons: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.icons, Unset):
            icons = self.icons.to_dict()

        is_locked = self.is_locked

        latest_reply = self.latest_reply

        metadata: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.metadata, Unset):
            metadata = self.metadata.to_dict()

        reply_count = self.reply_count

        reply_users: Union[Unset, list[str]] = UNSET
        if not isinstance(self.reply_users, Unset):
            reply_users = self.reply_users

        reply_users_count = self.reply_users_count

        subscribed = self.subscribed

        subtype = self.subtype

        text = self.text

        thread_ts = self.thread_ts

        ts = self.ts

        type_ = self.type_

        username = self.username

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if app_id is not UNSET:
            field_dict["app_id"] = app_id
        if blocks is not UNSET:
            field_dict["blocks"] = blocks
        if bot_id is not UNSET:
            field_dict["bot_id"] = bot_id
        if icons is not UNSET:
            field_dict["icons"] = icons
        if is_locked is not UNSET:
            field_dict["is_locked"] = is_locked
        if latest_reply is not UNSET:
            field_dict["latest_reply"] = latest_reply
        if metadata is not UNSET:
            field_dict["metadata"] = metadata
        if reply_count is not UNSET:
            field_dict["reply_count"] = reply_count
        if reply_users is not UNSET:
            field_dict["reply_users"] = reply_users
        if reply_users_count is not UNSET:
            field_dict["reply_users_count"] = reply_users_count
        if subscribed is not UNSET:
            field_dict["subscribed"] = subscribed
        if subtype is not UNSET:
            field_dict["subtype"] = subtype
        if text is not UNSET:
            field_dict["text"] = text
        if thread_ts is not UNSET:
            field_dict["thread_ts"] = thread_ts
        if ts is not UNSET:
            field_dict["ts"] = ts
        if type_ is not UNSET:
            field_dict["type"] = type_
        if username is not UNSET:
            field_dict["username"] = username

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.send_message_to_user_response_root_icons import (
            SendMessageToUserResponseRootIcons,
        )
        from ..models.send_message_to_user_response_root_metadata import (
            SendMessageToUserResponseRootMetadata,
        )
        from ..models.send_message_to_user_response_root_blocks_array_item_ref import (
            SendMessageToUserResponseRootBlocksArrayItemRef,
        )

        d = src_dict.copy()
        app_id = d.pop("app_id", UNSET)

        blocks = []
        _blocks = d.pop("blocks", UNSET)
        for componentsschemas_send_message_to_user_response_root_blocks_item_data in (
            _blocks or []
        ):
            componentsschemas_send_message_to_user_response_root_blocks_item = SendMessageToUserResponseRootBlocksArrayItemRef.from_dict(
                componentsschemas_send_message_to_user_response_root_blocks_item_data
            )

            blocks.append(
                componentsschemas_send_message_to_user_response_root_blocks_item
            )

        bot_id = d.pop("bot_id", UNSET)

        _icons = d.pop("icons", UNSET)
        icons: Union[Unset, SendMessageToUserResponseRootIcons]
        if isinstance(_icons, Unset):
            icons = UNSET
        else:
            icons = SendMessageToUserResponseRootIcons.from_dict(_icons)

        is_locked = d.pop("is_locked", UNSET)

        latest_reply = d.pop("latest_reply", UNSET)

        _metadata = d.pop("metadata", UNSET)
        metadata: Union[Unset, SendMessageToUserResponseRootMetadata]
        if isinstance(_metadata, Unset):
            metadata = UNSET
        else:
            metadata = SendMessageToUserResponseRootMetadata.from_dict(_metadata)

        reply_count = d.pop("reply_count", UNSET)

        reply_users = cast(list[str], d.pop("reply_users", UNSET))

        reply_users_count = d.pop("reply_users_count", UNSET)

        subscribed = d.pop("subscribed", UNSET)

        subtype = d.pop("subtype", UNSET)

        text = d.pop("text", UNSET)

        thread_ts = d.pop("thread_ts", UNSET)

        ts = d.pop("ts", UNSET)

        type_ = d.pop("type", UNSET)

        username = d.pop("username", UNSET)

        send_message_to_user_response_root = cls(
            app_id=app_id,
            blocks=blocks,
            bot_id=bot_id,
            icons=icons,
            is_locked=is_locked,
            latest_reply=latest_reply,
            metadata=metadata,
            reply_count=reply_count,
            reply_users=reply_users,
            reply_users_count=reply_users_count,
            subscribed=subscribed,
            subtype=subtype,
            text=text,
            thread_ts=thread_ts,
            ts=ts,
            type_=type_,
            username=username,
        )

        send_message_to_user_response_root.additional_properties = d
        return send_message_to_user_response_root

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
