from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import Union


T = TypeVar("T", bound="DefaultError")


@_attrs_define
class DefaultError:
    """
    Attributes:
        request_id (Union[Unset, str]):
        message (Union[Unset, str]):
        provider_message (Union[Unset, str]):
    """

    request_id: Union[Unset, str] = UNSET
    message: Union[Unset, str] = UNSET
    provider_message: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        request_id = self.request_id

        message = self.message

        provider_message = self.provider_message

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if request_id is not UNSET:
            field_dict["requestId"] = request_id
        if message is not UNSET:
            field_dict["message"] = message
        if provider_message is not UNSET:
            field_dict["providerMessage"] = provider_message

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        request_id = d.pop("requestId", UNSET)

        message = d.pop("message", UNSET)

        provider_message = d.pop("providerMessage", UNSET)

        default_error = cls(
            request_id=request_id,
            message=message,
            provider_message=provider_message,
        )

        default_error.additional_properties = d
        return default_error

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
