from typing import Any, TypeVar, TYPE_CHECKING

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import Union

if TYPE_CHECKING:
    from ..models.send_message_response_message_root_blocks_elements_elements_array_item_ref import (
        SendMessageResponseMessageRootBlocksElementsElementsArrayItemRef,
    )


T = TypeVar("T", bound="SendMessageResponseMessageRootBlocksElementsArrayItemRef")


@_attrs_define
class SendMessageResponseMessageRootBlocksElementsArrayItemRef:
    """
    Attributes:
        elements (Union[Unset, list['SendMessageResponseMessageRootBlocksElementsElementsArrayItemRef']]):
        type_ (Union[Unset, str]):  Example: rich_text_section.
    """

    elements: Union[
        Unset, list["SendMessageResponseMessageRootBlocksElementsElementsArrayItemRef"]
    ] = UNSET
    type_: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:

        elements: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.elements, Unset):
            elements = []
            for componentsschemas_send_message_response_message_root_blocks_elements_elements_item_data in self.elements:
                componentsschemas_send_message_response_message_root_blocks_elements_elements_item = componentsschemas_send_message_response_message_root_blocks_elements_elements_item_data.to_dict()
                elements.append(
                    componentsschemas_send_message_response_message_root_blocks_elements_elements_item
                )

        type_ = self.type_

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if elements is not UNSET:
            field_dict["elements"] = elements
        if type_ is not UNSET:
            field_dict["type"] = type_

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.send_message_response_message_root_blocks_elements_elements_array_item_ref import (
            SendMessageResponseMessageRootBlocksElementsElementsArrayItemRef,
        )

        d = src_dict.copy()
        elements = []
        _elements = d.pop("elements", UNSET)
        for componentsschemas_send_message_response_message_root_blocks_elements_elements_item_data in (
            _elements or []
        ):
            componentsschemas_send_message_response_message_root_blocks_elements_elements_item = SendMessageResponseMessageRootBlocksElementsElementsArrayItemRef.from_dict(
                componentsschemas_send_message_response_message_root_blocks_elements_elements_item_data
            )

            elements.append(
                componentsschemas_send_message_response_message_root_blocks_elements_elements_item
            )

        type_ = d.pop("type", UNSET)

        send_message_response_message_root_blocks_elements_array_item_ref = cls(
            elements=elements,
            type_=type_,
        )

        send_message_response_message_root_blocks_elements_array_item_ref.additional_properties = d
        return send_message_response_message_root_blocks_elements_array_item_ref

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
