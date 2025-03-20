from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import Union


T = TypeVar("T", bound="UploadFileResponse")


@_attrs_define
class UploadFileResponse:
    """
    Attributes:
        filetype (Union[Unset, str]): The Filetype
        title (Union[Unset, str]): The Title Example: abc.png.
        file_access (Union[Unset, str]): The File access Example: visible.
        mode (Union[Unset, str]): The Mode Example: hosted.
        media_display_type (Union[Unset, str]): The Media display type Example: unknown.
        url_private (Union[Unset, str]): The Url private Example: https://files.slack.com/files-
            pri/T01G1P7CKR8-F07T5FXKCRW/abc.png.
        id (Union[Unset, str]): The ID Example: F07T5FXKCRW.
        display_as_bot (Union[Unset, bool]): The Display as bot
        timestamp (Union[Unset, int]): The Timestamp Example: 1.729244937E9.
        created (Union[Unset, int]): The Created Example: 1.729244937E9.
        editable (Union[Unset, bool]): The Editable
        has_more_shares (Union[Unset, bool]): The Has more shares
        is_external (Union[Unset, bool]): The Is external
        pretty_type (Union[Unset, str]): The Pretty type
        external_type (Union[Unset, str]): The External type
        url_private_download (Union[Unset, str]): The Url private download Example: https://files.slack.com/files-
            pri/T01G1P7CKR8-F07T5FXKCRW/download/abc.png.
        user_team (Union[Unset, str]): The User team Example: T01G1P7CKR8.
        permalink_public (Union[Unset, str]): The Permalink public Example: https://slack-
            files.com/T01G1P7CKR8-F07T5FXKCRW-97a473ef9d.
        has_rich_preview (Union[Unset, bool]): The Has rich preview
        is_starred (Union[Unset, bool]): The Is starred
        size (Union[Unset, int]): The Size Example: 144576.0.
        comments_count (Union[Unset, int]): The Comments count Example: 0.0.
        name (Union[Unset, str]): The Name Example: abc.png.
        is_public (Union[Unset, bool]): The Is public
        mimetype (Union[Unset, str]): The Mimetype
        public_url_shared (Union[Unset, bool]): The Public url shared
        permalink (Union[Unset, str]): The Permalink Example:
            https://uipathslacktesting.slack.com/files/U02EBQA5AD9/F07T5FXKCRW/abc.png.
        user (Union[Unset, str]): The User Example: U02EBQA5AD9.
        username (Union[Unset, str]): The Username
    """

    filetype: Union[Unset, str] = UNSET
    title: Union[Unset, str] = UNSET
    file_access: Union[Unset, str] = UNSET
    mode: Union[Unset, str] = UNSET
    media_display_type: Union[Unset, str] = UNSET
    url_private: Union[Unset, str] = UNSET
    id: Union[Unset, str] = UNSET
    display_as_bot: Union[Unset, bool] = UNSET
    timestamp: Union[Unset, int] = UNSET
    created: Union[Unset, int] = UNSET
    editable: Union[Unset, bool] = UNSET
    has_more_shares: Union[Unset, bool] = UNSET
    is_external: Union[Unset, bool] = UNSET
    pretty_type: Union[Unset, str] = UNSET
    external_type: Union[Unset, str] = UNSET
    url_private_download: Union[Unset, str] = UNSET
    user_team: Union[Unset, str] = UNSET
    permalink_public: Union[Unset, str] = UNSET
    has_rich_preview: Union[Unset, bool] = UNSET
    is_starred: Union[Unset, bool] = UNSET
    size: Union[Unset, int] = UNSET
    comments_count: Union[Unset, int] = UNSET
    name: Union[Unset, str] = UNSET
    is_public: Union[Unset, bool] = UNSET
    mimetype: Union[Unset, str] = UNSET
    public_url_shared: Union[Unset, bool] = UNSET
    permalink: Union[Unset, str] = UNSET
    user: Union[Unset, str] = UNSET
    username: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        filetype = self.filetype

        title = self.title

        file_access = self.file_access

        mode = self.mode

        media_display_type = self.media_display_type

        url_private = self.url_private

        id = self.id

        display_as_bot = self.display_as_bot

        timestamp = self.timestamp

        created = self.created

        editable = self.editable

        has_more_shares = self.has_more_shares

        is_external = self.is_external

        pretty_type = self.pretty_type

        external_type = self.external_type

        url_private_download = self.url_private_download

        user_team = self.user_team

        permalink_public = self.permalink_public

        has_rich_preview = self.has_rich_preview

        is_starred = self.is_starred

        size = self.size

        comments_count = self.comments_count

        name = self.name

        is_public = self.is_public

        mimetype = self.mimetype

        public_url_shared = self.public_url_shared

        permalink = self.permalink

        user = self.user

        username = self.username

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if filetype is not UNSET:
            field_dict["filetype"] = filetype
        if title is not UNSET:
            field_dict["title"] = title
        if file_access is not UNSET:
            field_dict["file_access"] = file_access
        if mode is not UNSET:
            field_dict["mode"] = mode
        if media_display_type is not UNSET:
            field_dict["media_display_type"] = media_display_type
        if url_private is not UNSET:
            field_dict["url_private"] = url_private
        if id is not UNSET:
            field_dict["id"] = id
        if display_as_bot is not UNSET:
            field_dict["display_as_bot"] = display_as_bot
        if timestamp is not UNSET:
            field_dict["timestamp"] = timestamp
        if created is not UNSET:
            field_dict["created"] = created
        if editable is not UNSET:
            field_dict["editable"] = editable
        if has_more_shares is not UNSET:
            field_dict["has_more_shares"] = has_more_shares
        if is_external is not UNSET:
            field_dict["is_external"] = is_external
        if pretty_type is not UNSET:
            field_dict["pretty_type"] = pretty_type
        if external_type is not UNSET:
            field_dict["external_type"] = external_type
        if url_private_download is not UNSET:
            field_dict["url_private_download"] = url_private_download
        if user_team is not UNSET:
            field_dict["user_team"] = user_team
        if permalink_public is not UNSET:
            field_dict["permalink_public"] = permalink_public
        if has_rich_preview is not UNSET:
            field_dict["has_rich_preview"] = has_rich_preview
        if is_starred is not UNSET:
            field_dict["is_starred"] = is_starred
        if size is not UNSET:
            field_dict["size"] = size
        if comments_count is not UNSET:
            field_dict["comments_count"] = comments_count
        if name is not UNSET:
            field_dict["name"] = name
        if is_public is not UNSET:
            field_dict["is_public"] = is_public
        if mimetype is not UNSET:
            field_dict["mimetype"] = mimetype
        if public_url_shared is not UNSET:
            field_dict["public_url_shared"] = public_url_shared
        if permalink is not UNSET:
            field_dict["permalink"] = permalink
        if user is not UNSET:
            field_dict["user"] = user
        if username is not UNSET:
            field_dict["username"] = username

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        filetype = d.pop("filetype", UNSET)

        title = d.pop("title", UNSET)

        file_access = d.pop("file_access", UNSET)

        mode = d.pop("mode", UNSET)

        media_display_type = d.pop("media_display_type", UNSET)

        url_private = d.pop("url_private", UNSET)

        id = d.pop("id", UNSET)

        display_as_bot = d.pop("display_as_bot", UNSET)

        timestamp = d.pop("timestamp", UNSET)

        created = d.pop("created", UNSET)

        editable = d.pop("editable", UNSET)

        has_more_shares = d.pop("has_more_shares", UNSET)

        is_external = d.pop("is_external", UNSET)

        pretty_type = d.pop("pretty_type", UNSET)

        external_type = d.pop("external_type", UNSET)

        url_private_download = d.pop("url_private_download", UNSET)

        user_team = d.pop("user_team", UNSET)

        permalink_public = d.pop("permalink_public", UNSET)

        has_rich_preview = d.pop("has_rich_preview", UNSET)

        is_starred = d.pop("is_starred", UNSET)

        size = d.pop("size", UNSET)

        comments_count = d.pop("comments_count", UNSET)

        name = d.pop("name", UNSET)

        is_public = d.pop("is_public", UNSET)

        mimetype = d.pop("mimetype", UNSET)

        public_url_shared = d.pop("public_url_shared", UNSET)

        permalink = d.pop("permalink", UNSET)

        user = d.pop("user", UNSET)

        username = d.pop("username", UNSET)

        upload_file_response = cls(
            filetype=filetype,
            title=title,
            file_access=file_access,
            mode=mode,
            media_display_type=media_display_type,
            url_private=url_private,
            id=id,
            display_as_bot=display_as_bot,
            timestamp=timestamp,
            created=created,
            editable=editable,
            has_more_shares=has_more_shares,
            is_external=is_external,
            pretty_type=pretty_type,
            external_type=external_type,
            url_private_download=url_private_download,
            user_team=user_team,
            permalink_public=permalink_public,
            has_rich_preview=has_rich_preview,
            is_starred=is_starred,
            size=size,
            comments_count=comments_count,
            name=name,
            is_public=is_public,
            mimetype=mimetype,
            public_url_shared=public_url_shared,
            permalink=permalink,
            user=user,
            username=username,
        )

        upload_file_response.additional_properties = d
        return upload_file_response

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
