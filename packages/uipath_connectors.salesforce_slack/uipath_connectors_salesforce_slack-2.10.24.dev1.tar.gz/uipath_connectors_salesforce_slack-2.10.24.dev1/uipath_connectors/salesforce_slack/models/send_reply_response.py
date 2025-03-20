from typing import Any, TypeVar, TYPE_CHECKING

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import Union

if TYPE_CHECKING:
    from ..models.send_reply_response_icons import SendReplyResponseIcons
    from ..models.send_reply_response_metadata import SendReplyResponseMetadata
    from ..models.send_reply_response_root import SendReplyResponseRoot
    from ..models.send_reply_response_blocks_array_item_ref import (
        SendReplyResponseBlocksArrayItemRef,
    )
    from ..models.send_reply_response_message import SendReplyResponseMessage
    from ..models.send_reply_response_response_metadata import (
        SendReplyResponseResponseMetadata,
    )


T = TypeVar("T", bound="SendReplyResponse")


@_attrs_define
class SendReplyResponse:
    """
    Attributes:
        app_id (Union[Unset, str]):  Example: A02CEJTE85R.
        blocks (Union[Unset, list['SendReplyResponseBlocksArrayItemRef']]):
        channel (Union[Unset, str]): Select the public or private channel from the dropdown or pass channel name or
            channel ID. Ex: demo-slack-channel1 Example: C02CAP3LAAG.
        icons (Union[Unset, SendReplyResponseIcons]):
        message (Union[Unset, SendReplyResponseMessage]):
        metadata (Union[Unset, SendReplyResponseMetadata]):
        ok (Union[Unset, bool]):  Example: True.
        response_metadata (Union[Unset, SendReplyResponseResponseMetadata]):
        root (Union[Unset, SendReplyResponseRoot]):
        subtype (Union[Unset, str]):  Example: thread_broadcast.
        thread_ts (Union[Unset, str]): Message timestamp Example: 1675217357.904929.
        ts (Union[Unset, str]): The ID (timestamp) of the message sent Example: 1631092102.000400.
        username (Union[Unset, str]): Bot name Example: My Bot lalitha new.
    """

    app_id: Union[Unset, str] = UNSET
    blocks: Union[Unset, list["SendReplyResponseBlocksArrayItemRef"]] = UNSET
    channel: Union[Unset, str] = UNSET
    icons: Union[Unset, "SendReplyResponseIcons"] = UNSET
    message: Union[Unset, "SendReplyResponseMessage"] = UNSET
    metadata: Union[Unset, "SendReplyResponseMetadata"] = UNSET
    ok: Union[Unset, bool] = UNSET
    response_metadata: Union[Unset, "SendReplyResponseResponseMetadata"] = UNSET
    root: Union[Unset, "SendReplyResponseRoot"] = UNSET
    subtype: Union[Unset, str] = UNSET
    thread_ts: Union[Unset, str] = UNSET
    ts: Union[Unset, str] = UNSET
    username: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:

        app_id = self.app_id

        blocks: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.blocks, Unset):
            blocks = []
            for componentsschemas_send_reply_response_blocks_item_data in self.blocks:
                componentsschemas_send_reply_response_blocks_item = (
                    componentsschemas_send_reply_response_blocks_item_data.to_dict()
                )
                blocks.append(componentsschemas_send_reply_response_blocks_item)

        channel = self.channel

        icons: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.icons, Unset):
            icons = self.icons.to_dict()

        message: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.message, Unset):
            message = self.message.to_dict()

        metadata: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.metadata, Unset):
            metadata = self.metadata.to_dict()

        ok = self.ok

        response_metadata: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.response_metadata, Unset):
            response_metadata = self.response_metadata.to_dict()

        root: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.root, Unset):
            root = self.root.to_dict()

        subtype = self.subtype

        thread_ts = self.thread_ts

        ts = self.ts

        username = self.username

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if app_id is not UNSET:
            field_dict["app_id"] = app_id
        if blocks is not UNSET:
            field_dict["blocks"] = blocks
        if channel is not UNSET:
            field_dict["channel"] = channel
        if icons is not UNSET:
            field_dict["icons"] = icons
        if message is not UNSET:
            field_dict["message"] = message
        if metadata is not UNSET:
            field_dict["metadata"] = metadata
        if ok is not UNSET:
            field_dict["ok"] = ok
        if response_metadata is not UNSET:
            field_dict["response_metadata"] = response_metadata
        if root is not UNSET:
            field_dict["root"] = root
        if subtype is not UNSET:
            field_dict["subtype"] = subtype
        if thread_ts is not UNSET:
            field_dict["thread_ts"] = thread_ts
        if ts is not UNSET:
            field_dict["ts"] = ts
        if username is not UNSET:
            field_dict["username"] = username

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.send_reply_response_icons import SendReplyResponseIcons
        from ..models.send_reply_response_metadata import SendReplyResponseMetadata
        from ..models.send_reply_response_root import SendReplyResponseRoot
        from ..models.send_reply_response_blocks_array_item_ref import (
            SendReplyResponseBlocksArrayItemRef,
        )
        from ..models.send_reply_response_message import SendReplyResponseMessage
        from ..models.send_reply_response_response_metadata import (
            SendReplyResponseResponseMetadata,
        )

        d = src_dict.copy()
        app_id = d.pop("app_id", UNSET)

        blocks = []
        _blocks = d.pop("blocks", UNSET)
        for componentsschemas_send_reply_response_blocks_item_data in _blocks or []:
            componentsschemas_send_reply_response_blocks_item = (
                SendReplyResponseBlocksArrayItemRef.from_dict(
                    componentsschemas_send_reply_response_blocks_item_data
                )
            )

            blocks.append(componentsschemas_send_reply_response_blocks_item)

        channel = d.pop("channel", UNSET)

        _icons = d.pop("icons", UNSET)
        icons: Union[Unset, SendReplyResponseIcons]
        if isinstance(_icons, Unset):
            icons = UNSET
        else:
            icons = SendReplyResponseIcons.from_dict(_icons)

        _message = d.pop("message", UNSET)
        message: Union[Unset, SendReplyResponseMessage]
        if isinstance(_message, Unset):
            message = UNSET
        else:
            message = SendReplyResponseMessage.from_dict(_message)

        _metadata = d.pop("metadata", UNSET)
        metadata: Union[Unset, SendReplyResponseMetadata]
        if isinstance(_metadata, Unset):
            metadata = UNSET
        else:
            metadata = SendReplyResponseMetadata.from_dict(_metadata)

        ok = d.pop("ok", UNSET)

        _response_metadata = d.pop("response_metadata", UNSET)
        response_metadata: Union[Unset, SendReplyResponseResponseMetadata]
        if isinstance(_response_metadata, Unset):
            response_metadata = UNSET
        else:
            response_metadata = SendReplyResponseResponseMetadata.from_dict(
                _response_metadata
            )

        _root = d.pop("root", UNSET)
        root: Union[Unset, SendReplyResponseRoot]
        if isinstance(_root, Unset):
            root = UNSET
        else:
            root = SendReplyResponseRoot.from_dict(_root)

        subtype = d.pop("subtype", UNSET)

        thread_ts = d.pop("thread_ts", UNSET)

        ts = d.pop("ts", UNSET)

        username = d.pop("username", UNSET)

        send_reply_response = cls(
            app_id=app_id,
            blocks=blocks,
            channel=channel,
            icons=icons,
            message=message,
            metadata=metadata,
            ok=ok,
            response_metadata=response_metadata,
            root=root,
            subtype=subtype,
            thread_ts=thread_ts,
            ts=ts,
            username=username,
        )

        send_reply_response.additional_properties = d
        return send_reply_response

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
