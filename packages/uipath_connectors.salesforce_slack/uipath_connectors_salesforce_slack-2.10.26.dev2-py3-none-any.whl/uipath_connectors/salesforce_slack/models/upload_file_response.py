from typing import Any, Dict, Type, Optional
from pydantic import BaseModel, ConfigDict

from ..models.upload_file_response_reactions_array_item_ref import (
    UploadFileResponseReactionsArrayItemRef,
)


class UploadFileResponse(BaseModel):
    """
    Attributes:
        channels (Optional[list[str]]):
        comments_count (Optional[int]):
        created (Optional[int]):
        date_delete (Optional[int]):
        display_as_bot (Optional[bool]):
        editable (Optional[bool]):
        editor (Optional[str]):
        external_id (Optional[str]):
        external_type (Optional[str]):
        external_url (Optional[str]):
        filetype (Optional[str]):
        groups (Optional[list[str]]):
        has_rich_preview (Optional[bool]):
        id (Optional[str]): The output ID of the file uploaded
        image_exif_rotation (Optional[int]):
        ims (Optional[list[str]]):
        is_external (Optional[bool]):
        is_public (Optional[bool]):
        is_starred (Optional[bool]):
        is_tombstoned (Optional[bool]):
        user_team (Optional[str]): The unique identifier for the user's team. Example: T01G1P7CKR8.
        file_access (Optional[str]): The access permissions set for the file. Example: visible.
        has_more_shares (Optional[bool]): Indicates if there are more shares available.
        mimetype (Optional[str]):
        mode (Optional[str]):
        name (Optional[str]):
        non_owner_editable (Optional[bool]):
        num_stars (Optional[int]):
        original_h (Optional[int]):
        original_w (Optional[int]):
        permalink (Optional[str]):
        permalink_public (Optional[str]):
        pinned_to (Optional[list[str]]):
        pretty_type (Optional[str]):
        preview (Optional[str]):
        public_url_shared (Optional[bool]):
        reactions (Optional[list['UploadFileResponseReactionsArrayItemRef']]):
        size (Optional[int]):
        source_team (Optional[str]):
        state (Optional[str]):
        thumb_1024 (Optional[str]):
        thumb_1024_h (Optional[int]):
        thumb_1024_w (Optional[int]):
        thumb_160 (Optional[str]):
        thumb_360 (Optional[str]):
        thumb_360_h (Optional[int]):
        thumb_360_w (Optional[int]):
        thumb_480 (Optional[str]):
        thumb_480_h (Optional[int]):
        thumb_480_w (Optional[int]):
        thumb_64 (Optional[str]):
        thumb_720 (Optional[str]):
        thumb_720_h (Optional[int]):
        thumb_720_w (Optional[int]):
        thumb_80 (Optional[str]):
        thumb_800 (Optional[str]):
        thumb_800_h (Optional[int]):
        thumb_800_w (Optional[int]):
        thumb_960 (Optional[str]):
        thumb_960_h (Optional[int]):
        thumb_960_w (Optional[int]):
        thumb_tiny (Optional[str]):
        timestamp (Optional[int]):
        title (Optional[str]):
        updated (Optional[int]):
        url_private (Optional[str]): The output URL of the file uploaded
        url_private_download (Optional[str]):
        user (Optional[str]):
        username (Optional[str]):
    """

    model_config = ConfigDict(extra="allow")

    channels: Optional[list[str]] = None
    comments_count: Optional[int] = None
    created: Optional[int] = None
    date_delete: Optional[int] = None
    display_as_bot: Optional[bool] = None
    editable: Optional[bool] = None
    editor: Optional[str] = None
    external_id: Optional[str] = None
    external_type: Optional[str] = None
    external_url: Optional[str] = None
    filetype: Optional[str] = None
    groups: Optional[list[str]] = None
    has_rich_preview: Optional[bool] = None
    id: Optional[str] = None
    image_exif_rotation: Optional[int] = None
    ims: Optional[list[str]] = None
    is_external: Optional[bool] = None
    is_public: Optional[bool] = None
    is_starred: Optional[bool] = None
    is_tombstoned: Optional[bool] = None
    user_team: Optional[str] = None
    file_access: Optional[str] = None
    has_more_shares: Optional[bool] = None
    mimetype: Optional[str] = None
    mode: Optional[str] = None
    name: Optional[str] = None
    non_owner_editable: Optional[bool] = None
    num_stars: Optional[int] = None
    original_h: Optional[int] = None
    original_w: Optional[int] = None
    permalink: Optional[str] = None
    permalink_public: Optional[str] = None
    pinned_to: Optional[list[str]] = None
    pretty_type: Optional[str] = None
    preview: Optional[str] = None
    public_url_shared: Optional[bool] = None
    reactions: Optional[list["UploadFileResponseReactionsArrayItemRef"]] = None
    size: Optional[int] = None
    source_team: Optional[str] = None
    state: Optional[str] = None
    thumb_1024: Optional[str] = None
    thumb_1024_h: Optional[int] = None
    thumb_1024_w: Optional[int] = None
    thumb_160: Optional[str] = None
    thumb_360: Optional[str] = None
    thumb_360_h: Optional[int] = None
    thumb_360_w: Optional[int] = None
    thumb_480: Optional[str] = None
    thumb_480_h: Optional[int] = None
    thumb_480_w: Optional[int] = None
    thumb_64: Optional[str] = None
    thumb_720: Optional[str] = None
    thumb_720_h: Optional[int] = None
    thumb_720_w: Optional[int] = None
    thumb_80: Optional[str] = None
    thumb_800: Optional[str] = None
    thumb_800_h: Optional[int] = None
    thumb_800_w: Optional[int] = None
    thumb_960: Optional[str] = None
    thumb_960_h: Optional[int] = None
    thumb_960_w: Optional[int] = None
    thumb_tiny: Optional[str] = None
    timestamp: Optional[int] = None
    title: Optional[str] = None
    updated: Optional[int] = None
    url_private: Optional[str] = None
    url_private_download: Optional[str] = None
    user: Optional[str] = None
    username: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return self.model_dump(exclude_none=True)

    @classmethod
    def from_dict(cls: Type["UploadFileResponse"], src_dict: Dict[str, Any]):
        return cls.model_validate(src_dict)

    @property
    def additional_keys(self) -> list[str]:
        base_fields = self.model_fields.keys()
        return [k for k in self.__dict__ if k not in base_fields]

    def __getitem__(self, key: str) -> Any:
        if key in self.__dict__:
            return self.__dict__[key]
        raise KeyError(key)

    def __setitem__(self, key: str, value: Any) -> None:
        self.__dict__[key] = value

    def __delitem__(self, key: str) -> None:
        if key in self.__dict__:
            del self.__dict__[key]
        else:
            raise KeyError(key)

    def __contains__(self, key: str) -> bool:
        return key in self.__dict__
