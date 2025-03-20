from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import Union


T = TypeVar("T", bound="UploadFileRequest")


@_attrs_define
class UploadFileRequest:
    """
    Attributes:
        url_private (Union[Unset, str]): The Url private Example: https://files.slack.com/files-
            pri/T01G1P7CKR8-F07T5FXKCRW/abc.png.
        id (Union[Unset, str]): The ID Example: F07T5FXKCRW.
    """

    url_private: Union[Unset, str] = UNSET
    id: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        url_private = self.url_private

        id = self.id

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if url_private is not UNSET:
            field_dict["url_private"] = url_private
        if id is not UNSET:
            field_dict["id"] = id

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        url_private = d.pop("url_private", UNSET)

        id = d.pop("id", UNSET)

        upload_file_request = cls(
            url_private=url_private,
            id=id,
        )

        upload_file_request.additional_properties = d
        return upload_file_request

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
